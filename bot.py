#!/usr/bin/env python3

import asyncio
import functools
import glob
import importlib
import json

import yaml
import os
import re
import signal
import sys
import traceback
import urllib.parse
import logging
import logging.config
import datetime
from importlib import reload

import requests
from nio import AsyncClient, InviteEvent, JoinError, RoomMessageText, MatrixRoom, LoginError, RoomMemberEvent, RoomVisibility, RoomPreset, RoomCreateError, RoomResolveAliasResponse, UploadError, UploadResponse

# Couple of custom exceptions


class CommandRequiresAdmin(Exception):
    pass


class CommandRequiresOwner(Exception):
    pass


class Bot:

    def __init__(self):
        self.appid = 'org.vranki.hemppa'
        self.version = '1.5'
        self.client = None
        self.join_on_invite = False
        self.modules = dict()
        self.leave_empty_rooms = True
        self.pollcount = 0
        self.poll_task = None
        self.owners = []
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.logger = None

        self.jointime = None  # HACKHACKHACK to avoid running old commands after join
        self.join_hack_time = 5  # Seconds

        self.initialize_logger()

    def initialize_logger(self):

        if os.path.exists('config/logging.yml'):
            with open('config/logging.yml') as f:
                config = yaml.load(f, Loader=yaml.Loader)
                logging.config.dictConfig(config)
        else:
            log_format = '%(levelname)s - %(name)s - %(message)s'
            logging.basicConfig(format=log_format)

        self.logger = logging.getLogger("hemppa")

        if self.debug:
            logging.root.setLevel(logging.DEBUG)
            self.logger.info("enabled debugging")

        self.logger.debug("Logger initialized")

    async def send_text(self, room, body, msgtype="m.notice", bot_ignore=False):
        msg = {
            "body": body,
            "msgtype": msgtype,
        }
        if bot_ignore:
            msg["org.vranki.hemppa.ignore"] = "true"

        await self.client.room_send(room.room_id, 'm.room.message', msg)

    async def send_html(self, room, html, plaintext, msgtype="m.notice", bot_ignore=False):
        msg = {
            "msgtype": msgtype,
            "format": "org.matrix.custom.html",
            "formatted_body": html,
            "body": plaintext
        }
        if bot_ignore:
            msg["org.vranki.hemppa.ignore"] = "true"
        await self.client.room_send(room.room_id, 'm.room.message', msg)

    async def send_image(self, room, url, body):
        """

        :param room: A MatrixRoom the image should be send to
        :param url: A MXC-Uri https://matrix.org/docs/spec/client_server/r0.6.0#mxc-uri
        :param body: A textual representation of the image
        :return:
        """
        msg = {
            "url": url,
            "body": body,
            "msgtype": "m.image"
        }
        await self.client.room_send(room.room_id, 'm.room.message', msg)

    async def send_msg(self, mxid, roomname, message):
        # Sends private message to user. Returns true on success.

        # Find if we already have a common room with user:
        msg_room = None
        for croomid in self.client.rooms:
            roomobj = self.client.rooms[croomid]
            if len(roomobj.users) == 2:
                for user in roomobj.users:
                    if user == mxid:
                        msg_room = roomobj

        # Nope, let's create one
        if not msg_room:
            msg_room = await self.client.room_create(visibility=RoomVisibility.private,
                name=roomname,
                is_direct=True,
                preset=RoomPreset.private_chat,
                invite={mxid},
                )

        if not msg_room or (type(msg_room) is RoomCreateError):
            self.logger.error(f'Unable to create room when trying to message {mxid}')
            return False

        # Send message to the room
        await self.send_text(msg_room, message)
        return True

    def remove_callback(self, callback):
        for cb_object in self.client.event_callbacks:
            if cb_object.func == callback:
                self.logger.info("remove callback")
                self.client.event_callbacks.remove(cb_object)

    def get_room_by_id(self, room_id):
        try:
            return self.client.rooms[room_id]
        except KeyError:
            return None

    async def get_room_by_alias(self, alias):
        rar = await self.client.room_resolve_alias(alias)
        if type(rar) is RoomResolveAliasResponse:
            return rar.room_id
        return None

    # Throws exception if event sender is not a room admin
    def must_be_admin(self, room, event):
        if not self.is_admin(room, event):
            raise CommandRequiresAdmin

    # Throws exception if event sender is not a bot owner
    def must_be_owner(self, event):
        if not self.is_owner(event):
            raise CommandRequiresOwner

    # Returns true if event's sender has PL50 or more in the room event was sent in,
    # or is bot owner
    # TODO: Make configurable
    def is_admin(self, room, event):
        if self.is_owner(event):
            return True
        if event.sender not in room.power_levels.users:
            return False
        return room.power_levels.users[event.sender] >= 50

    # Returns true if event's sender is owner of the bot
    def is_owner(self, event):
        return event.sender in self.owners

    # Checks if this event should be ignored by bot, including custom property
    def should_ignore_event(self, event):
        return "org.vranki.hemppa.ignore" in event.source['content']

    # Helper function to upload a image from URL to homeserver. Use send_image() to actually send it to room.
    async def upload_image(self, url):
        self.client: AsyncClient
        response: UploadResponse

        self.logger.debug(f"start downloading image from url {url}")
        url_response = requests.get(url)
        self.logger.debug(f"response [status_code={url_response.status_code}, headers={url_response.headers}")

        if url_response.status_code == 200:
            content_type = url_response.headers.get("content-type")
            self.logger.info(f"uploading content to matrix server [size={len(url_response.content)}, content-type: {content_type}]")
            (response, alist) = await self.client.upload(lambda a, b: url_response.content, content_type)
            self.logger.debug("response: %s", response)

            if isinstance(response, UploadResponse):
                self.logger.info("uploaded file to %s", response.content_uri)
                return response.content_uri
            else:
                response: UploadError
                self.logger.error("unable to upload file. msg: %s", response.message)
        else:
            self.logger.error("unable to request url: %s", url_response)

        return None


    def save_settings(self):
        module_settings = dict()
        for modulename, moduleobject in self.modules.items():
            try:
                module_settings[modulename] = moduleobject.get_settings()
            except Exception:
                traceback.print_exc(file=sys.stderr)
        data = {self.appid: self.version, 'module_settings': module_settings}
        self.set_account_data(data)

    def load_settings(self, data):
        if not data:
            return
        if not data.get('module_settings'):
            return
        for modulename, moduleobject in self.modules.items():
            if data['module_settings'].get(modulename):
                try:
                    moduleobject.set_settings(
                        data['module_settings'][modulename])
                except Exception:
                    traceback.print_exc(file=sys.stderr)

    async def message_cb(self, room, event):
        # Ignore if asked to ignore
        if self.should_ignore_event(event):
            if self.debug:
                self.logger.debug('Ignoring event!')
            return

        body = event.body
        # Figure out the command
        if not self.starts_with_command(body):
            return

        if self.owners_only and not self.is_owner(event):
            self.logger.info(f"Ignoring {event.sender}, because they're not an owner")
            await self.send_text(room, "Sorry, only bot owner can run commands.")
            return

        # HACK to ignore messages for some time after joining.
        if self.jointime:
            if (datetime.datetime.now() - self.jointime).seconds < self.join_hack_time:
                self.logger.info(f"Waiting for join delay, ignoring message: {body}")
                return
            self.jointime = None

        command = body.split().pop(0)

        # Strip away non-alphanumeric characters, including leading ! for security
        command = re.sub(r'\W+', '', command)

        moduleobject = self.modules.get(command)

        if moduleobject is not None:
            if moduleobject.enabled:
                try:
                    await moduleobject.matrix_message(self, room, event)
                except CommandRequiresAdmin:
                    await self.send_text(room, f'Sorry, you need admin power level in this room to run that command.')
                except CommandRequiresOwner:
                    await self.send_text(room, f'Sorry, only bot owner can run that command.')
                except Exception:
                    await self.send_text(room, f'Module {command} experienced difficulty: {sys.exc_info()[0]} - see log for details')
                    traceback.print_exc(file=sys.stderr)
        else:
            self.logger.error(f"Unknown command: {command}")
            # TODO Make this configurable
            # await self.send_text(room,
            #                     f"Sorry. I don't know what to do. Execute !help to get a list of available commands.")

    @staticmethod
    def starts_with_command(body):
        """Checks if body starts with ! and has one or more letters after it"""
        return re.match(r"^!\w.*", body) is not None

    async def invite_cb(self, room, event):
        room: MatrixRoom
        event: InviteEvent

        if self.join_on_invite or self.is_owner(event):
            for attempt in range(3):
                self.jointime = datetime.datetime.now()
                result = await self.client.join(room.room_id)
                if type(result) == JoinError:
                    self.logger.error(f"Error joining room %s (attempt %d): %s", room.room_id, attempt, result.message)
                else:
                    self.logger.info(f"joining room '{room.display_name}'({room.room_id}) invited by '{event.sender}'")
                    return
        else:
            self.logger.warning(f'Received invite event, but not joining as sender is not owner or bot not configured to join on invite. {event}')

    async def memberevent_cb(self, room, event):
        # Automatically leaves rooms where bot is alone.
        if room.member_count == 1 and event.membership=='leave':
            self.logger.info(f"membership event in {room.display_name} ({room.room_id}) with {room.member_count} members by '{event.sender}' - leaving room as i don't want to be left alone!")
            await self.client.room_leave(room.room_id)

    def load_module(self, modulename):
        try:
            self.logger.info(f'load module: {modulename}')
            module = importlib.import_module('modules.' + modulename)
            module = reload(module)
            cls = getattr(module, 'MatrixModule')
            return cls(modulename)
        except ModuleNotFoundError:
            self.logger.error(f'Module {modulename} failed to load!')
            traceback.print_exc(file=sys.stderr)
            return None

    def reload_modules(self):
        for modulename in self.modules:
            self.logger.info(f'Reloading {modulename} ..')
            self.modules[modulename] = self.load_module(modulename)

        self.load_settings(self.get_account_data())

    def get_modules(self):
        modulefiles = glob.glob('./modules/*.py')

        for modulefile in modulefiles:
            modulename = os.path.splitext(os.path.basename(modulefile))[0]
            moduleobject = self.load_module(modulename)
            if moduleobject:
                self.modules[modulename] = moduleobject

    def clear_modules(self):
        self.modules = dict()

    async def poll_timer(self):
        while True:
            self.pollcount = self.pollcount + 1
            for modulename, moduleobject in self.modules.items():
                if moduleobject.enabled:
                    try:
                        await moduleobject.matrix_poll(self, self.pollcount)
                    except Exception:
                        traceback.print_exc(file=sys.stderr)
            await asyncio.sleep(10)

    def set_account_data(self, data):
        userid = urllib.parse.quote(self.matrix_user)

        ad_url = f"{self.client.homeserver}/_matrix/client/r0/user/{userid}/account_data/{self.appid}?access_token={self.client.access_token}"

        response = requests.put(ad_url, json.dumps(data))
        self.__handle_error_response(response)

        if response.status_code != 200:
            self.logger.error('Setting account data failed. response: %s json: %s', response, response.json())

    def get_account_data(self):
        userid = urllib.parse.quote(self.matrix_user)

        ad_url = f"{self.client.homeserver}/_matrix/client/r0/user/{userid}/account_data/{self.appid}?access_token={self.client.access_token}"

        response = requests.get(ad_url)
        self.__handle_error_response(response)

        if response.status_code == 200:
            return response.json()
        self.logger.error(f'Getting account data failed: {response} {response.json()} - this is normal if you have not saved any settings yet.')
        return None

    def __handle_error_response(self, response):
        if response.status_code == 401:
            self.logger.error("access token is invalid or missing")
            self.logger.info("NOTE: check MATRIX_ACCESS_TOKEN")
            sys.exit(2)

    def init(self):

        self.matrix_user = os.getenv('MATRIX_USER')
        matrix_server = os.getenv('MATRIX_SERVER')
        bot_owners = os.getenv('BOT_OWNERS')
        access_token = os.getenv('MATRIX_ACCESS_TOKEN')
        join_on_invite = os.getenv('JOIN_ON_INVITE')
        owners_only = os.getenv('OWNERS_ONLY') is not None
        leave_empty_rooms = os.getenv('LEAVE_EMPTY_ROOMS')

        if matrix_server and self.matrix_user and bot_owners and access_token:
            self.client = AsyncClient(matrix_server, self.matrix_user, ssl = matrix_server.startswith("https://"))
            self.client.access_token = access_token
            self.join_on_invite = (join_on_invite or '').lower() == 'true'
            self.leave_empty_rooms = (leave_empty_rooms or 'true').lower() == 'true'
            self.owners = bot_owners.split(',')
            self.owners_only = owners_only
            self.get_modules()

        else:
            self.logger.error("The environment variables MATRIX_SERVER, MATRIX_USER, MATRIX_ACCESS_TOKEN and BOT_OWNERS are mandatory")
            sys.exit(1)

    def start(self):
        self.load_settings(self.get_account_data())
        enabled_modules = [module for module_name, module in self.modules.items() if module.enabled]
        self.logger.info(f'Starting {len(enabled_modules)} modules..')
        for modulename, moduleobject in self.modules.items():
            if moduleobject.enabled:
                try:
                    moduleobject.matrix_start(self)
                except Exception:
                    traceback.print_exc(file=sys.stderr)
        self.logger.info(f'All modules started.')

    def stop(self):
        self.logger.info(f'Stopping {len(self.modules)} modules..')
        for modulename, moduleobject in self.modules.items():
            try:
                moduleobject.matrix_stop(self)
            except Exception:
                traceback.print_exc(file=sys.stderr)
        self.logger.info(f'All modules stopped.')

    async def run(self):
        await self.client.sync()
        for roomid, room in self.client.rooms.items():
            self.logger.info(f"Bot is on '{room.display_name}'({roomid}) with {len(room.users)} users")
            if len(room.users) == 1 and self.leave_empty_rooms:
                self.logger.info(f'Room {roomid} has no other users - leaving it.')
                self.logger.info(await self.client.room_leave(roomid))

        self.start()

        self.poll_task = asyncio.get_event_loop().create_task(self.poll_timer())

        if self.client.logged_in:
            self.load_settings(self.get_account_data())
            self.client.add_event_callback(self.message_cb, RoomMessageText)
            self.client.add_event_callback(self.invite_cb, (InviteEvent,))
            self.client.add_event_callback(self.memberevent_cb, (RoomMemberEvent,))

            if self.join_on_invite:
                self.logger.info('Note: Bot will join rooms if invited')
            self.logger.info('Bot running as %s, owners %s', self.client.user, self.owners)
            self.bot_task = asyncio.create_task(self.client.sync_forever(timeout=30000))
            await self.bot_task
        else:
            self.logger.error('Client was not able to log in, check env variables!')

    async def shutdown(self):
        await self.close()

    async def close(self):
        try:
            await self.client.close()
            self.logger.info("Connection closed")
        except Exception as ex:
            self.logger.error("error while closing client: %s", ex)

    def handle_exit(self, signame, loop):
        self.logger.info(f"Received signal {signame}")
        if self.poll_task:
            self.poll_task.cancel()
        self.bot_task.cancel()
        self.stop()


async def main():
    bot = Bot()
    bot.init()

    loop = asyncio.get_running_loop()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(bot.handle_exit, signame, loop))

    await bot.run()
    await bot.shutdown()


try:
    asyncio.run(main())
except Exception as e:
    traceback.print_exc(file=sys.stderr)

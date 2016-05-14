import telepot

class API:
    def __init__(self,bot,apikey=None):
        def handle(msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            if content_type == "text":
                response=self.bot.process(msg['text'])
                self.apibot.sendMessage(chat_id,response)
        self.bot=bot
        if apikey:
            self.apibot=telepot.Bot(apikey)
            self.apibot.message_loop(handle)
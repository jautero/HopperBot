import telepot

class Message:
    def __init__(self,msg):
        self._msg=msg
        self.populate_dict(msg)

    def populate_dict(self,msg):
        self.__dict__['name']=msg['from']['first_name']
        self.__dict__['text']=msg['text']
class API:
    def __init__(self,bot,apikey=None):
        def handle(msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            if content_type == "text":
                response=self.bot.process(Message(msg))
                self.apibot.sendMessage(chat_id,response)
        self.bot=bot
        if apikey:
            self.apibot=telepot.Bot(apikey)
            self.apibot.message_loop(handle)

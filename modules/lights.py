from modules.common.module import BotModule

class LightsModule(BotModule):
  
  async def matrix_message(self, bot, room, event):
    pass

  def help(self):
    return 'Control lights'
  

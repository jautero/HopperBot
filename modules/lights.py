import aiohttp, os
from modules.common.module import BotModule

class MatrixModule(BotModule):

  def __init__(self, name):
    super().__init__(name)
    self.instance=os.environ['HA_URL']
    self.token=os.environ["HA_TOKEN"]
  
  async def matrix_message(self, bot, room, event):
    args = event.body.split()
    entity_id=args[1]
    action="toggle"
    if args[2] == "on":
      action="turn_on"
    elif args[2] == "off":
      action="turn_off"
    await self.lights(entity_id,action)

  def help(self):
    return 'Control lights'

  async def lights(self,entity_id,action):
    headers={'Authorization': 'Bearer '+self.token,}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(self.instance+'/api/services/light/'+action,json={"entity_id":entity_id}) as resp:
          return resp.status

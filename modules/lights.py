import aiohttp, os
from modules.common.module import BotModule

class LightsModule(BotModule):
  
  async def matrix_message(self, bot, room, event):
    pass

  def help(self):
    return 'Control lights'

  async def lights_on(self,entity_id):
    instance=os.environ['HA_URL']
    token=os.environ["HA_TOKEN"]
    headers={'Authorization': 'Bearer '+token,}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(instance+'/api/services/light/turn_on',json={"entity_id":entity_id}) as resp:
          return resp.status

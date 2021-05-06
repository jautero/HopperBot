import pytest
from aioresponses import aioresponses

import modules.lights
from modules.common.module import BotModule

@pytest.fixture
def dut():
  return modules.lights.MatrixModule("lights")

@pytest.fixture
def mock_aiohttpclient():
  with aioresponses() as mock_client:
    yield mock_client

def test_create_module(dut):
  assert dut

def test_is_botmodule(dut):
  assert isinstance(dut,BotModule)

class TestEvent:
  pass
  
@pytest.mark.asyncio
async def test_lights_on(dut,mock_aiohttpclient):
  mock_aiohttpclient.post(dut.instance+'/api/services/light/turn_on',status=200)
  assert 200 == await dut.lights("light.eteisen_kattolamppu","turn_on")

@pytest.mark.asyncio
async def  test_lights_message(dut,mock_aiohttpclient):
  mock_aiohttpclient.post(dut.instance+'/api/services/light/turn_on',status=200)
  mock_aiohttpclient.post(dut.instance+'/api/services/light/turn_off',status=200)
  mock_aiohttpclient.post(dut.instance+'/api/services/light/toggle',status=200)

  event=TestEvent()
  event.body="!lights light.eteisen_kattolamppu on"
  await dut.matrix_message("testbot","testroom",event)
  event.body="!lights light.eteisen_kattolamppu off"
  await dut.matrix_message("testbot","testroom",event)
  event.body="!lights light.eteisen_kattolamppu toggle"
  await dut.matrix_message("testbot","testroom",event)
  

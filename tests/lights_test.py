import pytest
from aioresponses import aioresponses

import modules.lights
from modules.common.module import BotModule

@pytest.fixture
def dut():
  return modules.lights.LightsModule("lights")

@pytest.fixture
def mock_aiohttpclient():
  with aioresponses() as mock_client:
    yield mock_client

def test_create_module(dut):
  assert dut

def test_is_botmodule(dut):
  assert isinstance(dut,BotModule)

@pytest.mark.asyncio
async def test_lights_on(dut,mock_aiohttpclient):
  mock_aiohttpclient.post('https://za6qz3v9vsv57ez6xmh5ubphzkys1xky.ui.nabu.casa/api/services/light/turn_on',status=200)
  assert 200 == await dut.lights_on("light.eteisen_kattolamppu")

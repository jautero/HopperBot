import pytest
import modules.lights
from modules.common.module import BotModule

@pytest.fixture
def dut():
  return modules.lights.LightsModule("lights")

def test_create_module(dut):
  assert dut

def test_is_botmodule(dut):
  assert isinstance(dut,BotModule)
  

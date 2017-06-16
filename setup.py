#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(name="HopperBot",
      version="0.4",
      description="HopperBot is a chatbot that learns. It is named after Admiral Grace Hopper.",
      author="Juha Autero",
      author_email="jautero@iki.fi",
      url="https://github.com/jautero/HopperBot",
      install_requires=["pytest","python-telegram-bot","pyyaml","chatterbot"],
      py_modules = ['HopperBot'])

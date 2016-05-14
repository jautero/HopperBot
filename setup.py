#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="HopperBot",
      version="0.1",
      description="HopperBot is a chatbot that can be programmed with simple sentences. It is named after Admiral Grace Hopper.",
      author="Juha Autero",
      author_email="jautero@iki.fi",
      url="https://github.com/jautero/HopperBot",
      install_requires=["pytest"],
      packages=)
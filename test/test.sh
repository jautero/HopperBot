#!/bin/sh
export WORKSPACE=/app
pip install pytest
cd /app; python -m pytest test

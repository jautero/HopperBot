#!/bin/bash
domain=jautero.ems.host
export MATRIX_USER="@hopperbot:$domain"
export MATRIX_ACCESS_TOKEN="MDAxZWxvY2F0aW9uIGphdXRlcm8uZW1zLmhvc3QKMDAxM2lkZW50aWZpZXIga2V5CjAwMTBjaWQgZ2VuID0gMQowMDJlY2lkIHVzZXJfaWQgPSBAaG9wcGVyYm90OmphdXRlcm8uZW1zLmhvc3QKMDAxNmNpZCB0eXBlID0gYWNjZXNzCjAwMjFjaWQgbm9uY2UgPSBGNz1wV1B0LGFER0VjdmErCjAwMmZzaWduYXR1cmUg2Zw2wSmY4bPE3_UI_GBCxl38gFOP06--nuErlHOvre8K" 
export MATRIX_SERVER="https://$domain"
# export JOIN_ON_INVITE="True"
export BOT_OWNERS="@jautero:$domain"
pipenv run python3 bot.py

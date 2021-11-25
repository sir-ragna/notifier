#!/bin/sh

## HOW TO SET UP
## To create the venv environment
# python -m venv venv
## Enter the virtual environment
# source venv/bin/activate
## Install deps
# pip -r requirements.txt

source venv/bin/activate

python manage.py runserver


#!/bin/bash

## HOW TO SET UP
## To create the venv environment
# python -m venv venv
## Enter the virtual environment
# source venv/bin/activate
## Install deps
# pip install -r requirements.txt

source venv/bin/activate

export DEBUG=TRUE
export SECRET_KEY='django-insecure-a62c754d-d754-4c40-a81a-73e6bff62ac6'
export TIME_ZONE='CET'

[[ -d attachments ]] || mkdir attachments 2>/dev/null
[[ -d database ]] || mkdir database 2>/dev/null

python manage.py runserver 0.0.0.0:8000


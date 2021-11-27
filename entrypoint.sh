#!/bin/sh

# Entrypoint for docker

python manage.py migrate

gunicorn notifier.wsgi --bind 0.0.0.0:8000 --log-file -

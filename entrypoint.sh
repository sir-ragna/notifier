#!/bin/sh

# Entrypoint for docker

python manage.py migrate

gunicorn notifier.wsgi --log-file -

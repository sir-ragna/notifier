#!/bin/sh

if [[ $1 == "" ]] ; then
    echo "Usage $0 <tag>"
    echo "Example $0 v0.4"
    exit 1
fi

# Build the static files
source venv/bin/activate
python manage.py collectstatic --no-input

# Build the main notfifier container
buildah build --layers --tag="notifier:$1" . 

## Build the corresponding nginx container
pushd nginx
buildah build --layers --tag="notinginx:$1" .
popd

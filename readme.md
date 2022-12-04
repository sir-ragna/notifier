
# Notifier

Notifier is a very simple website that catches alert notifications.

The notifications are created by performing a post request.
This can be done with one line of Powershell, so it is easy and fast to 
include in scripts.

The idea is not to use this as a monitoring tool for a large number of machines, 
but rather, to quickly write one-off scripts to monitor a specific event at on a 
specific system.

Maybe a certain error only rarely occurs, and you want to get 
notified when it happens. Instead of checking the log file on a daily basis,
_notifier_ was created, so you can quickly whip up a monitoring script to do 
the checking for you.

## Filters

The system has pagination and bookmarkable filters.

The URL http://0.0.0.0:8000/?description=100&customer=Contoso&system=System 
will only show events that contain **100** in their description, **Contoso**  
in their customer field and **System** in their system field.

# Deploying notifier

This is an explanation for Linux.
Both development and deployment could be done on Windows in theory, I haven't
tested this.

Download the source code. Either clone the git respository or download
the zip file.

```sh
curl https://codeload.github.com/sir-ragna/notifier/zip/refs/heads/main -o notifier-main.zip   
unzip notifier-main.zip
cd notifier-main
```

Set up a Python virtual environment. This will prevent issues between Python 
system modules and the versions used by this program. This allows us to run 
old and outdated programs.

```sh
python -m venv venv
```

The above command creates a virtual in the directory `venv`.
Activate the environment and install the dependencies from the _requirements.txt_ file.

```sh
source venv/bin/activate
pip install -r requirements.txt
```

Proceed with creating a user.

    python manage.py createsuperuser --username admin

Set up the database.

    python manage.py migrate


Set up a systemd service file. That includes the following environment variables.

```
SECRET_KEY='generate-someting-random-to-put-here'
TIME_ZONE='CET'
```

## User Management

Create a user to use the application.

    python manage.py createsuperuser --username admin

More users can be created from the `/admin/` page that is built-into Django.

![screenshot of the add user screen](screenshots/add-user.png)



## Containers

Build the container

    buildah build --layers --tag="notifier:v0.5" .  

Run the container

    podman run --rm -it -p 8000:8000 -v $(pwd)/database:/app/database notifier:v0.6

    podman run --rm -it -p 8000:8000 -v $(pwd)/database:/app/database -v $(pwd)/attachments:/app/attachments -e SECRET_KEY='django-insecure-a62c754d-d754-4c40-a81a-73e6bff62ac6' localhost/notifier:v0.6

The container is using [gunicorn](https://gunicorn.org/) 
to run Django. As such it will not serve any
static files. To serve static files you are supposed to run an nginx server in 
front. To test this I have a Dockerfile and nginx configuration file in 
the nginx directory.


# Filter system

Filter on customer, system or keywords in description.

Make these bookmarkable.

http://website/notifications?desc="abc"&system="myserver"

# Attachments

Allow downloading of attachments.

# Development setup

Requires python 3. Instantiate the virtual environment and activate it.

```sh
python -m venv venv
source venv/bin/activate
```

Apply the migrations

```sh
python manage.py migrate
```

Create a new superuser.

```sh
python manage.py createsuperuser
```


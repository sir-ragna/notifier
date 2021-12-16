
# Notifier

The goal was to be able to easily generate alerts to a central server and 
optionally include attachments.

Ideally the alerts can be created with a powershell one-liner.

Authentication is done with a GUID that is also associated with a customer.

## Users

Create a user to use the application.

    python manage.py createsuperuser --username admin

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

# Notification

- Timestamp
- Description
- Customer
- System
- (Attachments)

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

Create a new super user.

```sh
python manage.py createsuperuser
```

Set the parameters.

```sh
export DEBUG=TRUE  # Activate debugging
export SECRET_KEY='django-insecure-a62c754d-d754-4c40-a81a-73e6bff62ac6' # set a secret key
export TIME_ZONE='CET' # Set the timezone
```

Start the server in DEV mode.

```sh
python manage.py runserver
```

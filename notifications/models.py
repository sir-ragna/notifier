
from django.db import models

class Notification(models.Model):
    time = models.DateTimeField(null=False)
    description = models.CharField(max_length=1024, null=False)
    customer = models.CharField(max_length=100, null=False)
    system = models.CharField(max_length=100, null=False)
    attachment_path = models.CharField(max_length=200, null=True)
    source_ip = models.CharField(max_length=100)

    def __str__(self):
        return f"{time}:{customer}:{system}:{description}"

class Customer(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    guid = models.CharField(max_length=50, null=False, unique=True)

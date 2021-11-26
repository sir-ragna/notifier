
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from pathlib import Path

def save_attachment(customer, filename, filehandle):
    customer = customer.replace('/', '')
    
    directory = f"attachments/{customer}/"
    filename = f"attachments/{customer}/{filename}"
    Path(directory).mkdir(parents=True, exist_ok=True)

    if not default_storage.exists(filename):
        with default_storage.open(filename, "wb+") as destination:
            for chunk in filehandle.chunks():
                destination.write(chunk)

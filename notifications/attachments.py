
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import FileResponse

from pathlib import Path

def save_attachment(customer, filename, filehandle):
    """Saves an attachment. Returns the file path on success, None on failure"""
    customer = customer.replace('/', '')
    
    directory = f"attachments/{customer}/"
    filename = f"attachments/{customer}/{filename}"
    Path(directory).mkdir(parents=True, exist_ok=True)

    if not default_storage.exists(filename):
        with default_storage.open(filename, "wb+") as destination:
            for chunk in filehandle.chunks():
                destination.write(chunk)
        return filename
    return None

def remove_attachment(filepath):
    return default_storage.delete(filepath)

def size_attachment(filepath):
    return default_storage.size(filepath)

def download_attachment(request, filepath):
    return FileResponse(default_storage.open(filepath, 'rb'))
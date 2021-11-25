
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import forms
from . import models

def index(request):
    """
    Shows the last 100 notifications (with infinite scroll?)
    """
    return HttpResponse("Hello World")

@csrf_exempt # We'll call this from scripts, not just from webpages (consider ratelimiting)
def create_notification(request):
    """
    Creates a notification from a POST request.
    """
    if request.method == 'POST':
        notification_form = forms.NotificationForm(request.POST)    
    else:
        notification_form = forms.NotificationForm()
    
    return render(request, "notify.html.j2", 
        {'notification_form': notification_form})

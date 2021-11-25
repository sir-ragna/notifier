
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

import datetime

from . import forms
from . import models


def index(request):
    """
    Shows the last 100 notifications (with infinite scroll?)
    """
    page = 0
    if request.method == 'GET' and 'amount' in request.GET:
        amount = abs(int(request.GET['amount']))
        if 'page' in request.GET:
            page = abs(int(request.GET['page']))
    else:
        amount = 10
    notifications = models.Notification.objects.order_by('-time')[page * amount:(page + 1) * amount]
    return render(request, "index.html.j2", {
        'notifications': notifications,
        'nextpage': page + 1,
        'previous': page - 1,
        'amount': amount,
    })

@csrf_exempt # We'll call this from scripts, not just from webpages (maybe consider ratelimiting)
def create_notification(request):
    """
    Creates a notification from a POST request.
    """
    if request.method == 'POST':
        notification_form = forms.NotificationForm(request.POST)
        if notification_form.is_valid():
            time = datetime.datetime.now()
            description = notification_form.cleaned_data['description']
            customer = notification_form.cleaned_data['customer']
            system = notification_form.cleaned_data['system']
            source_ip = request.META['REMOTE_ADDR']
            notification = models.Notification(
                time=time,
                description=description,
                customer=customer,
                system=system,
                source_ip=source_ip,
            )
            notification.save()
            messages.info(request, "Added notification")
        else:
            messages.error(request, "Failed to add notification")
    else:
        notification_form = forms.NotificationForm()
    
    return render(request, "notify.html.j2", 
        {'notification_form': notification_form})

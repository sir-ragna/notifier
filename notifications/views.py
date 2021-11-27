
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone

import datetime
import uuid

from . import forms
from . import models
from . import attachments


def index(request):
    """
    Shows the last 100 notifications (with infinite scroll?)
    """
    page = 0
    filter_form = forms.FilterForm(request.GET)

    if request.method == 'GET' and 'amount' in request.GET:
        amount = abs(int(request.GET['amount']))
        if 'page' in request.GET:
            page = abs(int(request.GET['page']))
    else:
        amount = 10
    if filter_form.is_valid():
        time = filter_form.cleaned_data['time'] # filter elements before time
        if not time:
            #time = datetime.datetime.now() # version without timezone
            time = timezone.now()           # version with timezone
        customer_name = filter_form.cleaned_data['customer']
        system = filter_form.cleaned_data['system']
        description = filter_form.cleaned_data['description']

        customer_objects = models.Customer.objects.filter(name__icontains=customer_name)
        notifications = models.Notification.objects.filter(
            customer__in=customer_objects,      # 
            system__icontains=system,           # contains, case insensitive match
            description__icontains=description, #
            time__lte=time                      # less than, only older events
            ).order_by('-time'
            )[page * amount:(page + 1) * amount]
    else:
        notifications = models.Notification.objects.order_by('-time')[page * amount:(page + 1) * amount]
    return render(request, "index.html.j2", {
        'notifications': notifications,
        'nextpage': page + 1,
        'previous': page - 1,
        'amount': amount,
        'filter_form': filter_form,
    })

@csrf_exempt # We'll call this from scripts, not just from webpages (maybe consider ratelimiting)
def create_notification(request):
    """
    Creates a notification from a POST request.
    """
    if request.method == 'POST':
        notification_form = forms.NotificationForm(request.POST, request.FILES)
        if notification_form.is_valid():
            #time = datetime.datetime.now() # 
            time = timezone.now()           # Datetime with timezone
            description = notification_form.cleaned_data['description']
            customer_guid = notification_form.cleaned_data['customer']
            customer_objects = models.Customer.objects.filter(guid=customer_guid)
            if len(customer_objects) > 0:
                customer = customer_objects[0]
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
                filename = notification.id
                messages.info(request, "Added notification")
                # Handle file upload when present
                if 'attachment' in request.FILES:
                    attachments.save_attachment(customer.name, filename, request.FILES['attachment'])
            else:
                messages.error(request, "Error: Customer GUID not found")
        else:
            messages.error(request, "Failed to add notification")
    else:
        notification_form = forms.NotificationForm()
    
    # customers = models.Customer.objects.all()
    # options = [(c.guid, c.name) for c in customers]
    # notification_form.fields['customer'].widget.choices = options #
    #notification_form['customer'].field.widget.choices = options # also works

    return render(request, "notify.html.j2", 
        {'notification_form': notification_form})

def manage_customers(request):
    if request.method == "POST":
        customer_form = forms.CustomerForm(request.POST)
        if customer_form.is_valid():
            name = customer_form.cleaned_data['name']
            guid = str(uuid.uuid4()) # generate GUID
            new_customer = models.Customer(name=name, guid=guid)
            new_customer.save()
            messages.info(request, f"Created customer({name})")
    else:
        customer_form = forms.CustomerForm()
    
    customers = models.Customer.objects.all()
    
    return render(request, "customers.html.j2", {
        'customer_form': customer_form, 
        'customers': customers
    })
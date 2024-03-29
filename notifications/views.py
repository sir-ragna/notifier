
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import auth


import datetime
import uuid

from . import forms
from . import models
from . import attachments

@login_required(login_url='/admin')
def index(request):
    """
    Shows the last 100 notifications (with infinite scroll?)
    """
    page = 0   # Default page that contains the last events
    min_id = int(request.GET.get('from', '0')) # Minimum ID

    filter_form = forms.FilterForm(request.GET)

    if request.method == 'GET' and 'amount' in request.GET:
        amount = abs(int(request.GET['amount']))
        if 'page' in request.GET:
            page = abs(int(request.GET['page']))
    else:
        amount = 50
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
            time__lte=time,                     # less than, only older events
            id__gt=min_id
            ).order_by('-time'
            )[page * amount:(page + 1) * amount]
    else:
        notifications = models.Notification.objects.filter(id__gt=min_id) \
            .order_by('-time')[page * amount:(page + 1) * amount]
    
    if request.content_type == 'application/json':
        data = {
            'customers': list(models.Customer.objects.all().values()),
            'notifications': list(notifications.values())
        }
        return JsonResponse(data)
        #return HttpResponse(serialize('json', notifications))
    
    return render(request, "index.html.j2", {
        'notifications': notifications,
        'nextpage': page + 1,
        'previous': 0 if page - 1 < 0 else page - 1,
        'amount': amount,
        'filter_form': filter_form,
    })

@login_required(login_url='/admin')
def delete_notifications(request):
    """
    This page will show notifications and allow us to delete notifications.
    """

    # Check if we get a post to delete an event
    if request.method == 'POST':
        action = request.POST.get('action', '')
        id = int(request.POST.get('id', -1))
        if action == 'delete' and id > 0:
            notification = models.Notification.objects.get(id=id)
            print("Notification to delete", notification)
            print(notification.delete())
            message = f"Succesfully removed notification (id:{id})."
            if not notification.attachment_path is None :
                message += f" removing attachment of size {attachments.size_attachment(notification.attachment_path)} bytes"
                attachments.remove_attachment(notification.attachment_path)
            messages.success(request, message)

    # Retrieve the last events.

    page = 0   # Default page that contains the last events
    min_id = int(request.GET.get('from', '0')) # Minimum ID

    filter_form = forms.FilterForm(request.GET)

    if request.method == 'GET' and 'amount' in request.GET:
        amount = abs(int(request.GET['amount']))
        if 'page' in request.GET:
            page = abs(int(request.GET['page']))
    else:
        amount = 50
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
            time__lte=time,                     # less than, only older events
            id__gt=min_id
            ).order_by('-time'
            )[page * amount:(page + 1) * amount]
    else:
        notifications = models.Notification.objects.filter(id__gt=min_id) \
            .order_by('-time')[page * amount:(page + 1) * amount]

    return render(request, "delete_notifications.html.j2", {
        'notifications': notifications,
        'nextpage': page + 1,
        'previous': 0 if page - 1 < 0 else page - 1,
        'amount': amount,
        'filter_form': filter_form,
    })

@csrf_exempt # We'll call this from scripts, not just from webpages (maybe consider ratelimiting)
def create_notification(request):
    """
    Creates a notification from a POST request.
    When surfing to this page we'll get a form that can be used to manually 
    create a _notification_. The page also helps with scripting these events.
    """
    ret_status = 200
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
                messages.info(request, "Added notification")
                # Handle file upload when present
                if 'attachment' in request.FILES:
                    file_attachment = request.FILES['attachment']
                    filename = f"{notification.id}_{file_attachment.name}"
                    file_path = attachments.save_attachment(customer.name, filename, file_attachment)
                    notification.attachment_path = file_path
                    notification.save()
            else:
                messages.error(request, "Error: Customer GUID not found")
                ret_status = 404
        else:
            messages.error(request, "Failed to add notification")
            ret_status = 500
    else:
        notification_form = forms.NotificationForm()
    
    return render(request, "notify.html.j2",
        {'notification_form': notification_form}, status=ret_status)

@login_required(login_url='/admin')
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
            messages.error(request, "Failed to create customer")
    else:
        customer_form = forms.CustomerForm()
    
    customers = models.Customer.objects.all()
    
    return render(request, "customers.html.j2", {
        'customer_form': customer_form, 
        'customers': customers
    })

@login_required(login_url='/admin')
def download_attachment(request, customer, filename):
    filepath = f"attachments/{customer}/{filename}"
    return attachments.download_attachment(request, filepath)

def logout(request):
    auth.logout(request)
    return redirect('index')
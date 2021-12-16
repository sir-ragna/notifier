from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('notify', views.create_notification, name="create notification"),
    path('customer', views.manage_customers, name="manage customers"),
    path('attachments/<str:customer>/<str:filename>', views.download_attachment, name="download attachment"),
    path('logout', views.logout, name="logout"),
]

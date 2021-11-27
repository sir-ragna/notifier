
from django import forms
from . import models

class NotificationForm(forms.Form):
    description = forms.CharField(max_length=1024, 
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Found error in log.txt'}))
    # customer = forms.CharField(max_length=100,label="Customer",
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control', 'placeholder': 'Customer 01'}))
    customer = forms.CharField(label="Customer",
        widget=forms.Select(choices=[('abc', 'ABC'), ('xyz', 'XYZ')]))
    system = forms.CharField(max_length=100,label="system",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'system xyz'}))    
    attachment = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        """
        Bit of magic. Retrieves the customer options for the dropdown box.
        """
        super().__init__(*args, **kwargs) # Call __init__() on the parent object
                                          # with the same arguments as this __init__
                                          # This is necessary so our fields are 
                                          # initialized.
        customers = models.Customer.objects.all()
        options = [(c.guid, c.name) for c in customers] # Build select options 
                                                        # List of tuples
        self['customer'].field.widget.choices = options 


class FilterForm(forms.Form):
    time = forms.DateTimeField(label="Events Before",required=False,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local','class': 'form-control'}))   
    description = forms.CharField(max_length=1024,required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Contained in description'}))
    customer = forms.CharField(max_length=100,label="Customer",required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Customer'}))
    system = forms.CharField(max_length=100,label="system",required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'System'}))   

class CustomerForm(forms.Form):
    name = forms.CharField(max_length=100,label="Customer name",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Contoso'}))

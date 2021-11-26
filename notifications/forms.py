
from django import forms

class NotificationForm(forms.Form):
    description = forms.CharField(max_length=1024, 
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Found error in log.txt'}))
    customer = forms.CharField(max_length=100,label="Customer",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Customer 01'}))
    system = forms.CharField(max_length=100,label="system",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'system xyz'}))    
    attachment = forms.FileField(required=False)

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


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

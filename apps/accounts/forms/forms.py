from django import forms


class editform(forms.Form):
    username = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100,error_messages={'required': 'Please enter your Lastname'})
    firstname = forms.CharField(max_length=100,error_messages={'required': 'Please enter your Firstname'})
    email = forms.CharField(max_length=100)

from django import forms


class editform(forms.Form):
    username = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    firstname = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)

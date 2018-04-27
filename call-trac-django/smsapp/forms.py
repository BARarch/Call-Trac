from django import forms

class SMSForm(forms.Form):
	name = forms.CharField(max_length=120)
	number = forms.CharField(max_length=20)
	message = forms.CharField(max_length=150)
from django import forms

class SMSForm(forms.Form):
	name = forms.CharField(max_length=120,
		widget=forms.TextInput(attrs={'class': "form-control col-12",
									  'type':"text",
									  'placeholder':"Name ",
									   'aria-label':"Name",
									   'aria-describedby':"basic-addon2"}))
	number = forms.CharField(max_length=20,
		widget=forms.TextInput(attrs={'class': "form-control",
									  'type':"text",
									  'placeholder':"Number ex:+18885552222",
									   'aria-label':"Number",
									   'aria-describedby':"basic-addon2"}),)
	message = forms.CharField(max_length=160,
		widget=forms.TextInput(attrs={'class': "form-control",
									  'type':"text",
									  'placeholder':"Enter Message...",
									   'aria-label':"Enter Message...",
									   'aria-describedby':"basic-addon2"}),)
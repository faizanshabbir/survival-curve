from django import forms

class ContactKMForm(forms.Form):
	name = forms.CharField(max_length=255,)
	email = forms.EmailField()

	message = forms.CharField(widget=forms.Textarea)
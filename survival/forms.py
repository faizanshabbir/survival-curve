from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.core.validators import validate_email

class ContactKMForm(forms.Form):
	name = forms.CharField(max_length=255,)
	email = forms.EmailField()

	message = forms.CharField(widget=forms.Textarea)

# class basicUserSignup(forms.Form):
# 	username = forms.CharField(max_length=255,)
# 	password = forms.CharField(max_length=255,)

# 	first name = forms.CharField(max_length=255,)
# 	last name = forms.CharField(max_length=255,)
# 	email = forms.EmailField()

class basicUserSignup(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from all the fields given in the base user model.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'empty_email':_("You must specify an email address"),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username","email","first_name","last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def check_email(self):
    	if not validate_email(email):
    		raise forms.ValidationError(
    			self.error_messages['empty_email'],
    			code='empty_email',
    		)
    	return email


    def save(self, commit=True):
        user = super(basicUserSignup, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
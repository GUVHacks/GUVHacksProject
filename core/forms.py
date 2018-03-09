import datetime

from django import forms
from django.contrib.auth.models import User

from core.models import *

class DateTypeInput(forms.DateInput):
    # used as a way to allow a date input type
    input_type = 'date'


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'email', 'password')


class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())


class AccountForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('name', 'phone', 'address', 'city', 'gender', 'age')


class EmploymentForm(forms.ModelForm):

	class Meta:
		model = Employment
		fields = ('employer', 'phone', 'wage', 'start_date', 'end_date', 'currently_employed')
		widgets = {'start_date': DateTypeInput,
				   'end_date': DateTypeInput}

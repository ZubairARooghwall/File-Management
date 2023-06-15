from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

#Import all the models
from .models import User

class MyUserRegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['name', 'username', 'email', 'password1', 'password2', 'bio', 'avatar', 'prefer_dark_theme', 'education']
		
		# in form, you add enctype="multipart/form-data"
		# in views.py, form = MyUserRegistrationForm(..add request.FILES...)
from django.db import models
# Import module for creating custom User
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
	pass
	username = models.CharField(max_length=30)
	email = models.CharField(max_length=120, unique=True, primary_key=True)
	date_of_birth = models.DateField(help_text="Enter your date of birth")
	education = models.IntegerField(help_text="Add years of education", null=True, editable=True)
	
	
	
	def __str__(self):
		return self.username

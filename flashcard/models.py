from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
	name = models.CharField(max_length=200, null=True)
	email = models.EmailField(unique=True)
	bio = models.TextField(null=True)
	
	avatar = models.ImageField(null=True, default="avatar/avatar.svg")
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
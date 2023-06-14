from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required  # It ensures that the user is logged in or not


#Import all the models
from .models import User, Subject, Topics, FlashCard, Notes, Log, Messages, Friendship, Group, Membership, GroupMessages, Todo # Continue adding the models
# Create your views here.


def home(request):
	
	
	render(request, '')
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required  # It ensures that the user is logged in or not


#Import all the models
from .models import User, Subject, Topics, FlashCard, Notes, Log, Messages, Friendship, Group, Membership, GroupMessages, Todo # Continue adding the models
# Create your views here.


# @login_required(login_url='login')
def home(request):
	
	user = request.user
	inspirational_quote = 0;
	todo = Todo.objects.all().order_by("created")
	notes = Notes.objects.all().order_by("-updated") # - means descending order
	subjects = Subject.objects.all().order_by("-updated")
	topics = Topics.objects.all().order_by("-updated")
	flashcards = FlashCard.objects.all().order_by("-updated")
	messages = Messages.objects.all().order_by("-created")
	group_messages = GroupMessages.objects.all().order_by("-created")
	membership = Membership.objects.all()
	groups = Group.objects.all()
	
	context = {"user": user, "inspirational": inspirational_quote, "todo": todo,
	           "notes": notes, "subjects": subjects, "topics": topics, "flashcards": flashcards,
	           "messages": messages, "group_messages": group_messages, "membership": membership,
	           "groups": groups}
	return render(request, 'flashcards/home.html', context)
	
	
def settings(request):
	
	
	
	return render(request, 'flashcards/conf/settings.html')


def credit(request):
	# This view is for all the people or websites who helped me

	return render(request, 'flashcards/conf/credit.html')
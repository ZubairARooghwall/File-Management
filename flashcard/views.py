from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required  # It ensures that the user is logged in or not
from .forms import MyUserRegistrationForm, UserForm


#Import all the models
from .models import User, Subject, Topics, FlashCard, Notes, Log, Messages, Friendship, Group, Membership, GroupMessages, Todo # Continue adding the models
# Create your views here.

# user authentication

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		
		if email is not None:
			email = email.lower()
		else:
			messages.error(request, "Email is required")
			return redirect('login')
		
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			messages.error(request, "User does not exist")
			return redirect('login')
			
		user = authenticate(request, email=email, password=password)
		
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.error(request, 'Username or password does not exist')
		
	page = 'login'
	context = {'page': page}
	return render(request, 'flashcards/registration/login_registration.html', context)
		

def registerPage(request):
	form = MyUserRegistrationForm()
	
	if request.method == 'POST':
		form = MyUserRegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			email = form.cleaned_data['email']
			if User.objects.filter(email=email).exists():
				messages.error(request, "User with this email already exists")
				return redirect("register")
			
			user = form.save(commit=False)
			user.email = user.email.lower()
			user.username = user.username.lower()
			user.save()
			
			login(request, user)
			return redirect('home')
		else:
			messages.error(request, form.errors)
			
	return render(request, 'flashcards/registration/login_registration.html', {"form": form})


def logoutPage(request):
	logout(request)
	return redirect('home')

# end user authentication
# all user management
@login_required(login_url='login')





# end user management

@login_required(login_url='login')
def home(request):
	
	user = request.user
	inspirational_quote = 0
	todo = Todo.objects.all().order_by("created")
	notes = Notes.objects.all().order_by("-updated") # - means descending order
	subjects = Subject.objects.all().order_by("-updated")
	topics = Topics.objects.all().order_by("-updated")
	flashcards = FlashCard.objects.all().order_by("-updated")
	messagess = Messages.objects.all().order_by("-created")
	group_messages = GroupMessages.objects.all().order_by("-created")
	membership = Membership.objects.all()
	groups = Group.objects.all()
	
	context = {"user": user, "inspirational": inspirational_quote, "todo": todo,
	           "notes": notes, "subjects": subjects, "topics": topics, "flashcards": flashcards,
	           "messages": messagess, "group_messages": group_messages, "membership": membership,
	           "groups": groups}
	return render(request, 'flashcards/home.html', context)
	
	
@login_required(login_url='login')
def settings(request):
	user = request.user
	form = UserForm(instance=user)
	
	if request.method == 'POST':
		form = UserForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
			return redirect('settings')
		
	return render(request, 'flashcards/conf/settings.html', {'form': form})


def credit(request):
	# This view is for all the people or websites who helped me

	return render(request, 'flashcards/conf/credit.html')


@login_required(login_url='login')
def statistics(request):
	
	
	return render(request, 'flashcards/statistics.html')


# all to do lists






# end to do lists
# all notes





# end notes
# all statistics







# end statistics
# all subjects




# end subjects
# all topics





# end topics
# all flashcards





# end flashcards
# all friends' chats





# end friends' chats
# all group chats





# end group chats
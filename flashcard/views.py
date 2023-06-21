from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required  # It ensures that the user is logged in or not
from django.views.decorators.csrf import csrf_exempt

from .forms import MyUserRegistrationForm, UserForm, NotesForm, TodoForm, SubjectForm, TopicForm, FlashcardForm

#Import all the models
from .models import User, Subject, Topics, FlashCard, Notes, Messages, Friendship, Group, Membership, GroupMessages, Todo # Continue adding the models
# Create your views here.

# user authentication###################################################################################################

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
def delete_account(request):
	try:
		u = User.objects.get(id=request.user.id)
		u.delete()
		messages.success(request, "The is deleted")
		
		return redirect('login')
	
	except User.DoesNotExist:
		messages.error(request, "User does not exist")

	
	return render(request, 'flashcards/conf/delete.html')


# edit user
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


#End user management####################################################################################################
# Main pages############################################################################################################

@login_required(login_url='login')
def home(request):
	user = request.user
	inspirational_quote = 0
	
	notes = Notes.objects.filter(creator=request.user).order_by("-updated")
	to_do = Todo.objects.filter(creator=request.user).order_by("created")
	subjects = Subject.objects.filter(creator=request.user).order_by("-updated")
	topics = Topics.objects.filter(creator = user).order_by("-updated")
	flashcards = FlashCard.objects.filter(creator = user).order_by("-updated")
	messagess = Messages.objects.all().order_by("-created")
	group_messages = GroupMessages.objects.all().order_by("-created")
	membership = Membership.objects.all()
	groups = Group.objects.all()
	error_message = 0

	context = {"user": user, "inspirational": inspirational_quote, "todo": to_do,
	           "notes": notes, "topics": topics, "flashcards": flashcards,
	            "subjects": subjects,
			}
	
	
	return render(request, 'flashcards/home.html', context)



@login_required(login_url='login')
def subject(request, pk):
	user = request.user
	
	current_subject = Subject.objects.get(id=pk)
	topics = Topics.objects.filter(creator=user, subject=current_subject).order_by("-updated")
	
	subjects = Subject.objects.filter(creator=request.user).order_by("-updated")
	notes = Notes.objects.filter(creator=user).order_by("-updated")
	to_do = Todo.objects.filter(creator=user).order_by("created")
	
	context = {"notes": notes, "todo": to_do, "topics": topics, "subject": subjects, "current_subject": current_subject}
	
	return render(request, 'flashcards/important/subject.html', context)


def topic(request, topic_id, subject_id):
	current_subject = Subject.objects.get(id=subject_id)
	
	current_topic = Topics.objects.get(id=topic_id)
	flashcards = FlashCard.objects.filter(creator=request.user, topic__subject=current_topic.subject, topic=current_topic).order_by("-updated")
	
	notes = Notes.objects.filter(creator=request.user).order_by("-updated")
	to_do = Todo.objects.filter(creator=request.user).order_by("created")
	
	flashcard_question_preview = ""
	flashcard_answer_preview = ""
	
	if flashcards:
		question = flashcards[0].question
		flashcard_question_preview = question[:40]
		if len(question) > 40:
			flashcard_question_preview += "..."
		
		answer = flashcards[0].answer
		flashcard_answer_preview = answer[:20]
		if len(answer) > 20:
			flashcard_answer_preview += "..."
	
	
	context = {"notes": notes, "todo": to_do, "current_topic": current_topic,
	           "current_subject": current_subject, "flashcards": flashcards,
	           "question_preview": flashcard_question_preview, "answer_preview": flashcard_answer_preview}
	return render(request, 'flashcards/important/topic.html', context)


def flashcard(request, subject_id, topic_id, flashcard_id):
	current_subject = Subject.objects.get(id=subject_id)
	current_topic = Topics.objects.get(id=topic_id)
	
	notes = Notes.objects.filter(creator=request.user).order_by("-updated")
	to_do = Todo.objects.filter(creator=request.user).order_by("created")
	
	flashcards = FlashCard.objects.get(creator=request.user, topic__subject=current_topic.subject,
	                                     topic=current_topic, id=flashcard_id)
	
	context = {"notes": notes, "todo": to_do, "topic": current_topic, "subject": current_subject, "flashcards": flashcards}
	return render(request, "flashcards/important/flashcard.html", context)


def flashcard_preview(request, subject_id, topic_id, flashcard_id):
	current_subject = Subject.objects.get(id=subject_id)
	current_topic = Topics.objects.get(id=topic_id)
	
	notes = Notes.objects.filter(creator=request.user).order_by("-updated")
	to_do = Todo.objects.filter(creator=request.user).order_by("created")
	
	flashcards = FlashCard.objects.get(creator=request.user, topic__subject=current_topic.subject,
	                                   topic=current_topic, id=flashcard_id)
	
	context = {"notes": notes, "todo": to_do, "topic": current_topic, "subject": current_subject,
	           "flashcards": flashcards}
	return render(request, "flashcards/important/flashcard_preview.html", context)


#Study flashcards #######################################################################################################
@csrf_exempt
def study_flashcards(request):
	flashcards = FlashCard.objects.filter(creator=request.user)
	total_flashcards = flashcards.count()
	current_flashcard_index = request.session.get('current_flashcard_index', 0)
	
	if current_flashcard_index >= total_flashcards:
		# Reset the current_flashcard_index if all flashcards have been studied
		request.session['current_flashcard_index'] = 0
		messages.info(request, "You have completed studying all flashcards.")
		return redirect('completed')
	
	current_flashcard = flashcards[current_flashcard_index]
	
	return render(request, 'flashcards/studying/study.html', {
		'flashcard': current_flashcard,
		'current_flashcard_index': current_flashcard_index,
		'total_flashcards': total_flashcards,
	})


	
# @csrf_exempt
# def update_flashcard_score(request):
# 	if request.method != 'POST':
# 		return JsonResponse({'success': False, 'message': 'Invalid request method'})
# 	flashcard_scores = request.session.get('flashcard_scores', {})
# 	flashcard_id = request.POST.get('flashcard_id')
# 	score = int(request.POST.get('score'))
#
# 	# Get the flashcard object from the database
# 	flashcard = get_object_or_404(FlashCard, id=flashcard_id)
#
# 	# Initialize scores and lapses dictionary for a new flashcard
# 	if flashcard_id not in flashcard_scores:
# 		flashcard_scores[flashcard_id] = {'score': 0, 'lapses': 0}
#
# 	# Update the flashcard's score and lapses
# 	flashcard_scores[flashcard_id]['score'] += score
# 	flashcard_scores[flashcard_id]['lapses'] += 1
#
# 	# Save the updated flashcard scores in the session
# 	request.session['flashcard_scores'] = flashcard_scores
#
# 	# Update the flashcard object in the database
# 	flashcard.score = score
# 	flashcard.lapses += 1
# 	flashcard.save()
#
# 	# Increment the current_flashcard_index in the session
# 	current_flashcard_index = request.session.get('current_flashcard_index', 0)
# 	request.session['current_flashcard_index'] = current_flashcard_index + 1
# 	return JsonResponse({'success': True})

@csrf_exempt
def update_flashcard_index(request):
	if request.method == 'POST':
		current_flashcard_index = request.session.get('current_flashcard_index', 0)
		request.session['current_flashcard_index'] = current_flashcard_index + 1
		return JsonResponse({'success': True, 'index': current_flashcard_index})
	
	return JsonResponse({'success': False, 'message': 'Invalid request method'})
	
	
def completed_page(request):
	# Get all flashcards
	flashcards = FlashCard.objects.all()
	flashcard_scores = request.session.get('flashcard_scores', {})
	
	# Calculate total flashcards and total correct flashcards
	total_flashcards = flashcards.count()
	total_correct = sum(flashcard_scores.get(str(flashcard.id), {}).get('score', 0) > 0 for flashcard in flashcards)
	
	context = {
		'flashcards': flashcards,
		'total_flashcards': total_flashcards,
		'total_correct': total_correct,
	}
	
	return render(request, 'flashcards/studying/completed.html', context)
	
	

def credit(request):
	# This view is for all the people or websites who helped me
	
	return render(request, 'flashcards/conf/credit.html')


@login_required(login_url='login')
def statistics(request):
	return render(request, 'flashcards/components/statistics.html')

#End Main Pages#########################################################################################################
#Component pages########################################################################################################





#End Component page#####################################################################################################
#Create Things##########################################################################################################
@login_required(login_url='login')
def create_todo(request):
	if request.method == "POST":
		form = TodoForm(request.POST)
		if form.is_valid():
			todo = form.save(commit=False)
			todo.creator = request.user
			todo.save()
			next_url = request.GET.get("next", '/')
			return redirect(next_url)
	else:
		form = TodoForm()
	
	return render(request, 'flashcards/components/createToDo.html', {"forms": form})


@login_required(login_url='login')
def create_notes(request):
	if request.method == 'POST':
		form = NotesForm(request.POST)
		if form.is_valid():
			notes = form.save(commit=False)
			notes.creator = request.user
			notes.save()
			next_url = request.GET.get("next_url", '/')
			return redirect(next_url)
	else:
		form = NotesForm()
	
	return render(request, 'flashcards/components/create.html', {'forms': form})


@login_required(login_url='login')
def subject_create(request):
	if request.method == "POST":
		form = SubjectForm(request.POST, request.FILES)
		if form.is_valid():
			subjects = form.save(commit=False)
			subjects.creator = request.user
			subjects.save()
			
			if form.errors:
				return redirect('subject_create', messages.error)
			
			return redirect('subject', subjects.id)
	else:
		form = SubjectForm()
	
	return render(request, 'flashcards/important/subject_create.html', {"forms": form})


@login_required(login_url='login')
def create_topic(request, pk):
	subject = Subject.objects.get(id=pk)
	
	
	if request.method == "POST":
		form = TopicForm(request.POST)
		if form.is_valid():
			topic = form.save(commit=False)
			topic.subject = subject
			topic.creator = request.user
			topic.save()
			
			return redirect('subject', pk=subject.id)
	else:
		form = TopicForm()
	
	return render(request, 'flashcards/components/createTopic.html', {"forms": form})


def create_flashcard(request, subject_id, topic_id):
	
	notes = Notes.objects.filter(creator=request.user).order_by("-updated")
	to_do = Todo.objects.filter(creator=request.user).order_by("created")
	
	current_subject = Subject.objects.get(id = subject_id)
	current_topic = Topics.objects.get(id=topic_id, subject=current_subject)
	flashcard = FlashCard.objects.filter(creator=request.user, topic__subject=current_topic.subject,
	                                     topic=current_topic).order_by("-updated")
	if request.method == 'POST':
		form = FlashcardForm(request.POST)
		user = request.user

		if form.is_valid():
			flashcard = form.save(commit=False)
			flashcard.creator = user
			flashcard.topic = current_topic
			flashcard.save()
			# return redirect('flashcard', subject_id = current_subject.id, topic_id = current_topic.id, flashcard_id = flashcard.id)
			return redirect('create-flashcard', subject_id = current_subject.id, topic_id = current_topic.id)
	else:
		form = FlashcardForm()


	return render(request, 'flashcards/important/flashcard_create.html', {"forms": form, "flashcards": flashcard, "current_topic": current_topic,
	                                                                      "current_subject": current_subject, "CreateOrUpdate": "Create", "notes": notes,
	                                                                      "todo": to_do, "isUpdate": "false"})

#End Create Things######################################################################################################
#Update Things##########################################################################################################


@login_required(login_url='login')
def subject_update(request, subject_id):
	subject = get_object_or_404(Subject, id=subject_id)
	if request.method == 'POST':
		form = SubjectForm(request.POST, request.FILES, instance=subject)
		
		if form.is_valid():
			form.save()
			return redirect('subject', pk=subject_id)
	else:
		form = SubjectForm(instance=subject)
	
	return render(request, 'flashcards/important/subject_update.html', {"forms": form, "current_subject": subject})


@login_required(login_url='login')
def topic_update(request, subject_id, topic_id):
	current_subject = Subject.objects.get(id=subject_id, creator=request.user)
	current_topic = Topics.objects.get(id=topic_id, subject=current_subject)
	user = request.user
	
	
	if request.method == 'POST':
		# form = UpdateTopicForm(request.POST, request.user.id , instance=current_topic)
		form = TopicForm(request.POST, instance=current_topic)
		
		if form.is_valid():
			form.save(commit=False)
			form.subject_id = int(subject_id)
			form.save()
			return redirect('topic', subject_id=subject_id, topic_id=topic_id)
	else:
		form = TopicForm(instance=current_topic)
	
	return render(request, 'flashcards/important/topic_update.html', {"forms": form, "current_topic": topic})


@login_required(login_url='login')
def update_flashcard(request, subject_id, topic_id, flashcard_id):
	current_subject = Subject.objects.get(id = subject_id)
	current_topic = Topics.objects.get(id=topic_id, subject = current_subject)
	
	notes = Notes.objects.filter(creator=request.user).order_by("-updated")
	to_do = Todo.objects.filter(creator=request.user).order_by("created")
	flashcards = FlashCard.objects.filter(creator=request.user, topic__subject=current_topic.subject,
	                                     topic=current_topic).order_by("-updated")
		
	user = request.user
	
	current_flashcard = FlashCard.objects.get(id = flashcard_id)
	if current_flashcard.creator != user:
		return redirect('flashcard', current_subject, current_topic)
	
	if request.method == 'POST':
		form = FlashcardForm(request.POST, instance=current_flashcard)
		
		if form.is_valid():
			flashcard = form.save(commit=False)
			flashcard.creator = user
			flashcard.topic = current_topic
			flashcard.subject = current_subject
			flashcard.save()
			
			return redirect('create-flashcard', current_subject.id, current_topic.id)
	
	else:
		form = FlashcardForm(instance=current_flashcard)
		
		
	return render(request, 'flashcards/important/flashcard_create.html', {"forms": form, "CreateOrUpdate": "Update",
	                                                                      "isUpdate": "true", "current_flashcard": current_flashcard,
	                                                                      "current_subject": current_subject, "current_topic": current_topic,
	                                                                      "flashcards": flashcards, "notes": notes, "todo": to_do
	                                                                      })


#End Update Things######################################################################################################
#Delete Things##########################################################################################################
@login_required(login_url='login')
def delete_todo(request, pk):
	do = Todo.objects.get(id=pk)
	do.delete()
	return redirect(request.GET.get("next_url", '/'))


@login_required(login_url='login')
def delete_notes(request, pk):
	do = Notes.objects.get(id=pk)
	do.delete()
	
	return redirect(request.GET.get("next_url", '/'))


@login_required(login_url='login')
def delete_subject(request, subject_id):
	subject = get_object_or_404(Subject, id=subject_id)
	
	if subject.creator != request.user:
		return redirect('home')
	
	subject.delete()
	
	return redirect('home')


@login_required(login_url='login')
def delete_topic(request, pk):
	do = Topics.objects.get(id=pk)
	do.delete()
	
	return redirect(request, 'home')


@login_required(login_url='login')
def delete_flashcard(request, subject_id, topic_id, flashcard_id):
	current_subject = Subject.objects.get(id=subject_id)
	current_topic = Topics.objects.get(id=topic_id, subject=current_subject)
	
	do = FlashCard.objects.get(id=flashcard_id, topic=current_topic)
	do.delete()
	
	return redirect(request.GET.get('next_url', '/'))

#End Delete Things######################################################################################################
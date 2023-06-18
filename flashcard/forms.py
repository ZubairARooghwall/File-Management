from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

#Import all the models
from .models import User, Notes, FlashCard, Topics, Todo, Subject

class MyUserRegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['name', 'username', 'email', 'password1', 'password2', 'bio', 'avatar', 'prefer_dark_theme', 'education']
		
		# in form, you add enctype="multipart/form-data"
		# in views.py, form = MyUserRegistrationForm(..add request.FILES...)


class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['name', 'email', 'bio', 'education', 'prefer_dark_theme', 'avatar']
		exclude = ['score', 'is_staff', 'is_superuser', 'is_active']


class NotesForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		flashcard_choices = [('', '---')]
		flashcard_choices += list(FlashCard.objects.values_list('id', 'question'))
		self.fields['flashcard'].widget = forms.Select(choices=flashcard_choices)
		
		topic_choices = [('', '---')]
		topic_choices += list(Topics.objects.values_list('id', 'topic_name'))
		self.fields['topic'].widget = forms.Select(choices=topic_choices)
	class Meta:
		model = Notes
		fields = ['title', 'note', 'flashcard', 'topic']
		

class TodoForm(ModelForm):
		class Meta:
			model = Todo
			fields = ['task']
		

class SubjectForm(ModelForm):
	class Meta:
		model = Subject
		fields = ['subject_name', 'picture']
	
class TopicForm(ModelForm):
	class Meta:
		model = Topics
		fields = ['topic_name']
		
		
# class UpdateTopicForm(ModelForm):
#
# 	# This is for topic update where I can change the subject of the topic
# 	# subject = forms.ChoiceField(choices=[])
#
# 	# def __init__(self, user, *args, **kwargs):
# 	# 	super().__init__(*args, **kwargs)
# 		# self.fields['subject'].choices = [(subject.id, subject.subject_name) for subject in Subject.objects.filter(creator = user)]
#
# 	class Meta:
# 		model = Topics
# 		fields = ['topic_name']
from django.urls import path, include
from django.contrib import admin
from . import views


urlpatterns = [
	# Everything homepage
	path('', views.home, name="home"),
	path('settings', views.settings, name='settings'),
	path('statistics', views.statistics, name='statistics'),
	# this is for new users
	# path('home', views.newvisitor, name="NewVisitor"),
	
	# login and register
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutPage, name="logout"),
	
	# user management
	path('delete-account', views.delete_account, name="delete_account"),
	
	# todo
	path('create_todo', views.create_todo, name="create_todo"),
	path('delete_todo/<int:pk>', views.delete_todo, name="delete_todo"),
	
	# notes
	path('create-notes', views.create_notes, name="create_notes"),
	path('delete-notes/<int:pk>', views.delete_notes, name="delete_notes"),
	
	# subjects
	path('subject=<int:pk>', views.subject, name='subject'),
	path('subject-create', views.subject_create, name='create_subjects'),
	path('subject=<int:subject_id>/update', views.subject_update, name='update_subjects'),
	path('subject=<int:subject_id>/delete', views.delete_subject, name='delete_subject'),
	
	# topics
	path('subject=<int:subject_id>/topic=<int:topic_id>', views.topic, name='topic'),
	path('subject=<int:pk>/create_topic', views.create_topic, name='create_topic'),
	path('subject=<int:subject_id>/topic=<int:topic_id>/update', views.topic_update, name='update_topic'),
	
	# flashcards
	path('subject=<int:subject_id>/topic=<int:topic_id>/flashcard=<int:flashcard_id>', views.flashcard, name='flashcard'),
	path('subject=<int:subject_id>/topic=<int:topic_id>/create-flashcard', views.create_flashcard, name='create-flashcard'),
	path('subject=<int:subject_id>/topic=<int:topic_id>/flashcard=<int:flashcard_id>/update-flashcard', views.update_flashcard, name='update-flashcard'),
	path('subject=<int:subject_id>/topic=<int:topic_id>/flashcard=<int:flashcard_id>/delete-flashcard', views.delete_flashcard, name='delete-flashcard'),
	path('subject=<int:subject_id>/topic=<int:topic_id>/flashcard=<int:flashcard_id>/preview-flashcard', views.flashcard_preview, name='flashcard-preview'),
	path('flashcards/study', views.study_flashcards, name='flashcard-study'),
	path('update_flashcard_index/', views.update_flashcard_index, name='update_flashcard_index'),
	path('completed', views.completed_page, name='completed'),
	
	# social
	path('profiles', views.all_profiles, name='profiles'),
	path('profile/<str:username>', views.profile, name='profile'),
	# group
	path('group/<int:group_id>', views.group, name='group'),
	path('group/create', views.create_group, name='create-group'),
	
	#Search
	path('search', views.search, name='search'),
	
	# Files
	path('file/<int:file_id>',  views.view_file, name='view_file'),
	# Download file
	path('file/download/<int:file_id>', views.download_file, name='download_file'),
	# Create or Upload files
	path('file/upload', views.upload_file, name='upload_file'),
	
]

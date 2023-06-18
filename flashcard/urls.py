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
	path('subject=<int:pk>/topic<int:pk>/update', views.topic_update, name='update_topic')
]
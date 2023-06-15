from django.urls import path, include
from . import views

urlpatterns = [
	# Everything homepage
	path('', views.home, name="home"),
	path('settings', views.settings, name='settings'),
	path('statistics', views.statistics, name='statistics')
	,
	# this is for new users
	# path('home', views.newvisitor, name="NewVisitor"),
	
	# login and register
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutPage, name="logout"),
	
	# user management
	path('delete-account', views.delete_account, name="delete_account"),

]
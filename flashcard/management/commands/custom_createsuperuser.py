from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand


class Command(BaseCommand):
	help = "Create a superuser with name, username, email, and password"
	
	def add_arguments(self, parser):
		super().add_arguments(parser)
		parser.add_argument("--name", dest="name", default=None, help="Specifies the name for the superuser.")
		
	
	def handle(self, *args, **options):
		options['name'] = input("Name: ")
		options['username'] = input("Username: ")
		options['email'] = input("Email: ")
		super().handle(*args, **options)
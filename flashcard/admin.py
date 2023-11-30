from django.contrib import admin
from .models import User, Subject, Topics, FlashCard, Notes, Messages, Friendship, Group, Membership, GroupMessages, Todo, File, Permission, Activity_log, Tag, Notification


# Register your models here. The model will be recognized by the admin page
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Topics)
admin.site.register(FlashCard)
admin.site.register(Notes)
admin.site.register(Messages)
admin.site.register(Friendship)
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(GroupMessages)
admin.site.register(Todo)

# Newly added for file_management
admin.site.register(File)
admin.site.register(Permission)
admin.site.register(Activity_log)
admin.site.register(Tag)
admin.site.register(Notification)
# End registering models


from django.contrib import admin
from .models import User, Subject, Topics, FlashCard, Notes, Log, Messages, Friendship, Group, Membership, GroupMessages, Todo


# Register your models here. The model will be recognized by the admin page
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Topics)
admin.site.register(FlashCard)
admin.site.register(Notes)
admin.site.register(Log)
admin.site.register(Messages)
admin.site.register(Friendship)
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(GroupMessages)
admin.site.register(Todo)
# End registering models


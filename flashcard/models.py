from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models
from django.utils import timezone # for updating time


def get_default_avatar():
  return staticfiles_storage.url('image/avatar/avatar.png')


# Create your models here.
class User(AbstractUser):
  name = models.CharField(max_length=300, null=True, blank=False, unique=True)
  username = models.CharField(max_length=300, unique=True)
  email = models.EmailField(unique=True, blank=False)
  biography = models.TextField(null=True, blank=True)
  score = models.IntegerField(null=False, default=0, blank=False)
  class educations(models.TextChoices):
    Middle_School = "Middle_School"
    High_School = "High_School"
    College = "College"
    Graduate_School = "Graduate_School"
  # When adding values, User(...., education="MSC",...)
  education = models.CharField(max_length=20, choices=educations.choices, default=educations.College)
  avatar = models.ImageField(null=True, default=get_default_avatar, max_length=500)
  prefer_dark_theme = models.BooleanField(default=False, help_text="Do you prefer dark theme?")
  is_active = models.BooleanField(default=True, help_text="If the person is active, it is True")
  date_joined = models.DateTimeField(auto_now_add=True)
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

# New Project time
## Files table

class File(models.Model):
  file_name = models.CharField(max_length=300)
  file = models.FileField(upload_to="files", max_length=500)
  type = models.CharField(max_length=10)
  file_size = models.IntegerField(null=False, blank=False)
  upload_time = models.DateTimeField(auto_now_add=True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  description = models.TextField(max_length=1000)

class Permission(models.Model):
  file = models.ForeignKey(File, on_delete=models.CASCADE)
  to_user = models.ForeignKey(User, on_delete=models.CASCADE)
  creation_time = models.DateTimeField(auto_now_add=True)

class Activity_log(models.Model):
  activity = models.CharField(max_length=10)
  creation_time = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  file = models.ForeignKey(File, on_delete=models.CASCADE)

class Tag(models.Model):
  tag_name = models.CharField(primary_key=True, max_length=300)
  creation_time = models.DateTimeField(auto_now_add=True)
  
  class colors(models.TextChoices):
    RED = "RED"
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    GRAY = "GRAY"
    BLUE = "BLUE"
  
  color = models.CharField(max_length=20, choices=colors.choices, default=colors.BLUE)


class Notification(models.Model):
  to_user = models.ForeignKey(User, on_delete=models.CASCADE)
  notification_type = models.CharField(max_length=7)
  creation_time = models.DateTimeField(auto_now_add=True)
  content = models.CharField(max_length=255)
  isRead = models.BooleanField(default=False)


# New Project end

class Subject(models.Model):
  subject_name = models.CharField(max_length=255, null=False, blank=False)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  picture = models.ImageField(null=True, default="#", blank=True, upload_to="image/avatar", max_length=500) # Add a default image
  creator = models.ForeignKey(User, on_delete=models.CASCADE)


class Topics(models.Model):
  topic_name = models.CharField(max_length=300, null=False, blank=False)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=False)
  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def save(self, *args, **kwargs):
    self.subject.update = timezone.now()
    self.subject.save()
    super().save(*args, **kwargs)




class FlashCard(models.Model):
  creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="Who is the original creator of the flashcard. I will add more functionality where learners can 'fork' it like github repo and pull request the mistakes")
  question = models.TextField(max_length=500, null=False, blank=False)
  question_hint = models.CharField(max_length=30, blank=True, help_text="If you forget, it will appear after a certain while")
  answer = models.TextField(max_length=2000, blank=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  # score = models.IntegerField(default=0, help_text="How much score is gained by the card", editable=True, null=True)
  topic = models.ForeignKey(Topics, on_delete=models.SET_NULL, null=True)
  # lapses = models.IntegerField(help_text="How many times has the flashcard been reviewed", default=0, editable=True)
  # average = models.IntegerField(help_text="What is the average score of the flashcard. After every lapse, the score is added", null=True, default=0)
  is_hidden = models.BooleanField(default=False)
  
  def save(self, *args, **kwargs):
    self.topic.updated = timezone.now()
    self.topic.save()
    self.topic.subject.updated = timezone.now()
    self.topic.subject.save()
    super().save(*args, **kwargs)



class Notes(models.Model):
  title = models.CharField(max_length=3000, null=False, blank=False, default="")
  note = models.TextField(max_length=255, null=False, blank=False)
  flashcard = models.ForeignKey(FlashCard, null=True, on_delete=models.SET_NULL, blank=True)
  topic = models.ForeignKey(Topics, null=True, on_delete=models.SET_NULL, blank=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  creator = models.ForeignKey(User, on_delete=models.CASCADE)



# Whenever you review a flashcard, it is recorded there. Good for statistics
# flashcard = Flashcard.objects.get(id=1)
# # logs = flashcard.log_set.all() to get all the log instances of the flashcard
# class Log(models.Model):
#   flashcard = models.ForeignKey(FlashCard, on_delete=models.SET_NULL, null=True, related_name="logs") # you can use flashcard.logs.all() to access all the flashcards
#   reviewed_time = models.DateTimeField(auto_now_add=True)
#
#   choice_field = [
#     ("bad", "answered badly"),
#     ("meh", "answered badgood"),
#     ("good", "answered good"),
#     ("best", "answered best")
#   ]
#   action = models.CharField(max_length=10, null=False, blank=False, choices=choice_field)
#   user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#   result = models.BooleanField(help_text="Was is answered correctly")
#   duration = models.DurationField()
#   notes = models.ForeignKey(Notes, on_delete=models.CASCADE)


# If I wanted, I will do it
# class MindMaps(models.Model):


# user = User.objects.get(id=1)  # Assuming you have the custom user model
# sent_messages = user.sent_messages.all()
# received_messages = user.received_messages.all()
class Messages(models.Model):
  sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
  recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="receiver")
  is_read = models.BooleanField(default=False)
  message = models.TextField()
  created = models.DateTimeField(auto_now_add=True)
  reply = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="replyTo")
  
  def __str__(self):
    return f"{self.sender.name} sent {self.message} to {self.recipient.name}"


class Friendship(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_friendship")
  friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_friendship")
  created = models.DateTimeField(auto_now_add=True)
  is_accepted = models.BooleanField(default=False)
  custom_name = models.CharField(max_length=120, default=friend.name, null=True, blank=True)
  
  
  # def save(self, *args, **kwargs):
  #   self.friend = self.user
  #   super().save(*args, **kwargs)
  
  def __str__(self):
    return f"{self.user} - {self.friend}"




# Social

def get_default_group_avatar():
  return staticfiles_storage.url('images/related/group.jpeg')


class Group(models.Model):
  host = models.ForeignKey(User, on_delete=models.CASCADE)
  group_name = models.CharField(max_length=120, null=False, blank=False)
  description = models.TextField(null=True, blank=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  is_public = models.BooleanField(default=True)
  image = models.ImageField(null=True, default=get_default_group_avatar, max_length=500) # Add default image!
  members = models.ManyToManyField(User, through="Membership", related_name="members")
  last_message = models.OneToOneField(
    'GroupMessages',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='group_last_message'
  )
  def __str__(self):
    return self.group_name

class Membership(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  group = models.ForeignKey(Group, on_delete=models.CASCADE)
  date_joined = models.DateTimeField(auto_now_add=True)
  
  choices_field = [
    ("mod", "Moderator"),
    ("co", "Co-Host")
  ]
  
  role = models.CharField(max_length=120, null=True, choices=choices_field)
  
  def __str__(self):
    return f"{self.user} - {self.group}"

class GroupMessages(models.Model):
  group = models.ForeignKey(Group, on_delete=models.CASCADE)
  sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  message = models.CharField(max_length=300, null=False, blank=False, help_text="Message")
  created = models.DateTimeField(auto_now_add=True)
  reply = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="replyGroup")
  
  def __str__(self):
    return f"Message #{self.id} in {self.group} by {self.sender.name}"



#
# class CallLog(models.Model):

# class temporatyGroupForStudyingFlashCard or other thing


class Todo(models.Model):
  task = models.TextField(max_length=255, null=False, blank=False)
  created = models.DateTimeField(auto_now_add=True)
  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  
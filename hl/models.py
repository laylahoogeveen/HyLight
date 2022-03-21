from pickle import FALSE
from django.db import models
from django.contrib.auth.models import User
from django.forms import BooleanField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=40, blank=True)
    title = models.CharField(max_length=50, null=True)
    available = models.BooleanField(default=False)
    avatar = models.URLField(max_length=150, null=True, blank=True)
    current_studies = models.ManyToManyField("StudyProgramme", blank=True, related_name="user_current_studies")
    past_studies = models.ManyToManyField("StudyProgramme", blank=True, related_name="user_past_studies")
    skills = models.ManyToManyField("Skill", blank=True, related_name="user_skills")

    def __str__(self):
        return self.user.username

    @property
    def get_availability(self):
        if self.available == True:
            return "Available"
        else:
            return "Unavailable"

    @property
    def get_skills(self):
        return self.skills.all()

    @property
    def get_current_studies(self):
        return self.current_studies.all()

    @property
    def get_past_studies(self):
        return self.past_studies.all()

    @property
    def get_all_studies(self):
        return (self.past_studies.all() | self.current_studies.all()).distinct()

class Skill(models.Model):
    name = models.CharField(max_length=40, null=True)
    # subscribers = models.ManyToManyField(User, blank=True, related_name="skills_subscribers")   
    
    def __str__(self):
        return self.name

class StudyProgramme(models.Model):
    name = models.CharField(max_length=50, null=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name="skills_studies")
    level = models.PositiveSmallIntegerField(null=True)
    # subscribers = models.ManyToManyField(User, blank=True, related_name="study_subscribers")  

    def __str__(self):
        return self.name

    @property
    def get_skills(self):
        return self.skills.all()

class Notification(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='notification_user')
    question = models.ForeignKey('Question', null=True, on_delete=models.CASCADE, related_name='question_notification')
    comment = models.ForeignKey('Comment', null=True, on_delete=models.CASCADE, related_name='comment_notification')
    seen = models.BooleanField(blank=True, default=False)


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comment_user')
    description = models.TextField(max_length=500, blank=True)
    posted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
    
class Question(models.Model):
    PENDING = 0
    IN_PROGRESS = 1
    ANSWERED = 2
    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (IN_PROGRESS, 'in progress'),
        (ANSWERED, 'answered'),
    )

    ORANGE = "orange"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    PURPLE = "purple"

    LIGHT_CHOICES = (
        (ORANGE, '(255,165,0)'),
        (GREEN, '(0,255,0)'),
        (YELLOW, '(255,255,0)'),
        (BLUE, '(0,0,255)'),
        (PURPLE, '(128,0,128)'),
    )
    
    title = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='question_user')
    description = models.TextField(max_length=500, blank=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name="question_subscribers") 
    online = models.BooleanField(blank=True, default=False)
    status = models.IntegerField(null=True, choices=STATUS_CHOICES, default=PENDING)
    colour = models.CharField(max_length=20, null=True, choices=LIGHT_CHOICES)
    posted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    study = models.ManyToManyField(StudyProgramme, blank=True, related_name="question_study")
    skills = models.ManyToManyField(Skill, blank=True, related_name="question_skill")
    comments = models.ManyToManyField(Comment, blank=True, related_name="question_comment")

    def __str__(self):
        if self.title:
            return self.title
        else:
            return ""

    
    @property
    def get_all_comments(self):
        return self.comments.all()

    @property
    def get_location(self):
        if self.online == True:
            return "On campus"
        else:
            return "Online"

    @property
    def get_skills(self):
        return self.skills.all()

    @property
    def get_studies(self):
        return self.study.all()

#         ENDING = 0
# DONE = 1
# STATUS_CHOICES = (
#     (PENDING, 'Pending'),
#     (DONE, 'Done'),
# )
# Then you can do order.status = Order.DONE.
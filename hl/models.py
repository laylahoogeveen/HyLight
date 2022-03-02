from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=50, null=True)
    available = models.BooleanField(default=False)
    avatar = models.URLField(max_length=150, null=True)

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    # if created:
    #     Profile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

class Skill(models.Model):
    name = models.CharField(max_length=40, null=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name="skills_subscribers")   

    
class StudyProgramme(models.Model):
    name = models.CharField(max_length=40, null=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name="study_subscribers")  
    level = models.PositiveSmallIntegerField(null=True)

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comment_user')
    description = models.TextField(max_length=500, blank=True)
    posted = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

class Question(models.Model):
    title = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='question_user')
    description = models.TextField(max_length=500, blank=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name="question_subscribers") 
    posted = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    level = models.PositiveSmallIntegerField(null=True)
    study = models.ManyToManyField(StudyProgramme, blank=True, related_name="question_study")
    skills = models.ManyToManyField(Skill, blank=True, related_name="question_skill")
    comments = models.ManyToManyField(Comment, blank=True, related_name="question_comment")



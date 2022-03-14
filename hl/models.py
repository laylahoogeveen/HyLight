from django.db import models
from django.contrib.auth.models import User

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
    subscribers = models.ManyToManyField(User, blank=True, related_name="skills_subscribers")   
    
    def __str__(self):
        return self.name

class StudyProgramme(models.Model):
    name = models.CharField(max_length=50, null=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name="skills_studies")
    subscribers = models.ManyToManyField(User, blank=True, related_name="study_subscribers")  
    level = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.name

    @property
    def get_skills(self):
        return self.skills.all()

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comment_user')
    description = models.TextField(max_length=500, blank=True)
    posted = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.description
    
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

    def __str__(self):
        return self.title

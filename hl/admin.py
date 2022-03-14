from django.contrib import admin
from .models import Profile, Skill, StudyProgramme, Comment, Question

# Register your models here.
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(StudyProgramme)
admin.site.register(Comment)
admin.site.register(Question)
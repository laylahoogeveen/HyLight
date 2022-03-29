from django.contrib.auth.models import User
from django.db.models import Q
from .models import Question, Notification
import random
from time import time


def get_students():
    '''Make a list of students for mock up purposes'''
    student_list = []
    students = ['taylor13', 'victor84', 'horace65', 'toto', 'annechien', 'humberto']
    for u in User.objects.all():
        if u.username in students:
            student_list.append(u)

    return student_list


def create_comment(form, question_pk, user):
    '''Create comment for question'''

    question = Question.objects.get(pk=question_pk)
    comment_form = form.save(commit=False)
    comment_form.user = user
    comment_form.save()  
    question.comments.add(comment_form)

    # Change question status from pending to in progress
    change_status(user, question)
    question.save()
    make_comment_notification(comment_form, question)


def change_status(user, question):
    '''Change status from pending to in progress'''

    if user != question.user:
        question.status = Question.IN_PROGRESS

def study_to_skills(user):
    '''Add skills belonging to user's study programmes to their list of skills'''

    for study in user.profile.get_all_studies:
        for skill in study.get_skills:

            user.profile.skills.add(skill)

def remove_all_skills(user):
    '''Remove user's skills'''

    for skill in user.profile.get_skills:
        user.profile.skills.remove(skill)


def get_user_questions(user):
    '''Get all questions that are relevant for user'''

    user_skills = user.profile.get_skills
    user_studies = user.profile.get_all_studies
    questions = Question.objects.filter((Q(skills__in=user_skills) | Q(study__in=user_studies))).exclude(user=user).order_by('-posted')
   
    # Ensure list items are unique while preserving order
    questions = list(dict.fromkeys(questions))
    return questions

def get_user_questions_unanswered(user):
    '''Get all questions that are relevant for user'''

    user_skills = user.profile.get_skills
    user_studies = user.profile.get_all_studies
    questions = Question.objects.filter((Q(skills__in=user_skills) | Q(study__in=user_studies))).exclude(user=user).order_by('-posted')
    questions = questions.exclude(status=2)

    # Ensure list items are unique while preserving order
    questions = list(dict.fromkeys(questions))

    return questions

    
def dummy_text():
    '''Dummy text for chat, some workaround for template issues'''

    meet = "Let's meet after class. There are still some things I want to discuss with you"
    idea = "Any idea where I can find the documentation?"
    lmk = "Okay, let me know!"
    lol = "LOL"
    test ="Goede vraag... Geen idee eigenlijk. Misschien lukt het wel als je het op een totaal andere manier aanpakt"
    chat = ["Hi"] * 13
    thx = "Thank you so much for helping me out with all this."

    

    chat[5] = thx
    chat[9] = meet
    chat[4] = idea
    chat[3] = lmk
    chat[10] = lol
    chat[11] = test
    # hey = ["Hey there! Could you help me out with this assignment I'm working on?"] * 5
    # hey2 = ["Okay, see ya!"] * 5
    # tough = ["That's a tough one..."] * 5
    # wtf = ["I just got home actually"] * 5
    # let = ["I'll let you know ASAP"] * 5
    # chats = [*chat, *hey, *hey2, *tough, *wtf, *let, *thx]
    return chat

def get_unused():
    '''Get colours that are currently not being used'''

    options = Question.LIGHT_CHOICES
    new_options = []
    used_colours = Question.objects.values_list('colour', flat=True).exclude(status=2)

    for o in options:
        if o[0] not in used_colours:
            new_options.append(o)

    # If there are none left, pick random colour
    if len(new_options) == 0:
        return random.choice(options)
        
    return random.choice(new_options)


def make_question_notification(question):
    '''Create a notification for users subscribed tags of question'''

    users = []

    # Get subscribers for skills the question was tagged with
    for skill in question.get_skills:
        for u in skill.user_skills.all():
            users.append(u)
    
    # Get subscribers for study programmes the question was tagged with
    for study in question.get_studies:
        for u in study.user_current_studies.all():
            users.append(u)
        for u in study.user_past_studies.all():
            users.append(u)

    # Make list items unique and make sure the owner 
    # of the question receives no notification
    users = list(set(users))
    users = [x for x in users if x.user.pk != question.user.pk]

    for u in users:
        Notification.objects.create(user=u.user, question=question)


def make_comment_notification(comment, question):
    '''Create a notification for user that originally asked the question,
    when someone has commented on it.'''

    # No notification if user comments on own question
    if comment.user != question.user:
        Notification.objects.create(user=question.user, question=question, comment=comment)

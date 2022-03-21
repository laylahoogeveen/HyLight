from django.contrib.auth.models import User
from django.db.models import Q
from .models import Question, Notification
import datetime

def get_students():
    '''Make a list of students for mock up purposes'''
    student_list = []
    students = ['taylor13', 'victor84', 'horace65', 'toto', 'annechien', 'humberto']
    for u in User.objects.all():
        if u.username in students:
            student_list.append(u)

    return student_list

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
    questions = list(dict.fromkeys(questions))
    # questions = list(questions)
    return questions

    
def dummy_text():
    meet = "Let's meet after class. There are still some things I want to discuss with you"
    idea = "Any idea where I can find the documentation?"
    lmk = "Okay, let me know!"
    lol = "LOL"
    test ="Goede vraag... Geen idee eigenlijk. Misschien lukt het wel als je het op een totaal andere manier aanpakt"
    chat = ["Hey!"] * 41
    hey = ["Hey there! Could you help me out with this assignment I'm working on?"] * 5
    hey2 = ["Okay, see ya!"] * 5
    tough = ["That's a tough one..."] * 5
    wtf = ["I just got home actually"] * 5
    let = ["I'll let you know ASAP"] * 5
    thx = ["Thank you so much for helping me out with all this."] * 5

    chat[9] = meet
    chat[4] = idea
    chat[3] = lmk
    chat[10] = lol
    chat[11] = test
    chats = [*chat, *hey, *hey2, *tough, *wtf, *let, *thx]
    return chats

def get_unused():
    '''Get colours that are currently not being used'''
    options = Question.LIGHT_CHOICES
    new_options = []
    used_colours = Question.objects.values_list('colour', flat=True).exclude(status=2)

    for o in options:
        if o[0] not in used_colours:
            new_options.append(o)

    # if there are none left
    if len(new_options) == 0:
        return options
        
    return new_options


def make_question_notification(question):

    users = []
    for skill in question.get_skills:
        for u in skill.user_skills.all():
            users.append(u)
    
    for study in question.get_studies:
        for u in study.user_current_studies.all():
            users.append(u)
        for u in study.user_past_studies.all():
            users.append(u)

    users = list(set(users))
    users = [x for x in users if x.user.pk != question.user.pk]

    print (question.user)
    print ("all users")
    for u in users:
        print (u)

    for u in users:
        Notification.objects.create(user=u.user, question=question)


def make_comment_notification(comment, question):
    if comment.user != question.user:
        Notification.objects.create(user=question.user, question=question, comment=comment)
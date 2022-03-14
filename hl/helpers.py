from django.contrib.auth.models import User

def study_to_skills(user):
    '''Add skills belonging to user's study programmes to their list of skills'''

    for study in user.profile.get_all_studies:
        for skill in study.get_skills:

            user.profile.skills.add(skill)

def remove_all_skills(user):
    '''Remove user's skills'''
    for skill in user.profile.get_all_studies:
        print (skill)

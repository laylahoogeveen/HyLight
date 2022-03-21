from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Question, Notification
from .forms import RegisterForm1, RegisterForm2, RegisterForm3, ProfileForm, CommentForm, ChangeQuestionForm
from .helpers import study_to_skills, remove_all_skills, make_question_notification
from formtools.wizard.views import SessionWizardView

def register(request):
    """ Register user, first step with basic info """

    if request.method == "GET":

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            form = RegisterForm1(request.POST)
            return render(request, "hl/account/register.html", {"form": form})

    if request.method == "POST" or None:
        initial={'username': request.session.get('username', None)}
        form = RegisterForm1(request.POST or None, initial=initial)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            request.session['creating'] = True
            form.save()
            return HttpResponseRedirect(reverse('register_next'))
    
    return render(request, "hl/account/register.html", {"form": form})

def register_next(request):
    """ Register user, second step with study details """
    
    user_username = request.session['username']
    creating = request.session['creating']
    

    #  if session not valid
    if user_username == None:
        return HttpResponseRedirect(reverse('index'))
    
    user = User.objects.get(username=user_username)

    form = RegisterForm2(request.POST, initial={'user': user})
    if request.method == "GET":
        if creating != True:
        # if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            form = RegisterForm2(request.POST)
    
    if request.method == 'POST' or None:
        form = RegisterForm2(request.POST or None, initial={'user': user})
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile = form.save()

            # sign in user after most important info has been added
            login(request, user)
            # authenticate(request, username=user.username, password=user.password)

            #Add skills belonging to user's study programmes to user skills
            study_to_skills(user)
            request.session['creating'] = True

            return HttpResponseRedirect(reverse('register_last'))

    return render(request, "hl/account/register_next.html", {"form": form})


def register_last(request):
    """ Register user, last step: adding/removing skills """
    message = None
    if 'creating' in request.session:
        if request.session['creating'] == True:
            message = "Please select the skills you have. Based on your education, we have selected some skills for you. Feel free to remove them."

    form = RegisterForm3(request.POST, instance=request.user.profile)
    if request.method == 'POST':
        form = RegisterForm3(request.POST or None, instance=request.user.profile)
        if form.is_valid():
            remove_all_skills(request.user)
            form.save()
            request.session['creating'] = False
            if message == None:
                
                # this should be settings
                return HttpResponseRedirect(reverse('index'))
            return HttpResponseRedirect(reverse('register_success'))
    
    context = {
        "form": form,
        "message": message,
    }

    return render(request, "hl/account/register_next.html", context)

def register_success(request):
    return render(request, "hl/account/register_last.html")


def change_skills(request):
    """ Change user's skills """
   
    form = RegisterForm3(request.POST, instance=request.user.profile)
    if request.method == 'POST':
        form = RegisterForm3(request.POST or None, instance=request.user.profile)
        if form.is_valid():
            remove_all_skills(request.user)
            form.save()
                
            return HttpResponseRedirect(reverse('profile'))

    context = {
        "form": form,
    }

    return render(request, "hl/account/register_next.html", context)


def login_view(request):
    """ Log in user """

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "hl/account/login.html", {"message": 
             "Username and password do not match."})

    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
    
    return render(request, "hl/account/login.html")

@login_required
def logout_view(request):
    """ Log out user"""

    logout(request)
    return render(request, "hl/account/login.html", {"message": "Signed out."})


@login_required
def profile(request):
    """ Return user info """

    user = User.objects.filter(username=request.user).first()

    if request.method == 'POST' or None:
        form = ProfileForm(request.POST, instance = user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            print (profile.available)
            profile = form.save()
            return HttpResponseRedirect(reverse("profile"))

    form = ProfileForm(request.POST)
    context = {
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                "form": form,
                }

    return render(request, "hl/account/profile.html", context)


@login_required
def questions_by_you(request):
    """Return forum page with questions asked by user"""
    comment_form = CommentForm(request.POST)
    form2 = CommentForm(request.POST or None)
    change_question_form = ChangeQuestionForm(request.POST or None)
    
    if request.method == "POST" or None:

        if 'title' not in request.POST:
            if form2.is_valid():
                question_pk = request.POST['questionID']
                question = Question.objects.get(pk=question_pk)
                comment_form = form2.save(commit=False)
                comment_form.user = request.user
                comment_form.save()  
                question.comments.add(comment_form)
                question.status = Question.IN_PROGRESS
                question.save()
                return HttpResponseRedirect(reverse('questions_by_you'))
        else:
            if change_question_form.is_valid():
                question_pk = request.POST['question_change_ID']
                question = Question.objects.get(pk=question_pk)
                change_question_form = ChangeQuestionForm(request.POST, instance = question)
                change_question_form.save()
                return HttpResponseRedirect(reverse('questions_by_you'))

    context = {
        "comment_form": comment_form,
        "questions_by_you": Question.objects.filter(user=request.user),
        "1column": True,
        "change_question_form": change_question_form,
    }

    return render(request, "hl/account/your_questions.html", context)


@login_required
def notifications(request):
    """Show list of notifications"""

    questions = Notification.objects.filter(user=request.user, seen=False).exclude(comment__isnull=False)
    comments = Notification.objects.filter(user=request.user, seen=False).exclude(comment__isnull=True)
    num_results = len(questions) + len(comments)
    # past_questions = Notification.objects.filter(user=request.user, seen=True).exclude(comment__isnull=False)
    # past_comments = Notification.objects.filter(user=request.user, seen=True).exclude(comment__isnull=True),
    # num_past_results = len(past_questions) + len(past_comments)
    context = {
        "1column": True,
        "questions": questions,
        "comments": comments,
        # "past_questions": past_questions,
        # "past_comments": past_comments,
        "num_results": num_results,
        # "num_past_results": num_past_results,
    }

    return render(request, "hl/account/notifications.html", context)


def seen_notifications(request):
    """Show list of past notifications"""

    questions = Notification.objects.filter(user=request.user, seen=True).exclude(comment__isnull=False).order_by('-posted')
    comments = Notification.objects.filter(user=request.user, seen=True).exclude(comment__isnull=True).order_by('-posted')
    num_results = len(questions) + len(comments)

    context = {
        "1column": True,
        "questions": questions,
        "comments": comments,
        "num_results": num_results,
    }

    return render(request, "hl/account/notifications.html", context)
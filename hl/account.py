from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm1, RegisterForm2, RegisterForm3
from .helpers import study_to_skills, remove_all_skills
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

    context = {
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                }

    return render(request, "hl/account/profile.html", context)
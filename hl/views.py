from . import account
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm


def index(request):
    """Return index page"""
   
    if request.method == "POST" or None:
        form = QuestionForm(request.POST or None)
        if form.is_valid():
            form.save()
    
    form = QuestionForm(request.POST)
    context = {
        "form": form,
    }

    if request.user.is_authenticated:
        return render(request, "hl/index.html", context)


    return redirect('login')

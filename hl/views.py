from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from .models import Painting, Object, Baseline

def index(request):
    """Return index page"""
    
        
    return render(request, "hl/index.html")
from . import account
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, CommentForm, ChangeQuestionForm
from .helpers import get_user_questions, dummy_text, get_unused
from .models import Profile, Question
import random

def index(request):
    """Return index page"""

    questions = get_user_questions(request.user)
    colours = get_unused()
    colour = random.choice(colours)
   
    if request.method == "POST" or None:
        if 'title' in request.POST:
            form = QuestionForm(request.POST or None)
            if form.is_valid():
                formpje = form.save(commit=False)
                colour = request.POST['question_colour']
                formpje.colour = colour
                formpje.user = request.user
                formpje.save()
                return HttpResponseRedirect(reverse('index'))
        else:
            form2 = CommentForm(request.POST or None)
            if form2.is_valid():
                question_pk = request.POST['questionID']
                question = Question.objects.get(pk=question_pk)
                comment_form = form2.save(commit=False)
                comment_form.user = request.user
                comment_form.save()  
                question.comments.add(comment_form)
                question.status = Question.IN_PROGRESS
                question.save()
                return HttpResponseRedirect(reverse('index'))

            
    students_campus = User.objects.filter(profile__available=True).exclude(profile__location=None)
    users = User.objects.order_by('-date_joined')
    form = QuestionForm(request.POST)
    comment_form = CommentForm(request.POST)
    context = {
        "form": form,
        "comment_form": comment_form,
        "questions": questions[0:3],
        "students_campus": students_campus,
        "users": users[0:5],
        "chats": dummy_text(),
        "colour": colour[0],
        "rgb": colour[1],
    }

    if request.user.is_authenticated:
        return render(request, "hl/index.html", context)

    return redirect('login')

def forum(request):
    """Return forum page with all questions"""
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
                return HttpResponseRedirect(reverse('forum'))
        else:
            if change_question_form.is_valid():
                question_pk = request.POST['question_change_ID']
                question = Question.objects.get(pk=question_pk)
                change_question_form = ChangeQuestionForm(request.POST, instance = question)
                change_question_form.save()
                return HttpResponseRedirect(reverse('forum'))


    context = {
        "questions": Question.objects.order_by('posted'),
        "change_question_form": change_question_form,
        "comment_form": comment_form,
        "questions_by_you": Question.objects.filter(user=request.user)
    }

    return render(request, "hl/forum.html", context)

def questions_for_you(request):
    """Return forum page with all questions"""
    comment_form = CommentForm(request.POST)
    form2 = CommentForm(request.POST or None)
    if form2.is_valid():
        question_pk = request.POST['questionID']
        question = Question.objects.get(pk=question_pk)
        comment_form = form2.save(commit=False)
        comment_form.user = request.user
        comment_form.save()  
        question.comments.add(comment_form)
        question.status = Question.IN_PROGRESS
        question.save()
        return HttpResponseRedirect(reverse('index'))

    context = {
        "questions": get_user_questions(request.user),
        "comment_form": comment_form,
        "addition": "for you",
        "questions_for_you": True,
    }

    return render(request, "hl/forum.html", context)

def available_students(request):
    """Return forum page with all questions"""
    students_campus = User.objects.filter(profile__available=True).exclude(profile__location=None)


    context = {
        "students_campus": students_campus,
    }

    return render(request, "hl/available_students.html", context)
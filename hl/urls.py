
from django.contrib import admin
from django.urls import include, path
from . import views
from . import account
from .forms import RegisterForm1, RegisterForm2

urlpatterns = [
    path("", views.index, name="index"),
    path("forum", views.forum, name="forum"),
    path("available_students", views.available_students, name="available_students"),
    path("questions_for_you", views.questions_for_you, name="questions_for_you"),
    path("register", account.register, name="register"),
    path("register_next", account.register_next, name="register_next"),
    path("change_skills", account.change_skills, name="change_skills"),
    path("register_last", account.register_last, name="register_last"),
    path("register_success", account.register_success, name="register_success"),
    path("login", account.login_view, name="login"),
    path("logout", account.logout_view, name="logout"),
    path("profile", account.profile, name="profile"),

]


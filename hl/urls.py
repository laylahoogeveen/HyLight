
from django.contrib import admin
from django.urls import include, path
from . import views
# from . import account

urlpatterns = [
    path("", views.index, name="index"),


]


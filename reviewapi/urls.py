from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.resume_review, name="review"),
]

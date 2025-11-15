from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("quiz/start/", views.quiz_start, name="quiz_start"),
]

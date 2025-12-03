from django.urls import path
from . import views

urlpatterns = [
    
    path('pytanie/<int:pytanie_id>/',
         views.StatystykiPytaniaAPIView.as_view(),
         name="statystyki-pytania-szczegoly"),

     path('pytania/',
         views.StatystykiWszystkichPytanAPIView.as_view(),
         name="statystyki-wszystkich-pytan"),

    path('update/',
         views.StatystykiPytaniaEdytujAPIView.as_view(),
         name="statystyki-pytania-update"),

     path('kursy-dni/',
         views.KursyDniAPIView.as_view(), 
         name="statystyki-egzaminy=w-7-dni"),

     path('leaderboard/',
         views.LeaderboardAPIView.as_view(), 
         name="leaderboard"),
   
    
]
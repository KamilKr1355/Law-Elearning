from django.urls import path
from . import views

urlpatterns = [
    # Quiz
    path('quiz/start/', views.Start_quiz.as_view(), name="quiz"),
    path('quiz/sprawdz/', views.Sprawdz_quiz.as_view(), name='sprawdz-quiz'),

    # Zapisy
    path('moje-zapisy/', 
         views.MojeZapisaneArtykulyAPIView.as_view(), 
         name="moje-zapisy"),
    
    path('moje-zapisy/<int:artykul_id>/', 
         views.UsunZapisArtykuluAPIView.as_view(), 
         name="usun-zapis"),

     # Notatki
     path('moje-notatki/', 
         views.MojeNotatkiApiView.as_view(), 
         name="moje-notatki"),

     path('moje-notatki/<int:id>', 
         views.NotatkaSzczegolyApiView.as_view(), 
         name="notatka-szczegoly"),

     

]
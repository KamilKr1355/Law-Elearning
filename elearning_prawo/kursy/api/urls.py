from django.urls import path
from . import views

urlpatterns = [
    # Users
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/profile/', views.getUserProfile, name='profil-uzytkownika'),
    path('users/', views.getUsers, name='profil-uzytkownikow'),
    path('users/register/', views.registerUser, name='rejestruj'),

    # Kursy
    path('kursy/', views.KursyAPIview.as_view(), name="kursy-lista"),
    path('kursy/<int:id>/', views.KursyAPIview.as_view(), name='kurs-opis'),
    
    # Rozdziały 
    path('kursy/<int:kurs_id>/rozdzialy/', 
         views.RozdzialyListaAPIview.as_view(), 
         name="rozdzialy-lista"),
    path('kursy/rozdzialy/<int:id>/', 
         views.RozdzialSzczegolyAPIview.as_view(), 
         name="rozdzial-szczegoly"),
    
    # Artykuły 
    path('kursy/<int:id>/artykuly/', views.ArtykulyAPIview.as_view(), name="artykuly-lista"),
    path('kursy/artykuly/<int:id>/', views.ArtykulyAPIview.as_view(), name="artykul-szczegoly"),
    
    # Quiz
    path('quiz/start/', views.Start_quiz.as_view(), name="quiz"),
    path('quiz/sprawdz/', views.Sprawdz_quiz.as_view(), name='sprawdz-quiz'),
]

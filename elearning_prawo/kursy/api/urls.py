from django.urls import path
from . import views

urlpatterns = [
    path('users/login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/profile', views.getUserProfile, name='profil-uzytkownika'),
    path('users/', views.getUsers, name='profil-uzytkownikow'),
    path('users/register',views.registerUser,name='rejestruj'),

    path('kursy/', views.Kursy.as_view(), name="kursy-lista"),
    path('kursy/<int:id>/',views.Kurs.as_view(), name= 'kurs-opis'),
    path('artykuly/kurs/<str:nazwa_kursu>/', views.Artykuly.as_view(), name="artykuly-kurs"),
    path('artykuly/<int:id>/',views.Artykul.as_view(), name="artykul-opis"),
    path('quiz/start/',views.Start_quiz.as_view(), name="quiz"),
    path('quiz/sprawdz/',views.Sprawdz_quiz.as_view(),name = 'sprawdz-quiz'),
    

    #path('register/', views.register,name="login"),
    #path('login/', views.login,name="register"),
    #path('logout/', views.logout,name="logout"),

]
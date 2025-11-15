from django.urls import path
from . import views

urlpatterns = [
    path('users/login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('kursy/', views.kursy, name="kursy-lista"),
    path('kursy/<int:id>/',views.get_kurs, name= 'kurs-opis'),
    path('artykuly/kurs/<str:nazwa_kursu>/', views.get_artykuly, name="artykuly-kurs"),
    path('artykuly/<int:id>/',views.get_artykul, name="artykul-opis"),
    path('quiz/start/',views.start_quiz, name="quiz"),
    path('quiz/sprawdz/',views.sprawdz_quiz,name = 'sprawdz-quiz'),
    path('users/profile', views.getUserProfile, name='profil-uzytkownika'),
    path('users/', views.getUsers, name='profil-uzytkownikow'),
    path('users/register',views.registerUser,name='rejestruj')

    #path('register/', views.register,name="login"),
    #path('login/', views.login,name="register"),
    #path('logout/', views.logout,name="logout"),

]
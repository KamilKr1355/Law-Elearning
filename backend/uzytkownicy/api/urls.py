from django.urls import path
from . import views
# Users
urlpatterns = [

    path('', views.getUsers, name='profil-uzytkownikow'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.getUserProfile, name='profil-uzytkownika'),
    path('register/', views.registerUser, name='rejestruj'),
    path('<str:pk>/promote/', views.promoteToAdmin, name='user-promote'),
    path('<str:pk>/ban/', views.toggleUserBan, name='user-ban'),
    path('<str:pk>/delete/', views.deleteUser, name='user-delete'),
]
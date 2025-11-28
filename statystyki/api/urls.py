from django.urls import path
from . import views

urlpatterns = [
    
    path('statystyki/pytanie/<int:pytanie_id>/',
         views.StatystykiPytaniaAPIView.as_view(),
         name="statystyki-pytania-szczegoly"),
    path('statystyki/update/',
         views.StatystykiPytaniaAPIView.as_view(),
         name="statystyki-pytania-update"),
    
]
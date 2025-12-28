from django.urls import path
from . import views

urlpatterns = [
     # Kursy
     path('', views.KursyAPIView.as_view(), name="kursy-lista"),
     path('<int:id>/', views.KursySzczegolyAPIView.as_view(), name='kurs-opis'),
    
     # Rozdziały 
     path('<int:kurs_id>/rozdzialy/', 
         views.RozdzialyListaAPIView.as_view(), 
         name="rozdzialy-lista"),
     path('rozdzialy/<int:id>/', 
         views.RozdzialSzczegolyAPIView.as_view(), 
         name="rozdzial-szczegoly"),
       
     # Artykuły 
     path('<int:kurs_id>/artykuly/', views.ArtykulyAPIView.as_view(), name="artykuly-lista"),
     path('rozdzial/<int:rozdzial_id>/artykuly/', views.ArtykulyRozdzialAPIView.as_view(), name="artykuly-rozdzialu-lista"),
     path('artykuly/<int:id>/', views.ArtykulySzczegolyAPIView.as_view(), name="artykul-szczegoly"),
     path('artykuly2/<int:id>/', views.ArtykulyGetAPIView.as_view(), name="artykul-szczegoly"),
     path('artykul-dnia/<int:kurs_id>',views.ArtykulyDniaAPIView.as_view(), name="artykul dnia"),


     # Pytania
     path('pytania/', views.PytaniaAPIView.as_view(), name="pytania-lista"),
     path('pytania/zmien/<int:id>/', views.PytanieSzczegolyAPIView.as_view(), name="pytanie-zmiana"),
     path('pytania/artykul/<int:artykul_id>/', views.PytaniaArtykulAPIView.as_view(), name="pytania-po-artykule"),
    
     #odpowiedzi
     path('odpowiedzi/', views.OdpowiedziAPIView.as_view(), name="odpowiedzi-zmiana"),
     path('odpowiedz/<int:id>/', views.OdpowiedziSzczegolyAPIView.as_view(), name="odpowiedz-szczegoly"),
     path('odpowiedzi/pytanie/<int:pytanie_id>/', views.OdpowiedziPytaniaAPIView.as_view(), name="odpowiedzi-pytania"),
     
]

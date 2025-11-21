from django.urls import path
from . import views

urlpatterns = [
    # Kursy
    path('', views.KursyAPIview.as_view(), name="kursy-lista"),
    path('<int:id>/', views.KursyAPIview.as_view(), name='kurs-opis'),
    
    # Rozdziały 
    path('<int:kurs_id>/rozdzialy/', 
         views.RozdzialyListaAPIview.as_view(), 
         name="rozdzialy-lista"),
    path('rozdzialy/<int:id>/', 
         views.RozdzialSzczegolyAPIview.as_view(), 
         name="rozdzial-szczegoly"),
    
    # Artykuły 
    path('<int:id>/artykuly/', views.ArtykulyAPIview.as_view(), name="artykuly-lista"),
    path('artykuly/<int:id>/', views.ArtykulyAPIview.as_view(), name="artykul-szczegoly"),
    
]

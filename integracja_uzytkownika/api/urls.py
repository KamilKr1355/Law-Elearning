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
         views.ZarzadzajZapisArtykuluAPIView.as_view(), 
         name="usun-zapis"),

    # Notatki
    path('moje-notatki/', 
        views.MojeNotatkiApiView.as_view(), 
        name="moje-notatki"),

    path('moje-notatki/<int:id>/', 
        views.NotatkaSzczegolyApiView.as_view(), 
        name="notatka-szczegoly"),


    #Komentarze 
    path('artykuly/<int:artykul_id>/komentarze/', 
        views.KomentarzeAPIView.as_view(), 
        name="komentarze"),     
     
    path('komentarze/<int:id>/', 
        views.KomentarzSzczegolyAPIView.as_view(), 
        name="komentarze-szczegoly"),    

    #Egzamin 

    path('wyniki-egzaminu/', 
        views.WynikiEgzaminuAPIView.as_view(), 
        name="wyniki-egzaminu-lista"),

     path('wyniki-wszystkich-egzaminow/', 
        views.WynikiWszystkichEgzaminowAPIView.as_view(), 
        name="wyniki-wszystkich-egzaminow-lista"),
    
    path('wyniki-egzaminu/<int:id>/', 
         views.WynikEgzaminuSzczegolyAPIView.as_view(), 
         name="wynik-egzaminu-szczegoly"),
    
    path('wyniki-egzaminu/srednia/kurs/<int:kurs_id>/', 
         views.SredniaUzytkownikKursAPIView.as_view(), 
         name="srednia-uzytkownik-kurs"),
    
    path('wyniki-egzaminu/srednia-kursu/<int:kurs_id>/', 
         views.SredniaKursAPIView.as_view(), 
         name="srednia-kurs"),
     
    #OcenaArtykulu
    path('oceny/artykul/<int:artykul_id>/',
         views.OcenaArtykuluAPIView.as_view(),
         name="ocena-artykulu"),
    
    #ProgressPytan
    path('progress/kurs/<int:kurs_id>/', 
         views.ProgressPytanAPIView.as_view(), 
         name="progress-pytan-kurs"),

    #Tryb Nauki
     path('nauka/kurs/<int:kurs_id>/',
         views.TrybNaukiAPIView.as_view(),
         name="tryb-nauki-pytania"),
]
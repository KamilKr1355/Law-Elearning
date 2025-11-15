from django.contrib import admin
from .models import Kurs, Uzytkownik_kurs, Rozdzial, Artykul, Pytanie, Odpowiedz,ZapisArtykulu,Notatka,Komentarz,StatystykiPytania,ProgressPytan,WynikiEgzaminu,OcenaArtykulu

admin.site.register(Kurs)
admin.site.register(Uzytkownik_kurs)
admin.site.register(Rozdzial)
admin.site.register(Artykul)
admin.site.register(Pytanie)
admin.site.register(Odpowiedz)
admin.site.register(ZapisArtykulu)
admin.site.register(Notatka)
admin.site.register(Komentarz)
admin.site.register(StatystykiPytania)
admin.site.register(ProgressPytan)
admin.site.register(WynikiEgzaminu)
admin.site.register(OcenaArtykulu)

from django.contrib import admin
from .models import Kurs, Uzytkownik_kurs, Rozdzial, Artykul, Pytanie, Odpowiedz

admin.site.register(Kurs)
admin.site.register(Uzytkownik_kurs)
admin.site.register(Rozdzial)
admin.site.register(Artykul)
admin.site.register(Pytanie)
admin.site.register(Odpowiedz)
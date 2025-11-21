from django.contrib import admin
from .models import ZapisArtykulu,Notatka,Komentarz,StatystykiPytania,ProgressPytan,WynikiEgzaminu,OcenaArtykulu
# Register your models here.
admin.site.register(ZapisArtykulu)
admin.site.register(Notatka)
admin.site.register(Komentarz)
admin.site.register(StatystykiPytania)
admin.site.register(ProgressPytan)
admin.site.register(WynikiEgzaminu)
admin.site.register(OcenaArtykulu)
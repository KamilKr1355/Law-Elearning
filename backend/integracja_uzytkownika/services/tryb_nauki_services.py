from kursy.repositories.pytania_repository import PytaniaRepository
from integracja_uzytkownika.mappers.progress_pytan_mapper import map_postep_pytania_tryb_nauki_row
import random

class TrybNaukiService:

    def pobierz_pytania_dla_kursu(self, kurs_id, uzytkownik_id):

        rows = PytaniaRepository.pobierz_pytania_dla_trybu_nauki(kurs_id, uzytkownik_id)
        wszystkie_pytania = [map_postep_pytania_tryb_nauki_row(r) for r in rows]
        
        pytania_do_powtorzenia = [] 
        pytania_poprawne = []     

        for p in wszystkie_pytania:
            if p['status_uzytkownika'] in ['NW','OZ']:
                pytania_do_powtorzenia.append(p)
            else:
                pytania_poprawne.append(p)

        random.shuffle(pytania_do_powtorzenia)
        random.shuffle(pytania_poprawne)
        
        limit_poprawnych = min(10, len(pytania_poprawne))
        
        return pytania_do_powtorzenia + pytania_poprawne[:limit_poprawnych]


    def oznacz_jako_wyswietlone(self, pytanie_id, uzytkownik_id):
        return PytaniaRepository.oznacz_pytanie_jako_wyswietlone(uzytkownik_id, pytanie_id)
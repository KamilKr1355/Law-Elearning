from ..repositories.statystyki_pytania_repository import StatystykiPytaniaRepository
from ..mappers.statystyki_pytania_mapper import map_statystyki_pytania_row

class StatystykiPytaniaService:

    def pobierz_statystyki(self, pytanie_id):
        wiersz = StatystykiPytaniaRepository.pobierz_wg_pytania(pytanie_id)
        return map_statystyki_pytania_row(wiersz)

    def aktualizuj_statystyki(self, pytanie_id, is_correct, jest_pierwsza_proba):
        if not jest_pierwsza_proba:
            wiersz = StatystykiPytaniaRepository.pobierz_wg_pytania(pytanie_id)
            return map_statystyki_pytania_row(wiersz)
 
        zaktualizowany_id = StatystykiPytaniaRepository.aktualizuj_statystyki_repo(pytanie_id, is_correct)
        
        wiersz = StatystykiPytaniaRepository.pobierz_po_id(zaktualizowany_id)
        return map_statystyki_pytania_row(wiersz)
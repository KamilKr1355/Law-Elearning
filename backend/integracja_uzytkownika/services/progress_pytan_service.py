from ..repositories.progress_pytan_repository import ProgressPytanRepository
from ..mappers.progress_pytan_mapper import map_progress_pytan_row, map_progress_summary_row
from integracja_uzytkownika.models import ProgressPytan 

class ProgressPytanService:

    def pobierz_postep_wg_kursu(self, uzytkownik_id, kurs_id):
        progress_rows = ProgressPytanRepository.pobierz_postep_dla_uzytkownika_kurs(uzytkownik_id, kurs_id)
        progress_list = [map_progress_pytan_row(r) for r in progress_rows]
        
        summary_row = ProgressPytanRepository.pobierz_podsumowanie_dla_kursu(uzytkownik_id, kurs_id)
        summary = map_progress_summary_row(summary_row)
        
        return progress_list, summary

    def sprawdz_czy_odpowiedziano(self, uzytkownik_id, pytanie_id):
        status = ProgressPytanRepository.pobierz_status_uzytkownika(uzytkownik_id, pytanie_id)
        return status in ['OP','OZ']

    def aktualizuj_postep(self, uzytkownik_id, pytanie_id, state):
        if state == "OP":
            status = ProgressPytan.Status.ODP_POPR 
        elif state == "OZ":
            status = ProgressPytan.Status.ODP_ZLA
        elif state == "W":
            status = ProgressPytan.Status.WYSWIETLONE
        elif state == "NW":
            status = ProgressPytan.Status.NIEWYSWIETLONE

        zaktualizowany_id = ProgressPytanRepository.utworz_lub_aktualizuj(uzytkownik_id, pytanie_id, status)
        
        wiersz = ProgressPytanRepository.pobierz_po_id(zaktualizowany_id)
        return map_progress_pytan_row(wiersz)
        
    def oznacz_jako_wyswietlone(self, pytanie_id, uzytkownik_id):
        status = ProgressPytan.Status.WYSWIETLONE
        
        zaktualizowany_id = ProgressPytanRepository.utworz_lub_aktualizuj(uzytkownik_id, pytanie_id, status)
        
        wiersz = ProgressPytanRepository.pobierz_po_id(zaktualizowany_id)
        return map_progress_pytan_row(wiersz)
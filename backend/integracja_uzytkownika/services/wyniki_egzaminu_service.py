# integracja_uzytkownika/services/wynik_egzaminu_service.py
from ..repositories.wyniki_egzaminu_repository import WynikiEgzaminuRepository
from ..mappers.wynik_egzaminu_mapper import (
    map_wyniki_row, 
    map_average_uzytkownik_kurs_row, 
    map_average_kurs_row
)

class WynikEgzaminuService:

    def get_by_id(self, id):
        row = WynikiEgzaminuRepository.get_by_id(id)
        return map_wyniki_row(row) if row else None

    def get_by_uzytkownik(self, uzytkownik_id):
        rows = WynikiEgzaminuRepository.get_by_uzytkownik(uzytkownik_id)
        return [map_wyniki_row(r) for r in rows]
    
    def get_by_uzytkownik_and_kurs(self, uzytkownik_id, kurs_id):
        rows = WynikiEgzaminuRepository.get_by_uzytkownik_and_kurs(uzytkownik_id, kurs_id)
        return [map_wyniki_row(r) for r in rows]
    
    def get_average_uzytkownik_kurs_grade(self, uzytkownik_id, kurs_id):
        row = WynikiEgzaminuRepository.get_average_uzytkownik_kurs_grade(uzytkownik_id, kurs_id)
        return map_average_uzytkownik_kurs_row(row) if row else None

    def get_average_kurs_grade(self, kurs_id):
        row = WynikiEgzaminuRepository.get_average_kurs_grade(kurs_id)
        return map_average_kurs_row(row) if row else None
    
    def insert_wynik(self, wynik, kurs_id, uzytkownik_id):
        row = WynikiEgzaminuRepository.insert_wynik(wynik, kurs_id, uzytkownik_id)
        return map_wyniki_row(row) if row else None
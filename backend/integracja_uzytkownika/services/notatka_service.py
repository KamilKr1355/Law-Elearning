from ..repositories.notatka_repository import NotatkaRepository
from ..mappers.notatka_mapper import map_notatka_row,map_notatka_row2

class NotatkaService:

    def get_by_uzytkownik_and_artykul(self,uzytkownik_id,artykul_id):
        row = NotatkaRepository.get_by_uzytkownik_and_artykul(uzytkownik_id,artykul_id)
        return [map_notatka_row(r) for r in row]
    
    def get_by_uzytkownik_and_kurs(self,uzytkownik_id,kurs_id):
        row = NotatkaRepository.get_by_uzytkownik_and_kurs(uzytkownik_id,kurs_id)
        return [map_notatka_row2(r) for r in row]
    
    def get_by_uzytkownik(self,uzytkownik_id):
        row = NotatkaRepository.get_by_uzytkownik(uzytkownik_id)
        return [map_notatka_row(r) for r in row]
    
    def get_by_id(self,id):
        row = NotatkaRepository.get_by_id(id)
        return map_notatka_row(row) if row else None

    def create(self,tresc,uzytkownik_id,artykul_id):
        new_id = NotatkaRepository.insert(tresc,uzytkownik_id,artykul_id)
        row  = NotatkaRepository.get_by_id(new_id)

        return map_notatka_row(row) if row else None
    
    def update(self,id,tresc,uzytkownik_id):
        
        updated_id = NotatkaRepository.update(id,tresc,uzytkownik_id)

        if not updated_id:
            return None
        
        row = NotatkaRepository.get_by_id(id)
        return map_notatka_row(row) if row else None
    
    def delete(self,id,uzytkownik_id):

        deleted_id = NotatkaRepository.delete(id,uzytkownik_id)
        
        return bool(deleted_id)
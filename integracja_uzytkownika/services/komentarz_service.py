from ..repositories.komentarz_repository import KomentarzRepository
from ..mappers.komentarz_mapper import map_komentarz_row

class KomentarzService:

    def get_by_artykul_and_uzytkownik(self,artykul_id,uzytkownik_id):

        rows = KomentarzRepository.get_by_artykul_and_uzytkownik(artykul_id,uzytkownik_id)
        return [map_komentarz_row(r) for r in rows]
    
    def get_by_artykul(self,artykul_id):

        rows = KomentarzRepository.get_by_artykul(artykul_id)
        return [map_komentarz_row(r) for r in rows]
    
    def get_by_id(self,id):

        row = KomentarzRepository.get_by_id(id)
        return map_komentarz_row(row) 

    def create(self,tresc,artykul_id,uzytkownik_id):

        new_id = KomentarzRepository.insert(tresc,artykul_id,uzytkownik_id)
        row = KomentarzRepository.get_by_id(new_id)

        return map_komentarz_row(row) if row else None
    
    def update(self,id,tresc,uzytkownik_id):

        updated = KomentarzRepository.update(id,tresc,uzytkownik_id)
        row = KomentarzRepository.get_by_id(int(id))

        return map_komentarz_row(row) if row else None
    
    def delete(self,id,uzytkownik_id,isAdmin=False):

        if not isAdmin:
            deleted = KomentarzRepository.delete(id,uzytkownik_id)

            return bool(deleted)
        
        return bool(KomentarzRepository.delete_admin(id))

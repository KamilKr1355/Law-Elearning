from ..repositories.zapis_repository import ZapisRepository
from ..mappers.zapis_mapper import map_zapis_row

class ZapisService:

    def list_all(self, uzytkownik_id):
        rows = ZapisRepository.get_zapisane_by_uzytkownik_id(uzytkownik_id)
        return [map_zapis_row(r) for r in rows]
    
    def delete(self, uzytkownik_id, artykul_id):
        deleted_id = ZapisRepository.delete(uzytkownik_id, artykul_id)
        return deleted_id is not None
    
    def create(self, uzytkownik_id, artykul_id):
        exists = ZapisRepository.check_exists(uzytkownik_id, artykul_id)
        if exists:
            return None  
        
        new_id = ZapisRepository.create(uzytkownik_id, artykul_id)
        row = ZapisRepository.get_by_id(new_id)
        return map_zapis_row(row) if row else None
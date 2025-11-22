from kursy.repositories.odpowiedzi_repository import OdpowiedziRepository
from kursy.mappers.odpowiedzi_mapper import map_odpowiedz_row

class OdpowiedziService:

    def get(self,id):
        row = OdpowiedziRepository.get_by_id(id)
        return map_odpowiedz_row(row) if row else None
    
    def get_pytanie_id(self, pytanie_id):
        rows = OdpowiedziRepository.get_all_by_pytanie_id(pytanie_id)
        return [map_odpowiedz_row(r) for r in rows]

    def create(self,tresc,poprawna,pytanie_id):
        new_id = OdpowiedziRepository.insert(tresc,poprawna,pytanie_id)
        return {"id": new_id, "tresc": tresc,"poprawna":poprawna,"pytanie_id":pytanie_id}
    
    def update(self, id,tresc,poprawna,pytanie_id):
        updated = OdpowiedziRepository.update(id, tresc,poprawna,pytanie_id)
        if not updated:
            return None
        return {"id": id, "tresc": tresc,"poprawna":poprawna,"pytanie_id":pytanie_id}
    
    def delete(self, id):
        deleted = OdpowiedziRepository.delete(id)
        return bool(deleted)

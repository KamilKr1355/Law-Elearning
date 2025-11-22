from kursy.repositories.pytania_repository import PytaniaRepository
from kursy.mappers.pytania_mapper import map_pytanie_row

class PytaniaService:

    def get(self,id):
        row = PytaniaRepository.get_by_id(id)
        return map_pytanie_row(row)

    def list_all(self):
        rows = PytaniaRepository.get_all_pytania_odpowiedz()
        return [map_pytanie_row(r) for r in rows]

    def get_artykul_id(self, artykul_id):
        rows = PytaniaRepository.get_by_artykul_id(artykul_id)
        return [map_pytanie_row(r) for r in rows]

    def create(self, tresc,artykul_id):
        new_id = PytaniaRepository.insert(tresc,artykul_id)
        return {"id": new_id, "tresc": tresc,"artykul_id":artykul_id}

    def update(self, id, tresc,artykul_id):
        updated = PytaniaRepository.update(id, tresc,artykul_id)
        if not updated:
            return None
        return {"id": updated, "tresc": tresc,"artykul_id":artykul_id}

    def delete(self, id):
        deleted = PytaniaRepository.delete(id)
        return bool(deleted)

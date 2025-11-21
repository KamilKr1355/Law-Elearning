from kursy.repositories.rozdzial_repository import RozdzialRepository
from kursy.mappers.rozdzial_mapper import map_rozdzial_row

class RozdzialService:

    def list_by_kurs(self, kurs_id):
        rows = RozdzialRepository.get_all_for_kurs(kurs_id)
        return [map_rozdzial_row(r) for r in rows]

    def get_one(self, id):
        row = RozdzialRepository.get_by_id(id)
        return map_rozdzial_row(row) if row else None

    def create(self, nazwa_rozdzialu, kurs_id):
        new_id = RozdzialRepository.insert(nazwa_rozdzialu, kurs_id)
        return {
            "id": new_id,
            "nazwa_rozdzialu": nazwa_rozdzialu,
            "kurs_id": kurs_id
        }

    def update(self, id, nazwa_rozdzialu, kurs_id):
        updated = RozdzialRepository.update(id, nazwa_rozdzialu, kurs_id)
        if not updated:
            return None
        return {
            "id": id,
            "nazwa_rozdzialu": nazwa_rozdzialu,
            "kurs_id": kurs_id
        }

    def delete(self, id):
        deleted = RozdzialRepository.delete(id)
        return bool(deleted)

from kursy.repositories.kurs_repository import KursRepository
from kursy.mappers.kurs_mapper import map_kurs_row

class KursService:

    def list_all(self):
        rows = KursRepository.get_all()
        return [map_kurs_row(r) for r in rows]

    def get_one(self, id):
        row = KursRepository.get_by_id(id)
        return map_kurs_row(row) if row else None

    def create(self, nazwa_kursu):
        new_id = KursRepository.insert(nazwa_kursu)
        return {"id": new_id, "nazwa_kursu": nazwa_kursu}

    def update(self, id, nazwa_kursu):
        updated = KursRepository.update(id, nazwa_kursu)
        if not updated:
            return None
        return {"id": id, "nazwa_kursu": nazwa_kursu}

    def delete(self, id):
        deleted = KursRepository.delete(id)
        return bool(deleted)

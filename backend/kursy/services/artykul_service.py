from kursy.repositories.artykul_repository import ArtykulRepository
from kursy.mappers.artykul_mapper import map_artykul_row

class ArtykulService:

    def list_all(self):
        rows = ArtykulRepository.get_all()
        return [map_artykul_row(r) for r in rows]

    def get_one(self, id):
        row = ArtykulRepository.get_by_id(id)
        return map_artykul_row(row) if row else None

    def create(self, tresc,tytul,nr_artykulu,rozdzial_id):
        new_id = ArtykulRepository.insert(tresc,tytul,nr_artykulu,rozdzial_id)
        return {"tresc":tresc,"tytul":tytul,"nr_artykulu":nr_artykulu,"rozdzial_id":rozdzial_id}

    def update(self,tresc,tytul,nr_artykulu,rozdzial_id,id):
        updated = ArtykulRepository.update(tresc,tytul,nr_artykulu,rozdzial_id,id)
        if not updated:
            return None
        return {"tresc":tresc,"tytul":tytul,"nr_artykulu":nr_artykulu,"rozdzial_id":rozdzial_id}

    def delete(self, id):
        deleted = ArtykulRepository.delete(id)
        return bool(deleted)

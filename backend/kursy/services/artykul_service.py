from kursy.repositories.artykul_repository import ArtykulRepository
from kursy.mappers.artykul_mapper import map_artykul_row
from kursy.mappers.artykul_mapper import map_artykul_row2
from kursy.mappers.artykul_mapper import map_artykul_row3

class ArtykulService:

    def list_all(self,kurs_id):
        rows = ArtykulRepository.get_all(kurs_id)
        return [map_artykul_row3(r) for r in rows]

    def get_one(self, artykul_id):
        row = ArtykulRepository.get_by_id(artykul_id)
        return map_artykul_row(row) if row else None

    def get_artykul_dnia(self, kurs_id):
        row = ArtykulRepository.get_artykul_dnia(kurs_id)
        return map_artykul_row3(row) if row else None
    
    def get_one_with_title(self, artykul_id):
        row = ArtykulRepository.get_by_id2(artykul_id)
        return map_artykul_row3(row) if row else None

    def get_by_rozdzial(self, rozdzial_id):
        rows = ArtykulRepository.get_by_rozdzial_id(rozdzial_id)
        return [map_artykul_row2(r) for r in rows] if rows else []

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

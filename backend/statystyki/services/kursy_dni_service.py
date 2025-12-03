from ..repositories.kursy_dni_repositories import KursyDniRepository
from ..mappers.kursy_dni_mapper import map_kurs_dni

class KursyDniService:

    def pobierz_statystyki(self):
        rows =KursyDniRepository.get_all()
        return [map_kurs_dni(row) for row in rows]
    
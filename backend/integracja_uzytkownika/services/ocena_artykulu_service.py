from ..repositories.ocena_artykulu_repository import OcenaArtykuluRepository
from ..mappers.ocena_artykulu_mapper import map_ocena_artykulu_row, map_srednia_ocena_row

class OcenaArtykuluService:

    def pobierz_srednia_ocene(self, artykul_id):
        wiersz = OcenaArtykuluRepository.getOcenaArtykulu(artykul_id)
        return map_srednia_ocena_row(wiersz)

    def pobierz_ocene_uzytkownika(self, artykul_id, uzytkownik_id):
        wiersz = OcenaArtykuluRepository.getOcenaUzytkownika(artykul_id, uzytkownik_id)
        return map_ocena_artykulu_row(wiersz)

    def utworz_lub_aktualizuj_ocene(self, artykul_id, ocena, uzytkownik_id):
        istniejaca_ocena = OcenaArtykuluRepository.getOcenaUzytkownika(artykul_id, uzytkownik_id)

        if istniejaca_ocena:
            zaktualizowany_id = OcenaArtykuluRepository.update(artykul_id, ocena, uzytkownik_id)
        else:
            zaktualizowany_id = OcenaArtykuluRepository.insertOcena(artykul_id, ocena, uzytkownik_id)

        if zaktualizowany_id:
            wiersz = OcenaArtykuluRepository.get_by_id(zaktualizowany_id)
            return map_ocena_artykulu_row(wiersz)
        
        return None

    def usun_ocene(self, artykul_id, uzytkownik_id):
        usuniete_id = OcenaArtykuluRepository.delete(artykul_id, uzytkownik_id)
        return usuniete_id is not None
import requests
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django.db import connection


class Command(BaseCommand):
    help = 'Scrapuje kursy, rozdziały i artykuły z zewnętrznej strony i zapisuje je do bazy danych'

    def handle(self, *args, **kwargs):
        self.czysc_tabele()
        self.wstaw_kursy()
        self.scrapuj_rozdzialy()
        self.scrapuj_artykuly()
        self.stdout.write(self.style.SUCCESS('Poprawnie wyscrapowano i zapisano dane do bazy danych.'))


    def wstaw_kursy(self):
        kursy = ["Kodeks Karny", "Kodeks Cywilny"]
        with connection.cursor() as cursor:
            for kurs in kursy:
                cursor.execute("""
                    INSERT INTO kursy_kurs (nazwa_kursu)
                    VALUES (%s);
                """, [kurs])
        self.stdout.write(self.style.SUCCESS("Dodano kursy (SQL)"))


    def scrapuj_rozdzialy(self):
        url = "https://arslege.pl/kodeks-karny/k1/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM kursy_kurs WHERE nazwa_kursu = %s;", ["Kodeks Karny"])
            kurs_id = cursor.fetchone()[0]

            for element in soup.find_all("h2"):
                nazwa_rozdzialu = element.get_text()

                cursor.execute("""
                    INSERT INTO kursy_rozdzial (kurs_id, nazwa_rozdzialu)
                    VALUES (%s, %s);
                """, [kurs_id, nazwa_rozdzialu])

        self.stdout.write(self.style.SUCCESS("Dodano rozdziały (SQL)"))


    def scrapuj_artykuly(self):
        url = "https://arslege.pl/kodeks-karny/k1/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nazwa_rozdzialu FROM kursy_rozdzial;")
            rozdzialy_map = {name: id for id, name in cursor.fetchall()}

            obecny_rozdzial_id = None

            for element in soup.find_all(["h2", "article"]):
                if element.name == "h2":
                    nazwa = element.get_text()
                    obecny_rozdzial_id = rozdzialy_map.get(nazwa, None)
                    continue

                if element.name == "article" and "art_box" in element.get("class", []):
                    tytul_text = element.find("h3", class_="art_indeks").get_text()
                    tresc = element.find("div", class_="art_tresc").get_text()
                    if not tresc:
                        tresc = None

                    nr_artykulu = tytul_text.split(" ")[1].strip(".")
                    tytul = " ".join(tytul_text.split(" ")[2:])

                    cursor.execute("""
                        INSERT INTO kursy_artykul (rozdzial_id, tresc, tytul, nr_artykulu)
                        VALUES (%s, %s, %s, %s);
                    """, [obecny_rozdzial_id, tresc, tytul, nr_artykulu])


            cursor.execute(r"""
                UPDATE kursy_artykul
                SET tytul = 'Słowniczek'
                WHERE tytul is NULL 
                or TRIM(tytul) = '' 
                or LENGTH(regexp_replace(tytul, '\s','', 'g')) = 0;
            """)

            cursor.execute(r"""
                DELETE FROM kursy_artykul 
                WHERE tresc IS NULL
                OR LENGTH(TRIM(tresc)) = 0
                OR LENGTH(regexp_replace(tresc, '\s','', 'g')) = 0;
                """)
            

        self.stdout.write(self.style.SUCCESS("Dodano artykuły (SQL)"))


    def czysc_tabele(self):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM statystyki_statystykipytania;")
            cursor.execute("DELETE FROM integracja_uzytkownika_progresspytan;")
            cursor.execute("DELETE FROM kursy_odpowiedz;")
            cursor.execute("DELETE FROM kursy_pytanie;")
            cursor.execute("DELETE FROM kursy_artykul;")
            cursor.execute("DELETE FROM kursy_rozdzial;")
            cursor.execute("DELETE FROM kursy_uzytkownik_kurs;")
            cursor.execute("DELETE FROM kursy_kurs;")

            cursor.execute("ALTER SEQUENCE kursy_kurs_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE kursy_rozdzial_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE kursy_artykul_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE kursy_uzytkownik_kurs_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE kursy_pytanie_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE kursy_odpowiedz_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE statystyki_statystykipytania_id_seq RESTART WITH 1;")
            

        self.stdout.write(self.style.WARNING("Tabele wyczyszczone i ID zresetowane (SQL)"))

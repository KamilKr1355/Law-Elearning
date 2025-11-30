from django.db import connection

class PytaniaRepository:

    @staticmethod
    def get_by_id(id):
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id,tresc, artykul_id
             FROM kursy_pytanie WHERE id=%s;""",[id])
            return cursor.fetchone()

    @staticmethod
    def get_all_pytania_odpowiedz():
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id,tresc, artykul_id
             FROM kursy_pytanie;""")
            return cursor.fetchall()

    @staticmethod
    def get_by_artykul_id(artykul_id):
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id,tresc, artykul_id
             FROM kursy_pytanie
                           WHERE artykul_id=%s;""",[artykul_id])
            return cursor.fetchall()

    @staticmethod
    def insert(tresc,artykul_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO kursy_pytanie (tresc,artykul_id)
                VALUES (%s,%s)
                RETURNING id;
            """, [tresc,artykul_id])
            return cursor.fetchone()[0]

    @staticmethod
    def update(id, tresc,artykul_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE kursy_pytanie
                SET tresc=%s,
                           artykul_id=%s
                WHERE id=%s
                RETURNING id;
            """, [tresc,artykul_id, id])
            return cursor.fetchone()[0]

    @staticmethod
    def delete(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM kursy_pytanie
                WHERE id=%s
                RETURNING id;
            """, [id])
            return cursor.fetchone()

    @staticmethod
    def pobierz_pytania_dla_trybu_nauki(kurs_id, uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    p.id AS pytanie_id,
                    p.tresc AS tresc_pytania,
                    COALESCE(pp.status, 'NW') AS status_uzytkownika 
                FROM 
                    kursy_pytanie p
                JOIN 
                    kursy_artykul a ON p.artykul_id = a.id
                JOIN
                    kursy_rozdzial r ON a.rozdzial_id = r.id
                LEFT JOIN 
                    integracja_uzytkownika_progresspytan pp 
                    ON p.id = pp.pytanie_id AND pp.uzytkownik_id = %s
                WHERE 
                    r.kurs_id = %s;
            """, [uzytkownik_id, kurs_id])
            return cursor.fetchall()
            
    @staticmethod
    def oznacz_pytanie_jako_wyswietlone(uzytkownik_id, pytanie_id, status_wyswietlone='W'):
        with connection.cursor() as cursor:

            cursor.execute("""
                UPDATE integracja_uzytkownika_progresspytan
                SET status = %s, data_aktualizacji = NOW()
                WHERE uzytkownik_id = %s AND pytanie_id = %s
                RETURNING id;
            """, [status_wyswietlone, uzytkownik_id, pytanie_id])
            
            result = cursor.fetchone()
            
            if result:
                return result[0] 

            cursor.execute("""
                INSERT INTO integracja_uzytkownika_progresspytan 
                (uzytkownik_id, pytanie_id, status, data_aktualizacji)
                VALUES (%s, %s, %s, NOW())
                RETURNING id;
            """, [uzytkownik_id, pytanie_id, status_wyswietlone])
            return cursor.fetchone()[0]
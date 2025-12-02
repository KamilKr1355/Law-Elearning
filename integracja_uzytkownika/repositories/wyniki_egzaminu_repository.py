from django.db import connection

class WynikiEgzaminuRepository:

    @staticmethod
    def get_by_uzytkownik(uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, data_zapisu, wynik, kurs_id, uzytkownik_id
                FROM integracja_uzytkownika_wynikiegzaminu
                WHERE uzytkownik_id = %s
                ORDER BY data_zapisu DESC;
            """, [uzytkownik_id])
            return cursor.fetchall()
        
    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, data_zapisu, wynik, kurs_id, uzytkownik_id
                FROM integracja_uzytkownika_wynikiegzaminu
                ORDER BY data_zapisu DESC;
            """)
            return cursor.fetchall()
        
    def get_all_by_kurs(kurs_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, data_zapisu, wynik, kurs_id, uzytkownik_id
                FROM integracja_uzytkownika_wynikiegzaminu
                WHERE kurs_id = %s
                ORDER BY data_zapisu DESC;
            """,[kurs_id])
            return cursor.fetchall()

    @staticmethod
    def get_by_id(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, data_zapisu, wynik, kurs_id, uzytkownik_id
                FROM integracja_uzytkownika_wynikiegzaminu
                WHERE id = %s;
            """, [id])
            return cursor.fetchone()

    @staticmethod
    def get_by_uzytkownik_and_kurs(uzytkownik_id, kurs_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, data_zapisu, wynik, kurs_id, uzytkownik_id
                FROM integracja_uzytkownika_wynikiegzaminu
                WHERE uzytkownik_id = %s AND kurs_id = %s
                ORDER BY data_zapisu DESC;
            """, [uzytkownik_id, kurs_id])
            return cursor.fetchall()

    @staticmethod
    def get_average_uzytkownik_kurs_grade(uzytkownik_id, kurs_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT avg, kurs_id, uzytkownik_id, username
                FROM average_grade_for_user_kurs_view
                WHERE uzytkownik_id = %s AND kurs_id = %s;
            """, [uzytkownik_id, kurs_id])
            return cursor.fetchone()

    @staticmethod
    def get_average_kurs_grade(kurs_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT avg_wynik, kurs_id
                FROM avg_kurs_grade
                WHERE kurs_id = %s;
            """, [kurs_id])
            return cursor.fetchone()
        
    @staticmethod
    def insert_wynik(wynik, kurs_id, uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO integracja_uzytkownika_wynikiegzaminu 
                (data_zapisu, wynik, kurs_id, uzytkownik_id)
                VALUES (NOW(), %s, %s, %s)
                RETURNING id, data_zapisu, wynik, kurs_id, uzytkownik_id;
            """, [wynik, kurs_id, uzytkownik_id])
            return cursor.fetchone()
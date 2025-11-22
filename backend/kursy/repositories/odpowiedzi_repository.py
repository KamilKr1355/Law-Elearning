from django.db import connection

class OdpowiedziRepository:

    @staticmethod
    def get_by_id(id):
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id,tresc, poprawna,pytanie_id
             FROM kursy_odpowiedz WHERE id=%s;""",[id])
            return cursor.fetchone()
        
    @staticmethod
    def get_all_by_pytanie_id(pytanie_id):
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id,tresc, poprawna,pytanie_id
             FROM kursy_odpowiedz WHERE pytanie_id=%s;""",[pytanie_id])
            return cursor.fetchall()
        
    @staticmethod
    def insert(tresc,poprawna,pytanie_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO kursy_odpowiedz (tresc,poprawna,pytanie_id)
                VALUES (%s,%s,%s)
                RETURNING id;
            """, [tresc,poprawna,pytanie_id])
            return cursor.fetchone()[0]
        
    @staticmethod
    def update(id, tresc,poprawna,pytanie_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE kursy_odpowiedz
                SET tresc=%s,
                           poprawna=%s,
                           pytanie_id=%s
                WHERE id=%s
                RETURNING id;
            """, [tresc,poprawna,pytanie_id, id])
            return cursor.fetchone()

    @staticmethod
    def delete(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM kursy_odpowiedz
                WHERE id=%s
                RETURNING id;
            """, [id])
            return cursor.fetchone()
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
            return cursor.fetchone()

    @staticmethod
    def delete(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM kursy_pytanie
                WHERE id=%s
                RETURNING id;
            """, [id])
            return cursor.fetchone()

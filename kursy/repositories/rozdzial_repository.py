from django.db import connection

class RozdzialRepository:

    @staticmethod
    def get_all_for_kurs(kurs_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nazwa_rozdzialu, kurs_id
                FROM kursy_rozdzial
                WHERE kurs_id = %s;
            """, [kurs_id])
            return cursor.fetchall()

    @staticmethod
    def get_by_id(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nazwa_rozdzialu, kurs_id
                FROM kursy_rozdzial
                WHERE id = %s;
            """, [id])
            return cursor.fetchone()

    @staticmethod
    def insert(nazwa_rozdzialu, kurs_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO kursy_rozdzial (nazwa_rozdzialu, kurs_id)
                VALUES (%s, %s)
                RETURNING id;
            """, [nazwa_rozdzialu, kurs_id])
            return cursor.fetchone()[0]

    @staticmethod
    def update(id, nazwa_rozdzialu, kurs_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE kursy_rozdzial
                SET nazwa_rozdzialu = %s, kurs_id = %s
                WHERE id = %s
                RETURNING id;
            """, [nazwa_rozdzialu, kurs_id, id])
            return cursor.fetchone()

    @staticmethod
    def delete(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM kursy_rozdzial
                WHERE id = %s
                RETURNING id;
            """, [id])
            return cursor.fetchone()

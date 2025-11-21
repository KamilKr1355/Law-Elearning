from django.db import connection

class KursRepository:

    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nazwa_kursu FROM kursy_kurs;")
            return cursor.fetchall()

    @staticmethod
    def get_by_id(id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nazwa_kursu FROM kursy_kurs WHERE id=%s;", [id])
            return cursor.fetchone()

    @staticmethod
    def insert(nazwa_kursu):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO kursy_kurs (nazwa_kursu)
                VALUES (%s)
                RETURNING id;
            """, [nazwa_kursu])
            return cursor.fetchone()[0]

    @staticmethod
    def update(id, nazwa_kursu):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE kursy_kurs
                SET nazwa_kursu=%s
                WHERE id=%s
                RETURNING id;
            """, [nazwa_kursu, id])
            return cursor.fetchone()

    @staticmethod
    def delete(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM kursy_kurs
                WHERE id=%s
                RETURNING id;
            """, [id])
            return cursor.fetchone()


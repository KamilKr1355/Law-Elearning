from django.db import connection

class ArtykulRepository:

    @staticmethod
    def get_all(kurs_id):
         with connection.cursor() as cursor:
                cursor.execute("SELECT artykul_id,tytul,tresc,nazwa_kursu,kurs_id FROM artykul_rozdzial_view WHERE kurs_id = %s;",[kurs_id])
                return cursor.fetchall()

    @staticmethod
    def get_by_id(artykul_id):
        with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT artykul_id,tresc,nazwa_kursu,id FROM artykul_kurs_view WHERE artykul_id=%s;",
                    [artykul_id]
                )
                return cursor.fetchone()

    @staticmethod
    def get_by_id2(artykul_id):
        with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT artykul_id,tytul,tresc,nazwa_kursu,kurs_id FROM artykul_rozdzial_view WHERE artykul_id=%s;",
                    [artykul_id]
                )
                return cursor.fetchone()
        
    @staticmethod
    def get_by_rozdzial_id(rozdzial_id):
        with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT artykul_id,tytul,tresc,nazwa_kursu,kurs_id,rozdzial_id FROM artykul_rozdzial_view WHERE rozdzial_id=%s;",
                    [rozdzial_id]
                )
                return cursor.fetchall()

    @staticmethod    
    def insert(tresc,tytul,nr_artykulu,rozdzial_id):
          with connection.cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO kursy_artykul (tresc,tytul,nr_artykulu,rozdzial_id)
                        VALUES (%s, %s, %s, %s) RETURNING id;
                    """,[tresc,tytul,nr_artykulu,rozdzial_id]
                )
                return cursor.fetchone()
          
    @staticmethod
    def update(tresc,tytul,nr_artykulu,rozdzial_id,id):
          with connection.cursor() as cursor:
                cursor.execute(
                    """
                        UPDATE kursy_artykul SET tresc=%s, tytul=%s,nr_artykulu=%s,rozdzial_id=%s
                        WHERE id = %s
                        RETURNING id;
                    """,[tresc,tytul,nr_artykulu,rozdzial_id,id]
                )
                return cursor.fetchone()
          
    @staticmethod
    def delete(id):
          with connection.cursor() as cursor:
            cursor.execute("""
                            DELETE FROM kursy_artykul WHERE id=%s RETURNING id;
                           """, [id])
            return cursor.fetchone()
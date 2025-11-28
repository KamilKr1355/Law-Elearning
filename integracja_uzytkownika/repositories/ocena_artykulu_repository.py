from django.db import connection

class OcenaArtykuluRepository:

    @staticmethod
    def get_by_id(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, ocena, data, artykul_id, uzytkownik_id
                FROM integracja_uzytkownika_ocenaartykulu 
                WHERE id = %s;
            """, [id])
            return cursor.fetchone()

    @staticmethod
    def getOcenaArtykulu(artykul_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT AVG(ocena),artykul_id
                           FROM integracja_uzytkownika_ocenaartykulu
						   WHERE artykul_id = %s
                           GROUP BY artykul_id;
                           """,[artykul_id])
            
            return cursor.fetchone()
            
    @staticmethod
    def getOcenaUzytkownika(artykul_id,uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT id,ocena,data,artykul_id,uzytkownik_id
                           FROM integracja_uzytkownika_ocenaartykulu
						   WHERE artykul_id = %s AND uzytkownik_id = %s
                           GROUP BY artykul_id;
                           """,[artykul_id,uzytkownik_id])
            
            return cursor.fetchone()


    @staticmethod
    def insertOcena(artykul_id,ocena,uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                           INSERT INTO integracja_uzytkownika_ocenaartykulu (ocena,artykul_id,uzytkownik_id)
                           VALUES (%s,%s,%s)
                           RETURNING id;
                           """,[ocena,artykul_id,uzytkownik_id])
            
            return cursor.fetchone()[0]
        
    @staticmethod
    def update(artykul_id,ocena,uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                           UPDATE integracja_uzytkownika_ocenaartykulu
                           SET ocena = %s
                           WHERE artykul_id = %s AND uzytkownik_id = %s
                           RETURNING id;
                           """,[ocena,artykul_id,uzytkownik_id])
            
            result = cursor.fetchone()
            return result[0] if result else None
        

    @staticmethod
    def delete(artykul_id,uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                           DELETE FROM integracja_uzytkownika_ocenaartykulu
                           WHERE artykul_id = %s AND uzytkownik_id = %s
                           RETURNING id;
                           """,[artykul_id,uzytkownik_id])
            
            result = cursor.fetchone()
            return result[0] if result else None
from django.db import connection

class KomentarzRepository:

    @staticmethod
    def get_by_artykul_and_uzytkownik(artykul_id,uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT uk.id,uk.tresc,uk.uzytkownik_id,uk.artykul_id,uk.data_zapisu,u.username
                           FROM integracja_uzytkownika_komentarz uk
                           JOIN auth_user u on u.id=uk.uzytkownik_id
                           WHERE artykul_id = %s AND uzytkownik_id = %s;
                           """,[artykul_id,uzytkownik_id])
            
            return cursor.fetchall()
        
    def get_by_id(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT uk.id,uk.tresc,uk.uzytkownik_id,uk.artykul_id,uk.data_zapisu,u.username
                           FROM integracja_uzytkownika_komentarz uk
                           JOIN auth_user u on u.id=uk.uzytkownik_id
                           WHERE uk.id = %s;
                           """,[id])
            
            return cursor.fetchone()
        
    @staticmethod
    def get_by_artykul(artykul_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT uk.id,uk.tresc,uk.uzytkownik_id,uk.artykul_id,uk.data_zapisu,u.username
                           FROM integracja_uzytkownika_komentarz uk
                           JOIN auth_user u on u.id=uk.uzytkownik_id
                           WHERE artykul_id = %s;
                           """,[artykul_id])
            
            return cursor.fetchall()
        
    @staticmethod
    def insert(tresc,artykul_id,uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                           INSERT INTO integracja_uzytkownika_komentarz(tresc,data_zapisu,artykul_id,uzytkownik_id)
                           VALUES (%s,NOW(),%s,%s)
                           RETURNING id;
                           """,[tresc,artykul_id,uzytkownik_id])
            
            return cursor.fetchone()[0]
        
    @staticmethod
    def update(id,tresc,uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                           UPDATE integracja_uzytkownika_komentarz
                           SET tresc = %s
                           WHERE id = %s AND uzytkownik_id = %s
                           RETURNING id;
                           """,[tresc,id,uzytkownik_id])
            
            result = cursor.fetchone()
            return result[0] if result else None
        
    @staticmethod
    def delete(id,uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                           DELETE FROM integracja_uzytkownika_komentarz
                           WHERE id = %s AND uzytkownik_id = %s
                           RETURNING id;
                           """,[id,uzytkownik_id])
            
            result = cursor.fetchone()
            return result[0] if result else None
        
    @staticmethod
    def delete_admin(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                           DELETE FROM integracja_uzytkownika_komentarz
                           WHERE id = %s
                           RETURNING id;
                           """,[id])
            
            result = cursor.fetchone()
            return result[0] if result else None

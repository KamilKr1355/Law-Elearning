from django.db import connection

class ZapisRepository:

    @staticmethod
    def get_zapisane_by_uzytkownik_id(uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, data_zapisu, tresc, tytul, artykul_id
                FROM zapis_uzytkownika_view 
                WHERE uzytkownik_id = %s
                ORDER BY data_zapisu DESC;
            """, [uzytkownik_id])
            return cursor.fetchall()
        
    @staticmethod
    def get_by_id(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, data_zapisu, tresc, tytul, artykul_id
                FROM zapis_uzytkownika_view 
                WHERE id = %s;
            """, [id])
            return cursor.fetchone()
        
    @staticmethod
    def check_exists(uzytkownik_id, artykul_id):
        """Sprawdź czy zapis już istnieje"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id FROM integracja_uzytkownika_zapisartykulu
                WHERE uzytkownik_id = %s AND artykul_id = %s;
            """, [uzytkownik_id, artykul_id])
            return cursor.fetchone()
        
    @staticmethod
    def delete(uzytkownik_id, artykul_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM integracja_uzytkownika_zapisartykulu
                WHERE uzytkownik_id = %s AND artykul_id = %s
                RETURNING id;
            """, [uzytkownik_id, artykul_id])
            result = cursor.fetchone()
            return result[0] if result else None
        
    @staticmethod   
    def create(uzytkownik_id, artykul_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO integracja_uzytkownika_zapisartykulu (uzytkownik_id, artykul_id,data_zapisu)
                VALUES (%s, %s,NOW())
                RETURNING id;
            """, [uzytkownik_id, artykul_id])
            return cursor.fetchone()[0]


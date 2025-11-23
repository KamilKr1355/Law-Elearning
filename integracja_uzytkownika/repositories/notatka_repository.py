from django.db import connection

class NotatkaRepository:

    @staticmethod
    def get_by_uzytkownik_and_artykul(uzytkownik_id,artykul_id):
        
        with connection.cursor() as cursor:
            cursor.execute("""
                            SELECT id,tresc,data_zapisu,artykul_id,uzytkownik_id
                            FROM integracja_uzytkownika_notatka
                            WHERE uzytkownik_id = %s AND artykul_id = %s;
                           """,[uzytkownik_id,artykul_id])
            
            return cursor.fetchall()
            
    @staticmethod
    def get_by_uzytkownik(uzytkownik_id):
        
        with connection.cursor() as cursor:
            cursor.execute("""
                            SELECT id,tresc,data_zapisu,artykul_id,uzytkownik_id
                            FROM integracja_uzytkownika_notatka
                            WHERE uzytkownik_id = %s;
                           """,[uzytkownik_id])
            
            return cursor.fetchall()
            
    @staticmethod
    def get_by_id(id):
        
        with connection.cursor() as cursor:
            cursor.execute("""
                            SELECT id,tresc,data_zapisu,artykul_id,uzytkownik_id
                            FROM integracja_uzytkownika_notatka
                            WHERE id = %s;
                           """,[id])
            
            return cursor.fetchone()

    @staticmethod
    def insert(tresc,uzytkownik_id,artykul_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                            INSERT INTO integracja_uzytkownika_notatka (tresc,data_zapisu,artykul_id,uzytkownik_id)
                            VALUES (%s,NOW(),%s,%s)
                            RETURNING id;
                           """,[tresc,artykul_id,uzytkownik_id])
            
            return cursor.fetchone()[0]
        
    @staticmethod
    def update(id,tresc,uzytkownik_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                            UPDATE integracja_uzytkownika_notatka 
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
                            DELETE FROM integracja_uzytkownika_notatka 
                            WHERE id = %s AND uzytkownik_id = %s
                            RETURNING id;
                           """,[id,uzytkownik_id])
            
            result = cursor.fetchone()
            return result[0] if result else None
        
    
            
            

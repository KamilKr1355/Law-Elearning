from django.db import connection

class ProgressPytanRepository:

    @staticmethod
    def pobierz_postep_dla_uzytkownika_kurs(uzytkownik_id, kurs_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    pp.id, pp.uzytkownik_id, pp.pytanie_id, pp.status, pp.data_aktualizacji
                FROM 
                    integracja_uzytkownika_progresspytan pp
                JOIN 
                    kursy_pytanie p ON pp.pytanie_id = p.id
                JOIN
                    kursy_artykul a ON p.artykul_id = a.id
                JOIN
                    kursy_rozdzial r ON a.rozdzial_id = r.id
                WHERE 
                    pp.uzytkownik_id = %s AND r.kurs_id = %s;
            """, [uzytkownik_id, kurs_id])

            return cursor.fetchall()
        
    @staticmethod
    def pobierz_status_uzytkownika(uzytkownik_id, pytanie_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT status 
                FROM integracja_uzytkownika_progresspytan 
                WHERE uzytkownik_id = %s AND pytanie_id = %s;
            """, [uzytkownik_id, pytanie_id])
            result = cursor.fetchone()
            return result[0] if result else None
        
    @staticmethod
    def utworz_lub_aktualizuj(uzytkownik_id, pytanie_id, status):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE integracja_uzytkownika_progresspytan
                SET status = %s, data_aktualizacji = NOW()
                WHERE uzytkownik_id = %s AND pytanie_id = %s
                RETURNING id;
            """, [status, uzytkownik_id, pytanie_id])
            
            result = cursor.fetchone()
            
            if result:
                return result[0] 

            cursor.execute("""
                INSERT INTO integracja_uzytkownika_progresspytan 
                (uzytkownik_id, pytanie_id, status, data_aktualizacji)
                VALUES (%s, %s, %s, NOW())
                RETURNING id;
            """, [uzytkownik_id, pytanie_id, status])
            return cursor.fetchone()[0]
        
    @staticmethod
    def pobierz_po_id(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, uzytkownik_id, pytanie_id, status, data_aktualizacji 
                FROM integracja_uzytkownika_progresspytan WHERE id = %s;
            """, [id])
            return cursor.fetchone()
        
    @staticmethod
    def usun_po_kurs_id(user_id,kurs_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM integracja_uzytkownika_progresspytan pp USING (SELECT p.id FROM kursy_pytanie p INNER JOIN kursy_artykul a ON a.id = p.artykul_id INNER JOIN kursy_rozdzial r ON r.id = a.rozdzial_id WHERE r.kurs_id = %s) pom WHERE pp.uzytkownik_id = %s AND pom.id= pp.pytanie_id RETURNING pp.id;
            """, [kurs_id,user_id])
            return cursor.fetchall()
        
    @staticmethod
    def pobierz_podsumowanie_dla_kursu(uzytkownik_id, kurs_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    (SELECT COUNT(DISTINCT p.id)
                     FROM kursy_pytanie p
                     JOIN kursy_artykul a ON p.artykul_id = a.id
                     JOIN kursy_rozdzial r ON a.rozdzial_id = r.id
                     WHERE r.kurs_id = %s) AS total_questions,
                    
                    (SELECT COUNT(DISTINCT pp.pytanie_id)
                     FROM integracja_uzytkownika_progresspytan pp
                     JOIN kursy_pytanie p ON pp.pytanie_id = p.id
                     JOIN kursy_artykul a ON p.artykul_id = a.id
                     JOIN kursy_rozdzial r ON a.rozdzial_id = r.id
                     WHERE pp.uzytkownik_id = %s
                     AND r.kurs_id = %s
                     AND pp.status IN ('OP', 'OZ', 'W')) AS completed_count;
            """, [kurs_id, uzytkownik_id, kurs_id])
            return cursor.fetchone()
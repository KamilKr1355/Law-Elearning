from django.db import connection

class StatystykiPytaniaRepository:

    @staticmethod
    def pobierz_wg_pytania(pytanie_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, pytanie_id, ilosc_odpowiedzi, poprawne_odpowiedzi
                FROM statystyki_statystykipytania
                WHERE pytanie_id = %s;
            """, [pytanie_id])
            return cursor.fetchone()

    @staticmethod
    def aktualizuj_statystyki_repo(pytanie_id, is_correct):
        increment_correct = 1 if is_correct else 0
        
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE statystyki_statystykipytania
                SET ilosc_odpowiedzi = ilosc_odpowiedzi + 1,
                    poprawne_odpowiedzi = poprawne_odpowiedzi + %s
                WHERE pytanie_id = %s
                RETURNING id;
            """, [increment_correct, pytanie_id])
            
            result = cursor.fetchone()
            
            if result:
                return result[0] 

            cursor.execute("""
                INSERT INTO statystyki_statystykipytania 
                (pytanie_id, ilosc_odpowiedzi, poprawne_odpowiedzi)
                VALUES (%s, 1, %s)
                RETURNING id;
            """, [pytanie_id, increment_correct])
            return cursor.fetchone()[0]
    
    @staticmethod
    def pobierz_po_id(id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, pytanie_id, ilosc_odpowiedzi, poprawne_odpowiedzi
                FROM statystyki_statystykipytania WHERE id = %s;
            """, [id])
            return cursor.fetchone()
        
    @staticmethod
    def pobierz_wszystkie():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                s.id,p.id AS pytanie_id,
                COALESCE(s.ilosc_odpowiedzi, 0) AS ilosc_odpowiedzi,
                COALESCE(s.poprawne_odpowiedzi, 0) AS poprawne_odpowiedzi
                FROM kursy_pytanie p
                LEFT JOIN statystyki_statystykipytania s ON p.id = s.pytanie_id
                ORDER BY
                COALESCE(s.poprawne_odpowiedzi, 0) / COALESCE(s.ilosc_odpowiedzi, 1)::NUMERIC ASC;
            """)
            return cursor.fetchall()
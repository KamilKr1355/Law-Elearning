from django.db import connection

class KursyDniRepository:

    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT dzien, liczba_kursow
                FROM kursy_ukonczone_ostatnie_7_dni;
            """)
            return cursor.fetchall()

    
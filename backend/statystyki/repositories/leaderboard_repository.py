from django.db import connection

class LeaderboardRepository:

    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT srednia::NUMERIC,username
                FROM leaderboard;
            """)
            return cursor.fetchall()
        

    
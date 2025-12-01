from django.db import connection

class QuizRepository:

    @staticmethod
    def get_questions_for_course(course_name):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.tresc
                FROM kursy_pytanie p
                JOIN artykul_kurs_view ak ON ak.artykul_id = p.artykul_id
                WHERE ak.nazwa_kursu = %s
            """, [course_name])
            return cursor.fetchall()

    @staticmethod
    def get_answers_for_question(question_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT o.id,o.tresc
                FROM kursy_odpowiedz o
                WHERE pytanie_id=%s;
            """, [question_id])
            return cursor.fetchall()

    @staticmethod
    def get_all_correct_answers():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT odpowiedz_id, pytanie_id 
                FROM quiz_view 
                WHERE poprawna=true;
            """)
            return cursor.fetchall()

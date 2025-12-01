import random
from ..repositories.quiz_repository import QuizRepository
from ..mappers.quiz_mapper import map_question_row, map_answer_row

class QuizService:

    def start_quiz(self, kurs_nazwa, count):
        rows = QuizRepository.get_questions_for_course(kurs_nazwa)
        if not rows:
            return None

        if count > len(rows):
            count = len(rows)

        selected = random.sample(rows, count)
        quiz = []

        for q in selected: #q ma id i tresc
            answers = QuizRepository.get_answers_for_question(q[0])
            quiz.append({
                **map_question_row(q),
                "odpowiedzi": [map_answer_row(a) for a in answers]
            })

        return quiz

    def check_quiz(self, odpowiedzi):
        poprawne = QuizRepository.get_all_correct_answers()

        wynik = 0
        poprawne_ids = []

        for odp in odpowiedzi:
            pyt_id = odp["pytanie_id"]
            wybrana = odp["wybrana_opcja"]

            if (wybrana, pyt_id) in poprawne:
                wynik += 1
                poprawne_ids.append(pyt_id)

        return wynik, poprawne_ids

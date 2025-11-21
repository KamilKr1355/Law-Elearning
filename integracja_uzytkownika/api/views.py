from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuizSerializer, SprawdzOdpowiedzSerializer
from integracja_uzytkownika.services.quiz_service import QuizService


class Start_quiz(APIView):
    permission_classes = [IsAuthenticated]

    service = QuizService()  

    def get(self, request):
        kurs = request.GET.get("kursy")
        count = int(request.GET.get("liczba_pytan", 20))

        if not kurs or count <= 0:
            return Response({"error": "Podaj poprawne dane"}, status=400)

        quiz = self.service.start_quiz(kurs, count)

        if quiz is None:
            return Response({"error": "Brak pytań"}, status=404)

        return Response(QuizSerializer(quiz, many=True).data, status=200)


class Sprawdz_quiz(APIView):
    permission_classes = [IsAuthenticated]

    service = QuizService()

    def post(self, request):
        serializer = SprawdzOdpowiedzSerializer(
            data=request.data.get("odpowiedzi"),
            many=True
        )

        if not serializer.is_valid():
            return Response({"error": "Zły format odpowiedzi"}, status=400)

        wynik, poprawne_ids = self.service.check_quiz(serializer.validated_data)

        return Response({
            "punkty": wynik,
            "poprawne": poprawne_ids
        }, status=200)

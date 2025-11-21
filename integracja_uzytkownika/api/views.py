from rest_framework.response import Response
from django.db import connection
import random
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import(
                         QuizSerializer,SprawdzOdpowiedzSerializer)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework_simplejwt.views import TokenObtainPairView 
from rest_framework.views import APIView


class Start_quiz(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        kursy_param = request.GET.get("kursy")
        count = int(request.GET.get("liczba_pytan", 20))

        if not kursy_param or count <= 0:
            return Response({"error": "Podaj poprawne dane"}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.tresc
                FROM kursy_pytanie p
                JOIN artykul_kurs_view ak ON ak.artykul_id = p.artykul_id
                WHERE ak.nazwa_kursu = %s
            """, [kursy_param])
            rows = cursor.fetchall()

        if count > len(rows):
            count = len(rows)
        rows = random.sample(rows, count)

        quiz = []

        for row in rows:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT o.tresc, o.poprawna
                    FROM kursy_odpowiedz o
                    WHERE pytanie_id=%s;
                """, [row[0]])
                odpowiedzi = cursor.fetchall()

            quiz.append({
                "id": row[0],
                "tresc": row[1],
                "odpowiedzi": [{"text": o[0], "correct": o[1]} for o in odpowiedzi]
            })

        return Response(QuizSerializer(quiz, many=True).data)


class Sprawdz_quiz(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SprawdzOdpowiedzSerializer(
            data=request.data.get("odpowiedzi"),
            many=True
        )

        if not serializer.is_valid():
            return Response(
                {"error": "Zły format odpowiedzi"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT tresc, pytanie_id FROM kursy_odpowiedz WHERE poprawna=true;"
            )
            poprawne_odpowiedzi = cursor.fetchall()

        wynik = 0
        poprawne_id = []

        for odp in serializer.validated_data:
            pyt_id = odp["pytanie_id"]
            wybrana = odp["wybrana_opcja"]

            if (wybrana, pyt_id) in poprawne_odpowiedzi:
                wynik += 1
                poprawne_id.append(pyt_id)

        return Response({
            "punkty": wynik,
            "poprawne": poprawne_id
        })
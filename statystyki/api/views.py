from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from integracja_uzytkownika.services.progress_pytan_service import ProgressPytanService
from statystyki.services.statystyki_pytania_service import StatystykiPytaniaService
from statystyki.services.leaderboard_service import LeaderboardService
from statystyki.services.kursy_dni_service import KursyDniService
from statystyki.api.serializers import (StatystykaUpdateInputSerializer, StatystykiPytaniaSerializer, KursDniSerializer,LeaderboardSerializer)


statystyki_pytania_schema = openapi.Response("Obiekt Statystyki Pytania.", schema=StatystykiPytaniaSerializer)
lista_kursy_dni_schema = openapi.Response("Obiekt Kursow w 7 dni.", schema=KursDniSerializer(many=True))
lista_leaderboard_schema = openapi.Response("Leaderboard", schema=LeaderboardSerializer(many=True))

class StatystykiPytaniaAPIView(APIView):
    """
    ZARZĄDZANIE STATYSTYKAMI PYTAŃ (GLOBALNYMI)
    
    Endpoint służy do pobierania globalnych statystyk pytania (GET) 
    """
    service_stats = StatystykiPytaniaService()
    service_progress = ProgressPytanService()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca globalne statystyki dla pytania (ilość odpowiedzi, % poprawnych). Dostępne publicznie.",
        responses={
            status.HTTP_200_OK: statystyki_pytania_schema,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono statystyk (zwracane są puste statystyki 200 OK)."
        }
    )
    def get(self, request, pytanie_id):
        stats = self.service_stats.pobierz_statystyki(pytanie_id)
        
        if not stats:
            puste_dane = {"pytanie_id": pytanie_id, "ilosc_odpowiedzi": 0, "poprawne_odpowiedzi": 0}
            return Response(StatystykiPytaniaSerializer(puste_dane).data, status=status.HTTP_200_OK)

        return Response(StatystykiPytaniaSerializer(stats).data, status=status.HTTP_200_OK)

class StatystykiWszystkichPytanAPIView(APIView):
    """
    ZARZĄDZANIE STATYSTYKAMI WSZYSTKICH PYTAŃ (GLOBALNYMI)
    
    Endpoint służy do pobierania globalnych statystyk WSZYSTKICH pytan (GET) 
    """
    service_stats = StatystykiPytaniaService()
    service_progress = ProgressPytanService()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca globalne statystyki wszystkich pytan",
        responses={
            status.HTTP_200_OK: statystyki_pytania_schema,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono statystyk"
        }
    )
    def get(self, request):
        stats = self.service_stats.pobierz_wszystkie_statystyki()
        
        if not stats:
            return Response({"error": "Brak statystyk"}, status=status.HTTP_404_NOT_FOUND)

        return Response(StatystykiPytaniaSerializer(stats,many=True).data, status=status.HTTP_200_OK)


class StatystykiPytaniaEdytujAPIView(APIView):
    """
    ZARZĄDZANIE STATYSTYKAMI PYTAŃ (GLOBALNYMI)
    
    Endpoint służy do rejestrowania 
    odpowiedzi użytkownika (POST) w trybie nauki.
    
    Ważne: Metoda POST aktualizuje statystyki GLOBALNE tylko przy PIERWSZEJ OSTATECZNEJ próbie odpowiedzi użytkownika.
    """
    service_stats = StatystykiPytaniaService()
    service_progress = ProgressPytanService()
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    @swagger_auto_schema(
        operation_description="REJESTRACJA ODPOWIEDZI: Rejestruje odpowiedź użytkownika w trybie nauki. Aktualizuje postęp użytkownika (OP/OZ) oraz warunkowo aktualizuje statystyki GLOBALNE (tylko przy pierwszej próbie).",
        request_body=StatystykaUpdateInputSerializer,
        responses={
            status.HTTP_200_OK: statystyki_pytania_schema,
            status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych wejściowych."
        }
    )
    def post(self, request):
        serializer = StatystykaUpdateInputSerializer(data=request.data) 
        
        if serializer.is_valid():
            pytanie_id = serializer.validated_data['pytanie_id']
            is_correct = serializer.validated_data['is_correct']
            uzytkownik_id = request.user.id
            
            progress_service = self.service_progress 
            stats_service = self.service_stats

            czy_juz_odpowiedziano = progress_service.sprawdz_czy_odpowiedziano(uzytkownik_id, pytanie_id)
            jest_pierwsza_proba = not czy_juz_odpowiedziano

            zaktualizowane_statystyki = stats_service.aktualizuj_statystyki(
                pytanie_id, 
                is_correct, 
                jest_pierwsza_proba
            )
            
            progress_service.aktualizuj_postep(
                uzytkownik_id, 
                pytanie_id, 
                is_correct
            )

            return Response(StatystykiPytaniaSerializer(zaktualizowane_statystyki).data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class KursyDniAPIView(APIView):
    """
    ZARZĄDZANIE LICZBA EGZAMINOW W 7 DNI
    
    Endpoint służy do pobierania ile egzaminow zostało ukończonych w ostatnich 7 dniach (GET)
    
    """
    service = KursyDniService()
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca liczbe ukonczonych egzaminow w ostatnich 7 dniach",
        responses={
            status.HTTP_200_OK: lista_kursy_dni_schema,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono statystyk"
        }
    )
    def get(self, request):
        stats = self.service.pobierz_statystyki()
        
        if not stats:
            return Response({"error": "Brak statystyk"}, status=status.HTTP_404_NOT_FOUND)

        return Response(KursDniSerializer(stats,many=True).data, status=status.HTTP_200_OK)
    
class LeaderboardAPIView(APIView):
    """
    ZARZĄDZANIE LEADERBOARDEM
    
    Endpoint służy do pobierania TOP 3 UZYTKOWNIKOW Z NAJLEPSZA SREDNIA W MINIMUM 10 EGZAMINACH (SREDNIA MUSI BYC >=50%)
    """
    service = LeaderboardService()
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca TOP 3 UZYTKOWNIKOW Z NAJLEPSZA SREDNIA W MINIMUM 10 EGZAMINACH (SREDNIA MUSI BYC >=50%)",
        responses={
            status.HTTP_200_OK: lista_leaderboard_schema,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono statystyk"
        }
    )
    def get(self, request):
        stats = self.service.pobierz_wszystkie_statystyki()
        
        if not stats:
            return Response({"error": "Brak statystyk"}, status=status.HTTP_404_NOT_FOUND)

        return Response(LeaderboardSerializer(stats,many=True).data, status=status.HTTP_200_OK)
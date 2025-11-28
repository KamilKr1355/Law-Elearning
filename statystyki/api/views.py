from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from integracja_uzytkownika.services.progress_pytan_service import ProgressPytanService
from statystyki.services.statystyki_pytania_service import StatystykiPytaniaService
from statystyki.api.serializers import (StatystykaUpdateInputSerializer,StatystykiPytaniaSerializer)


class StatystykiPytaniaAPIView(APIView):
    service_stats = StatystykiPytaniaService()
    service_progress = ProgressPytanService()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pytanie_id):
        stats = self.service_stats.pobierz_statystyki(pytanie_id)
        
        if not stats:
            puste_dane = {"pytanie_id": pytanie_id, "ilosc_odpowiedzi": 0, "poprawne_odpowiedzi": 0}
            return Response(StatystykiPytaniaSerializer(puste_dane).data, status=status.HTTP_200_OK)

        return Response(StatystykiPytaniaSerializer(stats).data, status=status.HTTP_200_OK)
    
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
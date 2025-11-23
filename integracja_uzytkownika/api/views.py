from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import (QuizSerializer, SprawdzOdpowiedzSerializer,
                          ZapisArtykuluSerializer,ZapisArtykuluPostSerializer,
                          NotatkaSerializer,NotatkaPostSerializer,NotatkaPutSerializer)
from integracja_uzytkownika.services.quiz_service import QuizService
from integracja_uzytkownika.services.zapis_service import ZapisService
from integracja_uzytkownika.services.notatka_service import NotatkaService
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny


class Start_quiz(APIView):
    permission_classes = [IsAuthenticated]

    service = QuizService()  

    def get(self, request):
        kurs = request.GET.get("kursy")
        count = int(request.GET.get("liczba_pytan", 20))

        if not kurs or count <= 0:
            return Response({"error": "Podaj poprawne dane"}, status=status.HTTP_400_BAD_REQUEST)

        quiz = self.service.start_quiz(kurs, count)

        if quiz is None:
            return Response({"error": "Brak pytań"}, status=status.HTTP_404_NOT_FOUND)

        return Response(QuizSerializer(quiz, many=True).data, status=status.HTTP_200_OK)


class Sprawdz_quiz(APIView):
    permission_classes = [IsAuthenticated]

    service = QuizService()

    def post(self, request):
        serializer = SprawdzOdpowiedzSerializer(
            data=request.data.get("odpowiedzi"),
            many=True
        )

        if not serializer.is_valid():
            return Response({"error": "Zły format odpowiedzi"}, status=status.HTTP_400_BAD_REQUEST)

        wynik, poprawne_ids = self.service.check_quiz(serializer.validated_data)

        return Response({
            "punkty": wynik,
            "poprawne": poprawne_ids
        }, status=status.HTTP_200_OK)


class MojeZapisaneArtykulyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    service = ZapisService()

    def get(self, request):
        zapisy = self.service.list_all(request.user.id)
        
        if not zapisy:
            return Response(
                {"message": "Brak zapisanych artykułów"}, 
                status=status.HTTP_200_OK
            )
        
        return Response(
            ZapisArtykuluSerializer(zapisy, many=True).data, 
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = ZapisArtykuluPostSerializer(data=request.data)

        if serializer.is_valid():
            artykul_id = serializer.validated_data["artykul_id"]

            zapis = self.service.create(request.user.id, artykul_id)
            
            if not zapis:
                return Response(
                    {"error": "Artykuł już zapisany"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                ZapisArtykuluSerializer(zapis).data, 
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsunZapisArtykuluAPIView(APIView):
    permission_classes = [IsAuthenticated]
    service = ZapisService()

    def delete(self, request, artykul_id):
        deleted = self.service.delete(request.user.id, artykul_id)
        
        if deleted:
            return Response(
                {"message": "Zapis usunięty"}, 
                status=status.HTTP_200_OK
            )
        
        return Response(
            {"error": "Nie znaleziono zapisu"}, 
            status=status.HTTP_404_NOT_FOUND
        )


class MojeNotatkiApiView(APIView):

        """Endpoint dla notatek zalogowanego użytkownika"""
        permission_classes = [IsAuthenticated]
        service = NotatkaService()

        def get(self,request):

            artykul_id = request.query_params.get('artykul_id')

            if artykul_id:
                notatki = self.service.get_by_uzytkownik_and_artykul(request.user.id,artykul_id)
            else:
                notatki = self.service.get_by_uzytkownik(request.user.id)

            if not notatki:
                return Response({"message":"Nie znaleziono notatek"})
            
            return Response(NotatkaSerializer(notatki,many=True).data)
        
        def post(self,request):

            serializer = NotatkaPostSerializer(data=request.data)

            if serializer.is_valid():
                tresc = serializer.validated_data["tresc"]
                artykul_id = serializer.validated_data["artykul_id"]

                notatka = self.service.create(tresc,request.user.id,artykul_id)

                if not notatka:
                    return Response({"error":"Nie udalo sie utworzyc notatki"},
                                    status=status.HTTP_400_BAD_REQUEST)
                
                return Response(NotatkaSerializer(notatka,many=False).data,
                                status=status.HTTP_201_CREATED)

            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
class NotatkaSzczegolyApiView(APIView):
    
    permission_classes = [IsAuthenticated]
    service = NotatkaService()
    
    def get(self,request,id):

        notatka = self.service.get_by_id(id)
        
        if not notatka:
            return Response({"error":"Nie znaleziono notatki"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if notatka['uzytkownik_id'] != request.user.id:
            return Response({"error":"Brak uprawnien"},
                            status=status.HTTP_403_FORBIDDEN)
        
        return Response(NotatkaSerializer(notatka).data,
                        status=status.HTTP_200_OK)
    
    def put(self,request,id):

        serializer = NotatkaPutSerializer(data=request.data)

        if serializer.is_valid():
            tresc = serializer.validated_data["tresc"]

            notatka = self.service.update(id,tresc,request.user.id)

            if not notatka:
                return Response({"error":"Nie znaleziono notatki"},
                                status=status.HTTP_404_NOT_FOUND)
            
            return Response(NotatkaSerializer(notatka).data,
                            status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):

        deleted = self.service.delete(id,request.user.id)

        if deleted:
            return Response({"message":"Notatka usunięta"},
                            status=status.HTTP_200_OK)
        
        return Response({"error":"Nie znaleziono notatki lub brak uprawnien"},
                        status=status.HTTP_404_NOT_FOUND)
            


"""
TODO 
Artykul POST/PUT/DELETE
KURS PUT/DELETE
ROZDZIAL GET/POST/PUT/DELETE TESTUJ API
PYTANIA GET/POST/PUT/DELETE
ODPOWIEDZ GET/POST/PUT/DELETE
ZAPISARTYKULU GET/DELETE/POST
NOTATKA GET/POST/PUT/DELETE
    KOMENTARZ GET/POST/PUT/DELETE
    STATYSTYKIPYTANIA GET/PUT/PATCH?
    PROGRESSPYTAN GET/PUT/PATCH
    WYNIKIEGZAMINU POST/GET/PUT/PATCH
    OCENAARTYKULU GET/POST/PATCH/PUT?
"""
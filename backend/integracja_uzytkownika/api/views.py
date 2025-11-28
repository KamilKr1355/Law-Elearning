from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import (QuizSerializer, SprawdzOdpowiedzSerializer,
                          ZapisArtykuluSerializer,ZapisArtykuluPostSerializer,
                          NotatkaSerializer,NotatkaPostSerializer,NotatkaPutSerializer,
                          KomentarzSerializer,WynikiEgzaminuSerializer,OcenaArtykuluCombinedSerializer
                          ,OcenaArtykuluInputSerializer,OcenaArtykuluSerializer, 
    AverageUzytkownikKursSerializer,
    AverageKursSerializer, ProgressPytanSerializer,ProgressKursSummarySerializer)
from integracja_uzytkownika.services.quiz_service import QuizService
from integracja_uzytkownika.services.zapis_service import ZapisService
from integracja_uzytkownika.services.progress_pytan_service import ProgressPytanService
from integracja_uzytkownika.services.notatka_service import NotatkaService
from integracja_uzytkownika.services.komentarz_service import KomentarzService
from integracja_uzytkownika.services.wyniki_egzaminu_service import WynikEgzaminuService
from integracja_uzytkownika.services.ocena_artykulu_service import OcenaArtykuluService
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

"""
POST {{URL}}/api/aktywnosc/quiz/sprawdz/
{
    "kurs_id": 1,
    "odpowiedzi" : [
        {"pytanie_id":1,"wybrana_opcja":2},
        {"pytanie_id":2,"wybrana_opcja":5}
    ]
}
"""
class Sprawdz_quiz(APIView):
    permission_classes = [IsAuthenticated]

    service = QuizService()
    wyniki_service = WynikEgzaminuService()  
    
    def post(self, request):
        serializer = SprawdzOdpowiedzSerializer(
            data=request.data.get("odpowiedzi"),
            many=True
        )

        if not serializer.is_valid():
            return Response({"error": "Zły format odpowiedzi"}, status=status.HTTP_400_BAD_REQUEST)

        kurs_id = request.data.get("kurs_id") 
        
        if not kurs_id:
            return Response({"error": "Brak wymaganego pola kurs_id w ciele żądania"}, status=status.HTTP_400_BAD_REQUEST)

        wynik, poprawne_ids = self.service.check_quiz(serializer.validated_data)
        procent = round(float(100*wynik/len(request.data["odpowiedzi"])),2)
        self.wyniki_service.insert_wynik(procent,kurs_id,request.user.id)

        return Response({
            "punkty": wynik,
            "poprawne": poprawne_ids,
            "wynik": procent
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
            
class KomentarzeAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]  
        return [IsAuthenticated()]  
    
    service = KomentarzService()
    

    def get(self,request,artykul_id):

        komentarze = self.service.get_by_artykul(artykul_id)

        if not komentarze:
            return Response({"message",f"Artykuł {artykul_id} nie ma komentarzy"},
                            status=status.HTTP_200_OK)
        
        return Response(KomentarzSerializer(komentarze,many=True).data,
                        status=status.HTTP_200_OK)
    
    def post(self,request,artykul_id):

        serializer = KomentarzSerializer(data = request.data)

        if serializer.is_valid():
            tresc = serializer.validated_data['tresc']

            komentarz = self.service.create(tresc,artykul_id,request.user.id)

            if not komentarz:
                return Response({"error":"Nie udalo sie dodac komentarza"})
            
            return Response(KomentarzSerializer(komentarz).data,
                            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class KomentarzSzczegolyAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]
    
    service = KomentarzService()

    def get(self,request,id):

        komentarz = self.service.get_by_id(id)

        if not komentarz:
            return Response({"error":"Nie znaleziono komentarza"},
                            status=status.HTTP_404_NOT_FOUND)
    
        return Response(KomentarzSerializer(komentarz).data,
                        status=status.HTTP_200_OK)
    
    def put(self,request,id):

        serializer = KomentarzSerializer(data=request.data)

        if serializer.is_valid():
            tresc = serializer.validated_data['tresc']

            komentarz = self.service.get_by_id(id)

            if not komentarz:
                return Response({"error" : "Nie znaleziono komentarza"},
                                status=status.HTTP_404_NOT_FOUND)
            
            if komentarz["uzytkownik_id"] != request.user.id:
                return Response(
                    {"error": "Możesz edytować tylko swoje komentarze"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            updated = self.service.update(id,tresc,request.user.id)

            if not updated:
                return Response({"error":"Nie udalo sie zaktualizowac komentarza"},
                                status=status.HTTP_400_BAD_REQUEST)

            komentarz = self.service.get_by_id(updated)

            return Response(KomentarzSerializer(komentarz).data,
                            status=status.HTTP_200_OK)
        
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):

        komentarz = self.service.get_by_id(id)

        if not komentarz:
            return Response({"error","Nie znaleziono komentarza"},
                            status=status.HTTP_404_NOT_FOUND)
        

        isAuthor = self.request.user.id == komentarz["uzytkownik_id"]
        isAdmin = self.request.user.is_staff

        if not(isAdmin or isAuthor):
            
            return Response({"error":"Brak uprawnień do usuniecia komentarza"},
                            status=status.HTTP_403_FORBIDDEN)
        
        deleted = self.service.delete(id,self.request.user.id,isAdmin)

        if deleted:
            return Response({"message":"Komentarz usunięty"},
                            status=status.HTTP_200_OK)

        return Response({"error":"Nie udało się usunąć komentarza"},
                        status=status.HTTP_400_BAD_REQUEST)
    
class WynikiEgzaminuAPIView(APIView):

    permission_classes = [IsAuthenticated]
    service = WynikEgzaminuService()

    def get(self, request):
        kurs_id = request.query_params.get('kurs_id')
        
        if kurs_id:
            wyniki = self.service.get_by_uzytkownik_and_kurs(request.user.id, kurs_id)
        else:
            wyniki = self.service.get_by_uzytkownik(request.user.id)
        
        if not wyniki:
            return Response(
                {"message": "Brak wyników egzaminów"},
                status=status.HTTP_200_OK
            )
        
        return Response(
            WynikiEgzaminuSerializer(wyniki, many=True).data,
            status=status.HTTP_200_OK
        )


class WynikEgzaminuSzczegolyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    service = WynikEgzaminuService()

    def get(self, request, id):
        wynik = self.service.get_by_id(id)
        
        if not wynik:
            return Response(
                {"error": "Nie znaleziono wyniku"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if wynik['uzytkownik_id'] != request.user.id:
            return Response(
                {"error": "Brak uprawnień"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(
            WynikiEgzaminuSerializer(wynik).data,
            status=status.HTTP_200_OK
        )


class SredniaUzytkownikKursAPIView(APIView):
    permission_classes = [IsAuthenticated]
    service = WynikEgzaminuService()

    def get(self, request, kurs_id):
        srednia = self.service.get_average_uzytkownik_kurs_grade(request.user.id, kurs_id)
        
        if not srednia:
            return Response(
                {"message": "Brak wyników dla tego kursu"},
                status=status.HTTP_200_OK
            )
        
        return Response(
            AverageUzytkownikKursSerializer(srednia).data,
            status=status.HTTP_200_OK
        )


class SredniaKursAPIView(APIView):
    permission_classes = [IsAuthenticated]  
    service = WynikEgzaminuService()

    def get(self, request, kurs_id):
        srednia = self.service.get_average_kurs_grade(kurs_id)
        
        if not srednia:
            return Response(
                {"message": "Brak wyników dla tego kursu"},
                status=status.HTTP_200_OK
            )
        
        return Response(
            AverageKursSerializer(srednia).data,
            status=status.HTTP_200_OK
        )

class OcenaArtykuluAPIView(APIView):
    service = OcenaArtykuluService()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, artykul_id):
        
        srednia_ocena_data = self.service.pobierz_srednia_ocene(artykul_id)
        srednia_ocena = srednia_ocena_data['srednia_ocena']
        
        moja_ocena = None
        if request.user.is_authenticated:
            moja_ocena = self.service.pobierz_ocene_uzytkownika(artykul_id, request.user.id)

        dane_wynikowe = {
            "artykul_id": artykul_id,
            "srednia_ocena": round(srednia_ocena, 2) if srednia_ocena is not None else 0.0,
            "moja_ocena": moja_ocena
        }

        return Response(OcenaArtykuluCombinedSerializer(dane_wynikowe).data, status=status.HTTP_200_OK)

    def post(self, request, artykul_id):
        serializer = OcenaArtykuluInputSerializer(data=request.data)
        
        if serializer.is_valid():
            ocena = serializer.validated_data['ocena']
            
            ocena_obiekt = self.service.utworz_lub_aktualizuj_ocene(artykul_id, ocena, request.user.id)
            
            if ocena_obiekt:
                return Response(OcenaArtykuluSerializer(ocena_obiekt).data, status=status.HTTP_201_CREATED)
            
            return Response({"error": "Nie udało się zapisać oceny."}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, artykul_id):
        usunieto = self.service.usun_ocene(artykul_id, request.user.id)
        
        if usunieto:
            return Response({"message": "Ocena usunięta."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Nie znaleziono oceny do usunięcia."}, status=status.HTTP_404_NOT_FOUND)

class ProgressPytanAPIView(APIView):
    permission_classes = [IsAuthenticated]
    service = ProgressPytanService()

    def get(self, request, kurs_id):
        progress_list, summary = self.service.pobierz_postep_wg_kursu(request.user.id, kurs_id)
        
        total = summary.get('total_questions', 0)
        completed = summary.get('completed_count', 0)
        percentage = round((completed / total) * 100, 2) if total > 0 else 0.0
        
        summary['progress_percentage'] = percentage

        return Response({
            "lista_postepu": ProgressPytanSerializer(progress_list, many=True).data,
            "podsumowanie": ProgressKursSummarySerializer(summary).data
        }, status=status.HTTP_200_OK)
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
WYNIKIEGZAMINU POST/GET/PUT/PATCH
OCENAARTYKULU GET/POST/PATCH/PUT?
    PROGRESSPYTAN GET/PUT/PATCH
    STATYSTYKIPYTANIA GET/PUT/PATCH?
"""
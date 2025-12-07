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
from drf_yasg.utils import swagger_auto_schema
from integracja_uzytkownika.services.tryb_nauki_services import TrybNaukiService
from .serializers import PytanieTrybNaukiSerializer 
from drf_yasg import openapi

zapis_schema = openapi.Response("Obiekt Zapisu Artykułu.", ZapisArtykuluSerializer)
zapisy_list_schema = openapi.Response("Lista Zapisanych Artykułów.", ZapisArtykuluSerializer(many=True))
notatka_schema = openapi.Response("Obiekt Notatki.", NotatkaSerializer)
notatki_list_schema = openapi.Response("Lista Notatek.", NotatkaSerializer(many=True))
komentarz_schema = openapi.Response("Obiekt Komentarza.", KomentarzSerializer)
komentarze_list_schema = openapi.Response("Lista Komentarzy.", KomentarzSerializer(many=True))
wynik_egzaminu_schema = openapi.Response("Obiekt Wyniku Egzaminu.", WynikiEgzaminuSerializer)
wyniki_list_schema = openapi.Response("Lista Wyników Egzaminów.", WynikiEgzaminuSerializer(many=True))
progress_summary_schema = openapi.Response("Podsumowanie Postępu.", ProgressKursSummarySerializer)
quiz_list_schema = openapi.Response("Lista Pytań Quizu.", QuizSerializer(many=True))


class Start_quiz(APIView):
    """
    START QUIZU (EGZAMIN)
    
    Pobiera losową pulę pytań dla zadanego kursu wraz z odpowiedziami i ich id, gotową do przeprowadzenia egzaminu.
    """
    permission_classes = [IsAuthenticated]
    service = QuizService() 

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca listę pytań i odpowiedzi dla nowego quizu/egzaminu.",
        manual_parameters=[
            openapi.Parameter('kursy', openapi.IN_QUERY, description="Nazwa kursu, dla którego mają być pytania.", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('liczba_pytan', openapi.IN_QUERY, description="Maksymalna liczba pytań do pobrania (domyślnie 20).", type=openapi.TYPE_INTEGER),
        ],
        responses={
            status.HTTP_200_OK: quiz_list_schema,
            status.HTTP_404_NOT_FOUND: "Brak pytań dla danego kursu."
        }
    )
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
    """
    SPRAWDZANIE EGZAMINU I ZAPIS WYNIKU
    
    Przyjmuje odpowiedzi użytkownika, ocenia je i zapisuje wynik procentowy do historii egzaminów.
    """
    permission_classes = [IsAuthenticated]
    service = QuizService()
    wyniki_service = WynikEgzaminuService() 
    
    @swagger_auto_schema(
        operation_description="WYSYŁANIE: Ocenia odpowiedzi użytkownika, zapisuje wynik egzaminu i zwraca punkty/poprawne ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['kurs_id', 'odpowiedzi'],
            properties={
                'kurs_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID kursu, z którego pochodzi egzamin.'),
                'odpowiedzi': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'pytanie_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'wybrana_opcja': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID wybranej opcji odpowiedzi.')
                    }
                ))
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(description="Wynik egzaminu.", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "punkty": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "poprawne": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER), description='Lista ID pytań, na które odpowiedziano poprawnie.'),
                    "wynik": openapi.Schema(type=openapi.TYPE_NUMBER, description='Wynik procentowy egzaminu.')
                }
            )),
            status.HTTP_400_BAD_REQUEST: "Błąd walidacji lub brak pola 'kurs_id'."
        }
    )
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
    """
    ZAPISY ARTYKUŁÓW (GET LISTA, POST DODAJ)
    
    Zarządzanie listą artykułów zapisanych przez zalogowanego użytkownika (funkcjonalność "przeczytaj później").
    """
    permission_classes = [IsAuthenticated]
    service = ZapisService()

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca listę artykułów zapisanych przez użytkownika.",
        responses={
            status.HTTP_200_OK: zapisy_list_schema
        }
    )
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

    @swagger_auto_schema(
        operation_description="DODAWANIE: Zapisuje artykuł do listy użytkownika.",
        request_body=ZapisArtykuluPostSerializer,
        responses={
            status.HTTP_201_CREATED: zapis_schema,
            status.HTTP_400_BAD_REQUEST: "Błąd walidacji lub artykuł już zapisany."
        }
    )
    def post(self, request):
        serializer = ZapisArtykuluPostSerializer(data=request.data)

        if serializer.is_valid():
            artykul_id = serializer.validated_data["artykul_id"]

            zapis = self.service.create(request.user.id, artykul_id)
            
            if not zapis:
                #self.service.delete(request.user.id, artykul_id)
                return Response(
                    {"message": "Usunieto zapisanie artykulu"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                ZapisArtykuluSerializer(zapis).data, 
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ZarzadzajZapisArtykuluAPIView(APIView):
    """
    USUWANIE ZAPISU ARTYKUŁU (DELETE)
    
    Usuwa pojedynczy zapisany artykuł na podstawie jego ID.
    """
    permission_classes = [IsAuthenticated]
    service = ZapisService()
    
    @swagger_auto_schema(
        operation_description="USUWANIE: Usuwa zapisany artykuł po ID.",
        responses={
            status.HTTP_200_OK: openapi.Response(description="Zapis usunięty pomyślnie."),
            status.HTTP_404_NOT_FOUND: "Nie znaleziono zapisu."
        }
    )
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

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca czy zapis istnieje",
        manual_parameters=[
            openapi.Parameter('artykul_id', openapi.IN_QUERY, description="Opcjonalny ID artykułu, aby pobrać notatki tylko dla niego.", type=openapi.TYPE_INTEGER),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(description="Zwraca czy zapis istnieje."),
            status.HTTP_204_NO_CONTENT: "Zapis nie istnieje."
        }
    )
    def get(self,request,artykul_id):
        zapis = self.service.check_exists(request.user.id,artykul_id)

        if not zapis:
            return Response({"istnieje":False}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({"istnieje":True}, status=status.HTTP_200_OK)

class MojeNotatkiApiView(APIView):
    """
    ZARZĄDZANIE NOTATKAMI (GET LISTA, POST DODAJ)
    
    Zarządzanie notatkami zalogowanego użytkownika.
    """
    permission_classes = [IsAuthenticated]
    service = NotatkaService()

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca listę wszystkich notatek użytkownika lub filtruje je po ID artykułu (query param: artykul_id).",
        manual_parameters=[
            openapi.Parameter('artykul_id', openapi.IN_QUERY, description="Opcjonalny ID artykułu, aby pobrać notatki tylko dla niego.", type=openapi.TYPE_INTEGER),
        ],
        responses={
            status.HTTP_200_OK: notatki_list_schema
        }
    )
    def get(self,request):
        artykul_id = request.query_params.get('artykul_id')

        if artykul_id:
            notatki = self.service.get_by_uzytkownik_and_artykul(request.user.id,artykul_id)
        else:
            notatki = self.service.get_by_uzytkownik(request.user.id)

        if not notatki:
            return Response({"message":"Nie znaleziono notatek"}, status=status.HTTP_200_OK)
        
        return Response(NotatkaSerializer(notatki,many=True).data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="DODAWANIE: Tworzy nową notatkę.",
        request_body=NotatkaPostSerializer,
        responses={
            status.HTTP_201_CREATED: notatka_schema,
            status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych."
        }
    )
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
    """
    ZARZĄDZANIE NOTATKAMI (GET, PUT, DELETE)
    
    Pobieranie, aktualizacja i usuwanie konkretnej notatki. Wymaga by użytkownik był właścicielem notatki.
    """
    permission_classes = [IsAuthenticated]
    service = NotatkaService()
    
    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca szczegóły notatki po ID. Wymaga autoryzacji jako właściciel.",
        responses={
            status.HTTP_200_OK: notatka_schema,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono notatki.",
            status.HTTP_403_FORBIDDEN: "Brak uprawnień (nie jesteś właścicielem)."
        }
    )
    def get(self,request,id):
        notatka = self.service.get_by_id(id)
        
        if not notatka:
            return Response({"error":"Nie znaleziono notatki"},
                            status=status.HTTP_404_NOT_FOUND)
        
        if notatka['uzytkownik_id'] != request.user.id:
            return Response({"error":"Brak uprawnien"},
                            status=status.HTTP_403_FORBIDDEN)
        
        return Response(NotatkaSerializer(notatka).data,
                        status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="AKTUALIZACJA (PUT): Aktualizuje treść notatki po ID. Wymaga autoryzacji jako właściciel.",
        request_body=NotatkaPutSerializer,
        responses={
            status.HTTP_200_OK: notatka_schema,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono notatki.",
            status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych."
        }
    )
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
    
    @swagger_auto_schema(
        operation_description="USUWANIE: Usuwa notatkę po ID. Wymaga autoryzacji jako właściciel.",
        responses={
            status.HTTP_200_OK: openapi.Response(description="Notatka usunięta pomyślnie."),
            status.HTTP_404_NOT_FOUND: "Nie znaleziono notatki lub brak uprawnień."
        }
    )
    def delete(self,request,id):
        deleted = self.service.delete(id,request.user.id)

        if deleted:
            return Response({"message":"Notatka usunięta"},
                            status=status.HTTP_200_OK)
        
        return Response({"error":"Nie znaleziono notatki lub brak uprawnien"},
                        status=status.HTTP_404_NOT_FOUND)
            
class KomentarzeAPIView(APIView):
    """
    ZARZĄDZANIE KOMENTARZAMI (GET PUBLICZNY, POST ZALOGOWANY)
    
    Pobieranie wszystkich komentarzy do danego artykułu, dodawanie nowych komentarzy.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()] 
        return [IsAuthenticated()] 
    
    service = KomentarzService()
    
    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca listę wszystkich komentarzy dla artykułu.",
        responses={
            status.HTTP_200_OK: komentarze_list_schema,
            status.HTTP_404_NOT_FOUND: "Artykuł nie ma komentarzy."
        }
    )
    def get(self,request,artykul_id):

        komentarze = self.service.get_by_artykul(artykul_id)

        if not komentarze:
            return Response({"message":f"Artykuł {artykul_id} nie ma komentarzy"},
                            status=status.HTTP_404_NOT_FOUND)
        
        return Response(KomentarzSerializer(komentarze,many=True).data,
                        status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="DODAWANIE: Tworzy nowy komentarz do artykułu. Wymaga zalogowania.",
        request_body=KomentarzSerializer, # Oczekuje pola 'tresc'
        responses={
            status.HTTP_201_CREATED: komentarz_schema,
            status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych."
        }
    )
    def post(self,request,artykul_id):

        serializer = KomentarzSerializer(data = request.data)

        if serializer.is_valid():
            tresc = serializer.validated_data['tresc']

            komentarz = self.service.create(tresc,artykul_id,request.user.id)

            if not komentarz:
                return Response({"error":"Nie udalo sie dodac komentarza"}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(KomentarzSerializer(komentarz).data,
                            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class KomentarzSzczegolyAPIView(APIView):
    """
    ZARZĄDZANIE KOMENTARZAMI (GET, PUT, DELETE)
    
    Pobieranie, edycja i usuwanie konkretnego komentarza. Edycja/Usunięcie wymaga, by użytkownik był autorem lub administratorem.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]
    
    service = KomentarzService()

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca szczegóły komentarza po ID.",
        responses={
            status.HTTP_200_OK: komentarz_schema,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono komentarza."
        }
    )
    def get(self,request,id):

        komentarz = self.service.get_by_id(id)

        if not komentarz:
            return Response({"error":"Nie znaleziono komentarza"},
                            status=status.HTTP_404_NOT_FOUND)
        
        return Response(KomentarzSerializer(komentarz).data,
                        status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="AKTUALIZACJA (PUT): Aktualizuje treść komentarza. Wymaga by użytkownik był autorem.",
        request_body=KomentarzSerializer,
        responses={
            status.HTTP_200_OK: komentarz_schema,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono komentarza.",
            status.HTTP_403_FORBIDDEN: "Brak uprawnień (nie jesteś autorem)."
        }
    )
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

            komentarz = self.service.get_by_id(updated["id"])

            return Response(KomentarzSerializer(komentarz).data,
                            status=status.HTTP_200_OK)
        
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="USUWANIE: Usuwa komentarz. Wymaga by użytkownik był autorem lub administratorem.",
        responses={
            status.HTTP_200_OK: openapi.Response(description="Komentarz usunięty pomyślnie."),
            status.HTTP_404_NOT_FOUND: "Nie znaleziono komentarza.",
            status.HTTP_403_FORBIDDEN: "Brak uprawnień (nie jesteś autorem ani administratorem)."
        }
    )
    def delete(self,request,id):

        komentarz = self.service.get_by_id(id)

        if not komentarz:
            return Response({"error":"Nie znaleziono komentarza"},
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
    
class WynikiWszystkichEgzaminowAPIView(APIView):
    """
    WYNIKI EGZAMINÓW (GET LISTA)
    
    Zwraca listę wszystkich wyników egzaminów 
    """
    permission_classes = [IsAuthenticated]
    service = WynikEgzaminuService()

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca listę wszystkich wyników egzaminów użytkownika. Opcjonalnie filtruje po kurs_id.",
        manual_parameters=[
            openapi.Parameter('kurs_id', openapi.IN_QUERY, description="Opcjonalny ID kursu do filtrowania wyników.", type=openapi.TYPE_INTEGER),
        ],
        responses={
            status.HTTP_200_OK: wyniki_list_schema
        }
    )
    def get(self, request):
        kurs_id = request.query_params.get('kurs_id')
        
        if kurs_id:
            wyniki = self.service.get_all_by_kurs(kurs_id)
        else:
            wyniki = self.service.get_all()
        
        if not wyniki:
            return Response(
                {"message": "Brak wyników egzaminów"},
                status=status.HTTP_200_OK
            )
        
        return Response(
            WynikiEgzaminuSerializer(wyniki, many=True).data,
            status=status.HTTP_200_OK
        )

class WynikiEgzaminuAPIView(APIView):
    """
    WYNIKI EGZAMINÓW (GET LISTA)
    
    Zwraca listę wszystkich wyników egzaminów zalogowanego użytkownika, 
    opcjonalnie filtruje po kursie.
    """
    permission_classes = [IsAuthenticated]
    service = WynikEgzaminuService()

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca listę wszystkich wyników egzaminów zalogowanego użytkownika. Opcjonalnie filtruje po kurs_id.",
        manual_parameters=[
            openapi.Parameter('kurs_id', openapi.IN_QUERY, description="Opcjonalny ID kursu do filtrowania wyników.", type=openapi.TYPE_INTEGER),
        ],
        responses={
            status.HTTP_200_OK: wyniki_list_schema
        }
    )
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
    """
    WYNIK EGZAMINU (GET SZCZEGÓŁY)
    
    Pobiera szczegóły pojedynczego wyniku egzaminu. Wymaga autoryzacji jako właściciel.
    """
    permission_classes = [IsAuthenticated]
    service = WynikEgzaminuService()

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca szczegóły pojedynczego wyniku egzaminu po ID.",
        responses={
            status.HTTP_200_OK: wynik_egzaminu_schema,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono wyniku.",
            status.HTTP_403_FORBIDDEN: "Brak uprawnień."
        }
    )
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
    """
    ŚREDNIA WYNIKÓW UŻYTKOWNIKA W KURSIE
    
    Oblicza i zwraca średni wynik zalogowanego użytkownika w danym kursie.
    """
    permission_classes = [IsAuthenticated]
    service = WynikEgzaminuService()

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca średni wynik osiągnięty przez zalogowanego użytkownika w danym kursie.",
        responses={
            status.HTTP_200_OK: openapi.Response("Średnia wynikowa.", AverageUzytkownikKursSerializer)
        }
    )
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
    """
    GLOBALNA ŚREDNIA WYNIKÓW KURSU
    
    Oblicza i zwraca średni wynik osiągnięty przez wszystkich użytkowników w danym kursie.
    """
    permission_classes = [IsAuthenticated] 
    service = WynikEgzaminuService()

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca globalną średnią wyników osiągniętych w danym kursie przez wszystkich użytkowników.",
        responses={
            status.HTTP_200_OK: openapi.Response("Średnia wynikowa kursu.", AverageKursSerializer)
        }
    )
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
    """
    OCENIANIE ARTYKUŁÓW (GET PUBLICZNY, POST/PUT/DELETE ZALOGOWANY)
    
    Zarządzanie oceną artykułu przez użytkownika oraz pobieranie średniej ocen.
    """
    service = OcenaArtykuluService()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca średnią ocenę artykułu (publiczną) oraz opcjonalnie ocenę zalogowanego użytkownika (moja_ocena).",
        responses={
            status.HTTP_200_OK: openapi.Response("Dane o ocenie.", OcenaArtykuluCombinedSerializer)
        }
    )
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

    @swagger_auto_schema(
        operation_description="DODAWANIE/AKTUALIZACJA (POST/PUT): Tworzy nową ocenę lub aktualizuje istniejącą (w zakresie 1-5).",
        request_body=OcenaArtykuluInputSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response("Ocena zapisana.", OcenaArtykuluSerializer),
            status.HTTP_400_BAD_REQUEST: "Błąd walidacji lub zakresu oceny."
        }
    )
    def post(self, request, artykul_id):
        serializer = OcenaArtykuluInputSerializer(data=request.data)
        
        if serializer.is_valid():
            ocena = serializer.validated_data['ocena']
            
            ocena_obiekt = self.service.utworz_lub_aktualizuj_ocene(artykul_id, ocena, request.user.id)
            
            if ocena_obiekt:
                return Response(OcenaArtykuluSerializer(ocena_obiekt).data, status=status.HTTP_201_CREATED)
            
            return Response({"error": "Nie udało się zapisać oceny."}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
    operation_description="AKTUALIZACJA (PUT): Aktualizuje istniejącą ocenę (1-5).",
    request_body=OcenaArtykuluInputSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response("Ocena zaktualizowana.", OcenaArtykuluSerializer),
        status.HTTP_400_BAD_REQUEST: "Błąd walidacji."
    }
)
    def put(self, request, artykul_id):
        return self.post(request, artykul_id)


    @swagger_auto_schema(
        operation_description="USUWANIE: Usuwa ocenę wystawioną przez zalogowanego użytkownika.",
        responses={
            status.HTTP_200_OK: openapi.Response(description="Ocena usunięta pomyślnie."),
            status.HTTP_404_NOT_FOUND: "Nie znaleziono oceny."
        }
    )
    def delete(self, request, artykul_id):
        usunieto = self.service.usun_ocene(artykul_id, request.user.id)
        
        if usunieto:
            return Response({"message": "Ocena usunięta."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Nie znaleziono oceny do usunięcia."}, status=status.HTTP_404_NOT_FOUND)

class ProgressPytanAPIView(APIView):
    """
    POSTĘP PYTAŃ (PROGRESS BAR)
    
    Zwraca szczegółowy postęp użytkownika w kursie oraz dane do wyświetlenia paska postępu.
    """

    permission_classes = [IsAuthenticated]
    service = ProgressPytanService()

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca szczegółowy postęp użytkownika w pytaniach z danego kursu oraz podsumowanie z % ukończenia.",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Postęp użytkownika w kursie.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'lista_postepu': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_OBJECT),
                            description="Lista statusów poszczególnych pytań"
                        ),
                        'podsumowanie': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'total_questions': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'completed_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'progress_percentage': openapi.Schema(type=openapi.TYPE_NUMBER, description='Procent ukończonych pytań')
                            }
                        )
                    }
                )
            )
        }
    )
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
    

class TrybNaukiAPIView(APIView):
    """
    POBIERANIE PYTAŃ DO TRYBU NAUKI
    
    Zwraca optymalną listę pytań do powtarzania z priorytetem na błędy użytkownika.
    Pytania są oznaczane jako Wyświetlone ('W') przy pobieraniu.
    """

    permission_classes = [IsAuthenticated]
    service = TrybNaukiService()

    @swagger_auto_schema(
        operation_description="POBIERANIE: Pobiera zoptymalizowaną listę pytań do nauki dla danego kursu. Pytania są oznaczane jako W (Wyświetlone).",
        responses={
            status.HTTP_200_OK: openapi.Response("Lista pytań do nauki.", PytanieTrybNaukiSerializer(many=True)),
            status.HTTP_200_OK: openapi.Response(description="Brak pytań do nauki w tym kursie.")
        }
    )
    def get(self, request, kurs_id):
        pytania = self.service.pobierz_pytania_dla_kursu(kurs_id, request.user.id)
        
        if not pytania:
            return Response({"message": "Brak pytań do nauki w tym kursie."}, status=status.HTTP_200_OK)

        for p in pytania:
             self.service.oznacz_jako_wyswietlone(p['pytanie_id'], request.user.id)
             p['status_uzytkownika'] = 'W' 

        return Response(PytanieTrybNaukiSerializer(pytania, many=True).data, status=status.HTTP_200_OK)
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
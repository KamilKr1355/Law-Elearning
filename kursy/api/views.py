from rest_framework.response import Response
from django.db import connection
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework import status
from .serializers import(KursSerializer,ArtykulViewSerializer,
                         ArtykulSerializer,
                         RozdzialSerializer,PytaniaSerializer,OdpowiedziSerializer)
from rest_framework.views import APIView
from kursy.services.kurs_service import KursService
from kursy.services.artykul_service import ArtykulService
from kursy.services.rozdzial_service import RozdzialService
from kursy.services.pytanie_service import PytaniaService
from kursy.services.odpowiedzi_service import OdpowiedziService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

kurs_schema_response = openapi.Response("Szczegóły kursu.", KursSerializer)
lista_kursow_schema_response = openapi.Response("Lista kursów.", KursSerializer(many=True))

artykul_schema_response = openapi.Response("Szczegóły artykulu.", ArtykulSerializer)
lista_artykulow_schema_response = openapi.Response("Lista kursów.", ArtykulSerializer(many=True))
artykulView_schema_response = openapi.Response("Szczegóły artykulu.", ArtykulViewSerializer)
lista_artykulowView_schema_response = openapi.Response("Lista kursów.", ArtykulViewSerializer(many=True))

rozdzial_schema_response = openapi.Response("Szczegóły rozdziału.", RozdzialSerializer)
lista_rozdzial_schema_response = openapi.Response("Lista rozdziałów.", RozdzialSerializer(many=True))

pytania_schema_response = openapi.Response("Szczegóły pytania.", PytaniaSerializer)
lista_pytania_schema_response = openapi.Response("Lista pytań.", PytaniaSerializer(many=True))

odpowiedzi_schema_response = openapi.Response("Szczegóły odpowiedzi.", OdpowiedziSerializer)
lista_odpowiedzi_schema_response = openapi.Response("Lista odpowiedzi.", OdpowiedziSerializer(many=True))


class KursyAPIView(APIView):
    """
    ZARZĄDZANIE KURSAMI (ADMIN / PUBLIC)
    
    Endpointy umożliwiają przeglądanie dostępnych kursów przez wszystkich użytkowników (GET), 
    a także dodawanie przez administratorów (POST).
    
    Publiczne trasy: GET (lista).
    Trasy administracyjne: POST.
    """

    service = KursService()
    serializer_class = KursSerializer

    def get_permissions(self):
        if self.request.method in ["POST"]:
            return [IsAdminUser()]
        return [AllowAny()]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca listę wszystkich kursów.",
        responses={
            status.HTTP_200_OK: lista_kursow_schema_response,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono żadnego kursu"
        }
    )
    def get(self, request):
        kursy = self.service.list_all()
        if not kursy:
            return Response({"error": "Nie znaleziono kursu"}, status=status.HTTP_404_NOT_FOUND)
        return Response(KursSerializer(kursy, many=True).data)

    @swagger_auto_schema(
            operation_description="DODAWANIE (ADMIN): Tworzy nowy kurs. Wymaga statusu administratora",
            request_body=KursSerializer,
            responses={
                status.HTTP_201_CREATED: kurs_schema_response,
                status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych wejściowych"
            }
    )
    def post(self, request):
        serializer = KursSerializer(data=request.data)
        if serializer.is_valid():
            nazwa = serializer.validated_data["nazwa_kursu"]
            kurs = self.service.create(nazwa)
            return Response(KursSerializer(kurs).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class KursySzczegolyAPIView(APIView):

    """
    ZARZĄDZANIE KURSEM (ADMIN / PUBLIC)
    
    Endpointy umożliwiają przeglądanie konkretnego kursu przez wszystkich użytkowników (GET), 
    a także modyfikowanie i usuwanie kursów przez administratorów (PUT, DELETE).
    
    Publiczne trasy: GET (szczegóły).
    Trasy administracyjne: PUT, DELETE.
    """

    service = KursService()
    serializer_class = KursSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca szczegóły pojedynczego kursu",
        responses={
            status.HTTP_200_OK: lista_kursow_schema_response,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono kursu"
        }
    )
    def get(self, request,id):
        kurs = self.service.get_one(id)
        if not kurs:
            return Response({"error": "Nie znaleziono kursu"}, status=status.HTTP_404_NOT_FOUND)
        return Response(KursSerializer(kurs).data)


    @swagger_auto_schema(
            operation_description="AKTUALIZOWANIE (ADMIN): Modyfikuje istniejący kurs po ID, wymaga uprawnień administratora",
            request_body=KursSerializer,
            responses={
                status.HTTP_200_OK: kurs_schema_response,
                status.HTTP_404_NOT_FOUND: "Nie znaleziono kursu",
                status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych"
            }
    )
    def put(self, request, id):
        serializer = KursSerializer(data=request.data)
        if serializer.is_valid():
            nazwa = serializer.validated_data["nazwa_kursu"]
            kurs = self.service.update(id, nazwa)
            if not kurs:
                return Response({"error": "Nie znaleziono kursu"}, status=status.HTTP_404_NOT_FOUND)
            return Response(KursSerializer(kurs).data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
            operation_description="USUWANIE (ADMIN): Usuwa istniejący kurs po ID, wymaga uprawnień administratora",
            responses={
                status.HTTP_200_OK: openapi.Response(description="Kurs usunięty pomyślnie."),
                status.HTTP_404_NOT_FOUND: "Nie znaleziono kursu."
            }
    )
    def delete(self, request, id):
        ok = self.service.delete(id)
        if not ok:
            return Response({"error": "Nie znaleziono kursu"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": f"Kurs {id} usunięty"},status=status.HTTP_200_OK)


"""
TODO: Walidacja w serializerze czy dodawany artykul z konkretnego rozdzialu faktycznie jest w kursie
"""
class ArtykulyAPIView(APIView):
    """
    ZARZĄDZANIE ARTYKULAMI (ADMIN / PUBLIC)
    
    Endpointy umożliwiają przeglądanie wszystkich artykułów przez wszystkich użytkowników (GET), 
    a także tworzenie artykulow przez administratorów (POST).
    
    Publiczne trasy: GET (szczegóły).
    Trasy administracyjne: POST.
    """
    service = ArtykulService()

    def get_permissions(self):
        if self.request.method in ["POST","PUT","DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]
    #permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca liste artykułów",
        responses={
            status.HTTP_200_OK: lista_artykulowView_schema_response,
            status.HTTP_404_NOT_FOUND: "Brak artykułów"
        }
    )
    def get(self, request, kurs_id):
        artykuly = self.service.list_all(kurs_id)
        
        if not artykuly:
            return Response(
                {"error": "Brak artykułów"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(ArtykulViewSerializer(artykuly, many=True).data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
            operation_description="DODAWANIE (ADMIN): Tworzy nowy artykuł. Wymaga statusu administratora",
            request_body=ArtykulSerializer,
            responses={
                status.HTTP_201_CREATED: artykul_schema_response,
                status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych wejściowych"
            }
    )
    def post(self,request,kurs_id):
        serializer = ArtykulSerializer(data=request.data)
        if serializer.is_valid():
            tresc = serializer.validated_data["tresc"]
            tytul = serializer.validated_data["tytul"]
            nr_artykulu = serializer.validated_data["nr_artykulu"]
            rozdzial_id = serializer.validated_data["rozdzial_id"]
            kurs_id = kurs_id

            artykul = self.service.create(tresc,tytul,nr_artykulu,rozdzial_id)

            return Response(ArtykulSerializer(artykul).data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtykulySzczegolyAPIView(APIView):
    """
    ZARZĄDZANIE ARTYKULEM (ADMIN / PUBLIC)
    
    Endpointy umożliwiają przeglądanie konkretnego artykulu przez wszystkich użytkowników (GET), 
    a także modyfikowanie i usuwanie artykulow przez administratorów (PUT, DELETE).
    
    Publiczne trasy: GET (szczegóły).
    Trasy administracyjne: PUT, DELETE.
    """
    service = ArtykulService()

    def get_permissions(self):
        if self.request.method in ["PUT","DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]
    #permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca szczegóły artykułu po id",
        responses={
            status.HTTP_200_OK: artykulView_schema_response,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono artykułu"
        }
    )
    def get(self, request, id):
        artykul = self.service.get_one(id)
        if not artykul:
            return Response(
                {"error": "Brak artykułu"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(ArtykulViewSerializer(artykul, many=False).data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
            operation_description="AKTUALIZOWANIE (ADMIN): Aktualizuje artykuł po id. Wymaga statusu administratora",
            request_body=ArtykulSerializer,
            responses={
                status.HTTP_200_OK: artykul_schema_response,
                status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych wejściowych"
            }
    )       
    def put(self,request,id):
        serializer = ArtykulSerializer(data=request.data)
        if serializer.is_valid():
            tresc = serializer.validated_data["tresc"]
            tytul = serializer.validated_data["tytul"]
            nr_artykulu = serializer.validated_data["nr_artykulu"]
            rozdzial_id = serializer.validated_data["rozdzial_id"]

            artykul = self.service.update(tresc,tytul,nr_artykulu,rozdzial_id,id)
            return Response(ArtykulSerializer(artykul).data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
            operation_description="USUWANIE (ADMIN): Usuwanie artykułu po id. Wymaga statusu administratora",
            responses={
                status.HTTP_200_OK: openapi.Response(description="Artykuł usunięty"),
                status.HTTP_400_BAD_REQUEST: "Nie znaleziono artykułu"
            }
    )  
    def delete(self,request,id):
        deleted = self.service.delete(id)
        if deleted:
            return Response({"message": f"Artykuł {id} usunięty."}, status=status.HTTP_200_OK)
        return Response({"error": "Nie znaleziono artykułu"}, status=status.HTTP_404_NOT_FOUND)

class RozdzialyListaAPIView(APIView):
    """
    ZARZĄDZANIE ROZDZIALAMI (ADMIN / PUBLIC)
    
    Endpointy umożliwiają przeglądanie rozdziałów przez wszystkich użytkowników (GET), 
    a także tworzenie rozdziałów przez administratorów (POST).
    
    Publiczne trasy: GET.
    Trasy administracyjne: POST.
    """
    service = RozdzialService()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca liste rozdziałów dla kursu po id kursu",
        responses={
            status.HTTP_200_OK: lista_rozdzial_schema_response,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono rozdziałów"
        }
    )
    def get(self, request, kurs_id):
        rozdzialy = self.service.list_by_kurs(kurs_id)

        if not rozdzialy:
            return Response(
                {"error": "Nie znaleziono rozdziałów"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            RozdzialSerializer(rozdzialy, many=True).data,
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
            operation_description="DODAWANIE (ADMIN): Tworzy nowy rozdział. Wymaga statusu administratora",
            request_body=RozdzialSerializer,
            responses={
                status.HTTP_201_CREATED: rozdzial_schema_response,
                status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych wejściowych"
            }
    )
    def post(self, request, kurs_id):
        data = request.data.copy()
        data["kurs_id"] = kurs_id

        serializer = RozdzialSerializer(data=data)

        if serializer.is_valid():
            nazwa = serializer.validated_data["nazwa_rozdzialu"]
            rozdzial = self.service.create(nazwa, kurs_id)
            return Response(
                RozdzialSerializer(rozdzial).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RozdzialSzczegolyAPIView(APIView):
    """
    ZARZĄDZANIE ROZDZIAŁEM (ADMIN / PUBLIC)
    
    Endpointy umożliwiają przeglądanie konkretnego artykulu przez wszystkich użytkowników (GET), 
    a także  modyfikowanie i usuwanie rozdziałów przez administratorów (PUT, DELETE).
    
    Publiczne trasy: GET (szczegóły).
    Trasy administracyjne: PUT, DELETE.
    """
    service = RozdzialService()

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca szczegóły rozdziału po id",
        responses={
            status.HTTP_200_OK: rozdzial_schema_response,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono rozdziału"
        }
    )
    def get(self, request, id):
        rozdzial = self.service.get_one(id)

        if not rozdzial:
            return Response(
                {"error": "Nie znaleziono rozdziału"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            RozdzialSerializer(rozdzial).data,
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
            operation_description="AKTUALIZOWANIE (ADMIN): Aktualizuje rozdział po id. Wymaga statusu administratora",
            request_body=RozdzialSerializer,
            responses={
                status.HTTP_200_OK: rozdzial_schema_response,
                status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych wejściowych"
            }
    ) 
    def put(self, request, id):
        serializer = RozdzialSerializer(data=request.data)

        if serializer.is_valid():
            nazwa = serializer.validated_data["nazwa_rozdzialu"]
            kurs_id = serializer.validated_data["kurs_id"]

            updated = self.service.update(id, nazwa, kurs_id)

            if not updated:
                return Response(
                    {"error": "Nie znaleziono rozdziału"},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                RozdzialSerializer(updated).data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
            operation_description="USUWANIE (ADMIN): Usuwanie rozdziału po id. Wymaga statusu administratora",
            responses={
                status.HTTP_200_OK: openapi.Response(description="Rozdział usunięty"),
                status.HTTP_400_BAD_REQUEST: "Nie znaleziono rozdziału"
            }
    )  
    def delete(self, request, id):
        deleted = self.service.delete(id)

        if deleted:
            return Response(
                {"message": f"Rozdział {id} usunięty."},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Nie znaleziono rozdziału"},
            status=status.HTTP_404_NOT_FOUND
        )
            
class PytaniaAPIView(APIView):
    """
    ZARZĄDZANIE PYTANIAMI (ADMIN / PUBLIC)
    
    Endpointy umożliwiają przeglądanie wszystkich pytań przez zalogowanych użytkowników (GET), 
    a także tworzenie pytań przez administratorów (POST).
    
    Publiczne trasy: GET.
    Trasy administracyjne: POST.
    """
    service = PytaniaService()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca wszystkie pytania",
        responses={
            status.HTTP_200_OK: lista_pytania_schema_response,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono pytań"
        }
    )
    def get(self, request):
        pytania = self.service.list_all()

        if pytania:
            return Response(PytaniaSerializer(pytania, many=True).data,status=status.HTTP_200_OK)

        return Response(
                {"error": "Nie znaleziono pytań"},
                status=status.HTTP_404_NOT_FOUND
            )


    @swagger_auto_schema(
            operation_description="DODAWANIE (ADMIN): Tworzy nowe pytanie. Wymaga statusu administratora",
            request_body=PytaniaSerializer,
            responses={
                status.HTTP_201_CREATED: pytania_schema_response,
                status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych wejściowych"
            }
    )
    def post(self, request):
        serializer = PytaniaSerializer(data=request.data)
        if serializer.is_valid():
            tresc = serializer.validated_data["tresc"]
            artykul_id = serializer.validated_data["artykul_id"]

            pytanie = self.service.create(tresc, artykul_id)
            return Response(PytaniaSerializer(pytanie).data,status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PytaniaArtykulAPIView(APIView):
    """
    ZARZĄDZANIE PYTANIAMI KONKRETNEGO ARTYKUŁU (ADMIN / PUBLIC)
    
    Endpointy umożliwiają przeglądanie wszystkich pytań przypisanych do danego artykułu przez wszystkich użytkowników (GET), 
    
    Publiczne trasy: GET.
    """
    service = PytaniaService()
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca wszystkie pytania konkretnego artykułu",
        responses={
            status.HTTP_200_OK: lista_pytania_schema_response,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono pytań"
        }
    )
    def get(self, request, artykul_id):
        pytania = self.service.get_artykul_id(artykul_id)
        if not pytania:
            return Response({"error": "Brak pytań"}, status=status.HTTP_404_NOT_FOUND)
        return Response(PytaniaSerializer(pytania, many=True).data,status=status.HTTP_200_OK)

class PytanieSzczegolyAPIView(APIView):
    """
    ZARZĄDZANIE KONKRETNYM PYTANIEM (ADMIN / PUBLIC)
    
    Endpointy umożliwiają przeglądanie wszystkich pytań przez zalogowanych użytkowników (GET), 
    a także edytowanie i usuwanie pytań przez administratorów (PUT, DELETE).
    
    Publiczne trasy: GET.
    Trasy administracyjne: PUT,DELETE.
    """
    service = PytaniaService()

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca szczegóły pytania id",
        responses={
            status.HTTP_200_OK: pytania_schema_response,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono pytania"
        }
    )
    def get(self, request, id):
        pytanie = self.service.get(id)
        if not pytanie:
            return Response({"error": "Nie znaleziono pytania"}, status=status.HTTP_404_NOT_FOUND)
        return Response(PytaniaSerializer(pytanie).data)

    @swagger_auto_schema(
            operation_description="AKTUALIZOWANIE (ADMIN): Aktualizuje pytanie po id. Wymaga statusu administratora",
            request_body=PytaniaSerializer,
            responses={
                status.HTTP_200_OK: pytania_schema_response,
                status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych wejściowych"
            }
    ) 
    def put(self, request, id):
        serializer = PytaniaSerializer(data=request.data)
        if serializer.is_valid():
            tresc = serializer.validated_data["tresc"]
            artykul_id = serializer.validated_data["artykul_id"]

            updated = self.service.update(id, tresc, artykul_id)
            return Response(PytaniaSerializer(updated).data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
            operation_description="USUWANIE (ADMIN): Usuwanie pytania po id. Wymaga statusu administratora",
            responses={
                status.HTTP_200_OK: openapi.Response(description="Pytanie usunięte"),
                status.HTTP_400_BAD_REQUEST: "Nie znaleziono pytania"
            }
    ) 
    def delete(self, request, id):
        deleted = self.service.delete(id)
        if deleted:
            return Response({"message": f"Pytanie {id} usunięte."})
        return Response({"error": "Nie znaleziono pytania"}, status=404)
    
class OdpowiedziSzczegolyAPIView(APIView):
    """
    ZARZĄDZANIE ODPOWIEDZIAMI (ADMIN / PUBLIC)
    
    Endpointy umożliwiają przeglądanie konkretnej odpowiedzi przez zalogowanych użytkowników (GET), 
    a także  modyfikowanie i usuwanie odpowiedzi przez administratorów (PUT, DELETE).
    
    Publiczne trasy: GET (szczegóły).
    Trasy administracyjne: PUT, DELETE.
    """
    service = OdpowiedziService()

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca szczegóły odpowiedzi po id",
        responses={
            status.HTTP_200_OK: odpowiedzi_schema_response,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono odpowiedzi"
        }
    )
    def get(self, request,id):
        odpowiedz = self.service.get(id)
        if not odpowiedz:
            return Response({"error": "Nie znaleziono odpowiedzi"}, status=status.HTTP_404_NOT_FOUND)
        return Response(OdpowiedziSerializer(odpowiedz,many=False).data,status=status.HTTP_200_OK)

    @swagger_auto_schema(
            operation_description="AKTUALIZOWANIE (ADMIN): Aktualizuje odpowiedzi po id. Wymaga statusu administratora",
            request_body=OdpowiedziSerializer,
            responses={
                status.HTTP_200_OK: odpowiedzi_schema_response,
                status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych wejściowych",
                status.HTTP_404_NOT_FOUND: "Nie znaleziono odpowiedzi"
            }
    ) 
    def put(self, request, id):
        serializer = OdpowiedziSerializer(data=request.data)
        if serializer.is_valid():
            tresc = serializer.validated_data["tresc"]
            poprawna = serializer.validated_data["poprawna"]
            pytanie_id = serializer.validated_data["pytanie_id"]

            odpowiedz = self.service.update(id,tresc,poprawna,pytanie_id)

            if not odpowiedz:
                return Response({"error": "Nie znaleziono odpowiedzi"}, status=status.HTTP_404_NOT_FOUND)
            
            return Response(OdpowiedziSerializer(odpowiedz).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
            operation_description="USUWANIE (ADMIN): Usuwanie odpowiedz po id. Wymaga statusu administratora",
            responses={
                status.HTTP_200_OK: openapi.Response(description="Odpowiedz usunięta"),
                status.HTTP_404_NOT_FOUND: "Nie znaleziono odpowiedzi"
            }
    ) 
    def delete(self, request, id):
        deleted = self.service.delete(id)
        if deleted:
            return Response({"message": f"Odpowiedz {id} usunięta."})
        return Response({"error": "Nie znaleziono odpowiedzi"}, status=status.HTTP_404_NOT_FOUND)

class OdpowiedziAPIView(APIView):
    """
    ZARZĄDZANIE ODPOWIEDZIAMI (ADMIN / PUBLIC)
    
    Endpointy umożliwiają przeglądanie odpowiedzi do konkretnego pytania przez zalogowanych użytkowników (GET), 
    a także tworzenie odpowiedzi przez administratorów (POST).
    
    Publiczne trasy: GET.
    Trasy administracyjne: POST.
    """
    service = OdpowiedziService()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
            operation_description="DODAWANIE (ADMIN): Tworzy nowa odpowiedz. Wymaga statusu administratora",
            request_body=OdpowiedziSerializer,
            responses={
                status.HTTP_201_CREATED: pytania_schema_response,
                status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych wejściowych"
            }
    )
    def post(self, request):
        serializer = OdpowiedziSerializer(data=request.data)
        if serializer.is_valid():
            tresc = serializer.validated_data["tresc"]
            poprawna = serializer.validated_data["poprawna"]
            pytanie_id = serializer.validated_data["pytanie_id"]

            odpowiedz = self.service.create(tresc,poprawna,pytanie_id)
            return Response(OdpowiedziSerializer(odpowiedz).data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OdpowiedziPytaniaAPIView(APIView):
    """
    ZARZĄDZANIE ODPOWIEDZIAMI (ADMIN / PUBLIC)
    
    Endpointy umożliwiają przeglądanie odpowiedzi do konkretnego pytania przez zalogowanych użytkowników (GET), 
    a także tworzenie odpowiedzi przez administratorów (POST).
    
    Publiczne trasy: GET.
    Trasy administracyjne: POST.
    """
    service = OdpowiedziService()

    def get_permissions(self):
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="POBIERANIE: Zwraca wszystkie odpowiedzi do id pytania",
        responses={
            status.HTTP_200_OK: lista_odpowiedzi_schema_response,
            status.HTTP_404_NOT_FOUND: "Nie znaleziono odpowiedzi"
        }
    )
    def get(self,request,pytanie_id):
        odpowiedz = self.service.get_pytanie_id(pytanie_id)

        if not odpowiedz:
            return Response({"error": "Nie znaleziono odpowiedzi"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(OdpowiedziSerializer(odpowiedz,many=True).data,status=status.HTTP_200_OK)







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
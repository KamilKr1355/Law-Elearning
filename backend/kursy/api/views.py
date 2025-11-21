from rest_framework.response import Response
from django.db import connection
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework import status
from .serializers import(KursSerializer,ArtykulViewSerializer,
                         ArtykulSerializer,
                         RozdzialSerializer)
from rest_framework.views import APIView
from kursy.services.kurs_service import KursService
from kursy.services.artykul_service import ArtykulService
from kursy.services.rozdzial_service import RozdzialService



class KursyAPIView(APIView):

    service = KursService()

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request, id=None):
        if id:
            kurs = self.service.get_one(id)
            if not kurs:
                return Response({"error": "Nie znaleziono kursu"}, status=404)
            return Response(KursSerializer(kurs).data)

        kursy = self.service.list_all()
        if not kursy:
            return Response({"error": "Nie znaleziono kursu"}, status=404)
        return Response(KursSerializer(kursy, many=True).data)

    def post(self, request):
        serializer = KursSerializer(data=request.data)
        if serializer.is_valid():
            nazwa = serializer.validated_data["nazwa_kursu"]
            kurs = self.service.create(nazwa)
            return Response(KursSerializer(kurs).data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, id):
        serializer = KursSerializer(data=request.data)
        if serializer.is_valid():
            nazwa = serializer.validated_data["nazwa_kursu"]
            kurs = self.service.update(id, nazwa)
            if not kurs:
                return Response({"error": "Nie znaleziono kursu"}, status=404)
            return Response(KursSerializer(kurs).data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        ok = self.service.delete(id)
        if not ok:
            return Response({"error": "Nie znaleziono kursu"}, status=404)
        return Response({"message": f"Kurs {id} usunięty"})


class ArtykulyAPIview(APIView):

    service = ArtykulService()

    def get_permissions(self):
        if self.request.method in ["POST","PUT","DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]
    #permission_classes = [IsAuthenticated]


    def get(self, request, id=None):
        if id:
            artykul = self.service.get_one(id)
            if not artykul:
                return Response(
                    {"error": "Brak artykułów"},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(ArtykulViewSerializer(artykul, many=False).data)
        else:
            artykuly = self.service.list_all()
        
            if not artykuly:
                return Response(
                    {"error": "Brak artykułów"},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(ArtykulViewSerializer(artykuly, many=True).data)
    
    def post(self,request):
        serializer = ArtykulSerializer(data=request.data)
        if serializer.is_valid():
            tresc = serializer.validated_data["tresc"]
            tytul = serializer.validated_data["tytul"]
            nr_artykulu = serializer.validated_data["nr_artykulu"]
            rozdzial_id = serializer.validated_data["rozdzial_id"]

            artykul = self.service.create(tresc,tytul,nr_artykulu,rozdzial_id)

            return Response(ArtykulSerializer(artykul).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def put(self,request,id):
        serializer = ArtykulSerializer(data=request.data)
        if serializer.is_valid():
            tresc = serializer.validated_data["tresc"]
            tytul = serializer.validated_data["tytul"]
            nr_artykulu = serializer.validated_data["nr_artykulu"]
            rozdzial_id = serializer.validated_data["rozdzial_id"]

            artykul = self.service.update(tresc,tytul,nr_artykulu,rozdzial_id,id)
            return Response(ArtykulSerializer(artykul).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        deleted = self.service.delete(id)
        if deleted:
            return Response({"message": f"Artykuł {id} usunięty."}, status=status.HTTP_200_OK)
        return Response({"error": "Nie znaleziono artykułu"}, status=status.HTTP_404_NOT_FOUND)


class RozdzialyListaAPIView(APIView):
    service = RozdzialService()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request, kurs_id):
        rozdzialy = self.service.list_by_kurs(kurs_id)

        if not rozdzialy:
            return Response(
                {"error": "Nie znaleziono rozdziałów"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            RozdzialSerializer(reversed(rozdzialy), many=True).data,
            status=status.HTTP_200_OK
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
    service = RozdzialService()

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

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
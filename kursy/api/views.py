from rest_framework.response import Response
from django.db import connection
import random
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import(KursSerializer,ArtykulViewSerializer,
                         ArtykulSerializer,PytanieSerializer,
                         RozdzialSerializer)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework_simplejwt.views import TokenObtainPairView 
from rest_framework.views import APIView


class KursyAPIview(APIView):
    """GET - lista kursów
       POST - dodanie kursu tylko dla admina
    """

    def get_permissions(self):
        if self.request.method in ["POST","PUT","DELETE"]:
            return [IsAdminUser()]
        else:
            return [AllowAny()]

    def get(self, request, id=None):
        if id:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM kursy_kurs WHERE id=%s;", [id])
                row = cursor.fetchone()

            if not row:
                return Response({"error": "Nie znaleziono kursu"}, status=status.HTTP_404_NOT_FOUND)

            kurs = {"id": row[0], "nazwa_kursu": row[1]}
            return Response(KursSerializer(kurs).data, status=status.HTTP_200_OK)
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nazwa_kursu FROM kursy_kurs;")
            rows = cursor.fetchall()

        if not rows:
            return Response({"error": "Brak kursów"}, status=status.HTTP_404_NOT_FOUND)

        kursy = [{"id": r[0], "nazwa_kursu": r[1]} for r in rows]
        serializer = KursSerializer(kursy, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = KursSerializer(data=request.data)
        if serializer.is_valid():
            nazwa_kursu = serializer.validated_data["nazwa_kursu"]

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO kursy_kurs (nazwa_kursu) VALUES (%s) RETURNING id;",
                    [nazwa_kursu]
                )
                new_id = cursor.fetchone()[0]

            kurs = {"id": new_id, "nazwa_kursu": nazwa_kursu}
            return Response(KursSerializer(kurs).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,id):
        serializer = KursSerializer(data=request.data)
        if serializer.is_valid():
            nazwa_kursu = serializer.validated_data["nazwa_kursu"]

            with connection.cursor() as cursor:
                cursor.execute("""
                                UPDATE kursy_kurs SET nazwa_kursu=%s 
                                WHERE id=%s;
                               """,[nazwa_kursu,id])
                kurs = {"id":id,"nazwa_kursu":nazwa_kursu}
            return Response(KursSerializer(kurs).data)
        return Response({"error":"Niepoprawne dane"},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        with connection.cursor() as cursor:
            cursor.execute("""
                            DELETE from kursy_kurs where id=%s RETURNING id;
                           """,[id])
            row = cursor.fetchone()
        if row:
            return Response({"message":f"Kurs o id {id} zostal usuniety"},status=status.HTTP_200_OK)
        return Response({"error":f"Nie znaleziono kursu o id {id}"},status=status.HTTP_404_NOT_FOUND)


class ArtykulyAPIview(APIView):
    def get_permissions(self):
        if self.request.method in ["POST","PUT","DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]
    #permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT artykul_id,tresc,nazwa_kursu,id FROM artykul_kurs_view WHERE id=%s;",
                    [id]
                )
                rows = cursor.fetchall()
        else:
            with connection.cursor() as cursor:
                cursor.execute("SELECT artykul_id,tresc,nazwa_kursu,id FROM artykul_kurs_view;")
                rows = cursor.fetchall()
        
        if not rows:
            return Response(
                {"error": "Brak artykułów"},
                status=status.HTTP_404_NOT_FOUND
            )

        artykuly = [
            {"artykul_id": r[0], "tresc": r[1], "nazwa_kursu": r[2], "id": r[3]}
            for r in rows
        ]
        return Response(ArtykulViewSerializer(artykuly, many=True).data)
    
    def post(self,request):
        serializer = ArtykulSerializer(data=request.data)
        if serializer.is_valid():
            tresc = serializer.validated_data["tresc"]
            tytul = serializer.validated_data["tytul"]
            nr_artykulu = serializer.validated_data["nr_artykulu"]
            rozdzial_id = serializer.validated_data["rozdzial_id"]

            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM kursy_rozdzial WHERE id=%s;", [rozdzial_id])
                if not cursor.fetchone():
                    return Response(
                        {"error": f"Rozdział o id {rozdzial_id} nie istnieje"},
                        status=status.HTTP_404_NOT_FOUND
                    )

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO kursy_artykul (tresc,tytul,nr_artykulu,rozdzial_id)
                        VALUES (%s, %s, %s, %s) RETURNING id;
                    """,[tresc,tytul,nr_artykulu,rozdzial_id]
                )

                artykul = {"tresc":tresc,"tytul":tytul,"nr_artykulu":nr_artykulu,"rozdzial_id":rozdzial_id}
            return Response(ArtykulSerializer(artykul).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def put(self,request,id):
        serializer = ArtykulSerializer(data=request.data)
        if serializer.is_valid():
            tresc = serializer.validated_data["tresc"]
            tytul = serializer.validated_data["tytul"]
            nr_artykulu = serializer.validated_data["nr_artykulu"]
            rozdzial_id = serializer.validated_data["rozdzial_id"]

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                        UPDATE kursy_artykul SET tresc=%s, tytul=%s,nr_artykulu=%s,rozdzial_id=%s
                        WHERE id = %s;
                    """,[tresc,tytul,nr_artykulu,rozdzial_id,id]
                )

            artykul = {"tresc":tresc,"tytul":tytul,"nr_artykulu":nr_artykulu,"rozdzial_id":rozdzial_id}
            return Response(ArtykulSerializer(artykul).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        with connection.cursor() as cursor:
            cursor.execute("""
                            DELETE FROM kursy_artykul WHERE id=%s RETURNING id;
                           """, [id])
            deleted = cursor.fetchone()
        if deleted:
            return Response({"message": f"Artykuł {id} usunięty."}, status=status.HTTP_200_OK)
        return Response({"error": "Nie znaleziono artykułu"}, status=status.HTTP_404_NOT_FOUND)


class RozdzialyListaAPIview(APIView):
    """
    GET /kursy/<kurs_id>/rozdzialy/ - lista rozdziałów kursu
    POST /kursy/<kurs_id>/rozdzialy/ - dodaj nowy rozdział do kursu
    """
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get(self, request, kurs_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nazwa_rozdzialu, kurs_id 
                FROM kursy_rozdzial
                WHERE kurs_id=%s;
            """, [kurs_id])
            rozdzialy = [
                {"id": r[0], "nazwa_rozdzialu": r[1], "kurs_id": r[2]} 
                for r in cursor.fetchall()
            ]
            
        if not rozdzialy:
            return Response(
                {"error": "Nie znaleziono rozdziałów"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = RozdzialSerializer(rozdzialy, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, kurs_id):
        data = request.data.copy()
        data['kurs_id'] = kurs_id  
        
        serializer = RozdzialSerializer(data=data)
        if serializer.is_valid():
            nazwa_rozdzialu = serializer.validated_data["nazwa_rozdzialu"]
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO kursy_rozdzial (nazwa_rozdzialu, kurs_id) 
                    VALUES (%s, %s) RETURNING id;
                """, [nazwa_rozdzialu, kurs_id])
                
                new_id = cursor.fetchone()[0]

            rozdzial = {
                "id": new_id, 
                "nazwa_rozdzialu": nazwa_rozdzialu, 
                "kurs_id": kurs_id
            }
            return Response(
                RozdzialSerializer(rozdzial).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RozdzialSzczegolyAPIview(APIView):
    """
    GET /kursy/rozdzialy/<id>/ - szczegóły rozdziału
    PUT /kursy/rozdzialy/<id>/ - edytuj rozdział
    DELETE /kursy/rozdzialy/<id>/ - usuń rozdział
    """
    
    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get(self, request, id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nazwa_rozdzialu, kurs_id 
                FROM kursy_rozdzial
                WHERE id=%s;
            """, [id])
            row = cursor.fetchone()
        
        if not row:
            return Response(
                {"error": "Nie znaleziono rozdziału"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        rozdzial = {
            "id": row[0], 
            "nazwa_rozdzialu": row[1], 
            "kurs_id": row[2]
        }
        return Response(
            RozdzialSerializer(rozdzial).data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, id):
        serializer = RozdzialSerializer(data=request.data)
        
        if serializer.is_valid():
            nazwa_rozdzialu = serializer.validated_data["nazwa_rozdzialu"]
            kurs_id = serializer.validated_data["kurs_id"]
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE kursy_rozdzial 
                    SET nazwa_rozdzialu=%s, kurs_id=%s 
                    WHERE id=%s
                    RETURNING id;
                """, [nazwa_rozdzialu, kurs_id, id])
                
                updated = cursor.fetchone()
            
            if not updated:
                return Response(
                    {"error": "Nie znaleziono rozdziału"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            rozdzial = {
                "id": id, 
                "nazwa_rozdzialu": nazwa_rozdzialu, 
                "kurs_id": kurs_id
            }
            return Response(
                RozdzialSerializer(rozdzial).data,
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM kursy_rozdzial 
                WHERE id=%s 
                RETURNING id;
            """, [id])
            deleted = cursor.fetchone()
        
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
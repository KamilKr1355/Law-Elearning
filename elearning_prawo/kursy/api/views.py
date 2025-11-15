from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import connection
from .serializers import CosSerializer,UserSerializer,UserSerializerWithToken
import random
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework_simplejwt.views import TokenObtainPairView 

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self,attrs):
        data = super().validate(attrs)
        
        serializer = UserSerializerWithToken(self.user).data

        for k,v in serializer.items():
            data[k] = v

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['message'] = 'hello world'
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user

    serializer = UserSerializer(user,many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):
    data = request.data

    try:
        user = User.objects.create(
            first_name=data['name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user,many=False)
        return Response(serializer.data)
    except:
        message = {'error':'taka osoba juz istnieje'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def kursy(request):
    if request.method =="GET":
        with connection.cursor() as cursor:
            cursor.execute("""
                select id,nazwa_kursu from kursy_kurs;
            """)
            rows = cursor.fetchall()
        kursy = [{"id": r[0],"nazwa_kursu":r[1]} for r in rows]
        return Response(kursy)
    if request.method == "POST":
        data = request.data
        nazwa_kursu = data.get("nazwa_kursu")

        if not nazwa_kursu:
            return Response({"error":"Brakuje danych"},status=400)
        
        with connection.cursor() as cursor:
            cursor.execute(""" 
                insert into kursy_kurs (nazwa_kursu) values (%s) RETURNING id;
        """,[nazwa_kursu])
            id = cursor.fetchone()[0]
        return Response({"id":id,"nazwa_kursu":nazwa_kursu})
    
@api_view(['GET'])    
def get_kurs(request,id):
    with connection.cursor() as cursor:
        cursor.execute(""" 
            SELECT * from kursy_kurs where id=%s
        """,[id])
        row = cursor.fetchone()
    if not row:
        return Response({"error":"Nie znaleziono kursu"},status = 404)
    kurs = {"id":row[0],"nazwa_kursu":row[1]}
    return Response(kurs)

@api_view(['GET'])
def get_artykuly(request,nazwa_kursu):
    with connection.cursor() as cursor:
        cursor.execute("""  
            SELECT * from artykul_kurs_view
                       WHERE nazwa_kursu=%s;
        """,[nazwa_kursu])
        rows = cursor.fetchall()
    artykuly = [{"id": row[0],"tresc": row[1],"nazwa_kursu":row[2],"id_kursu":row[3]} for row in rows]
    return Response(artykuly)

@api_view(['GET'])
def get_artykul(request,id):
    with connection.cursor() as cursor:
        cursor.execute("""
                       SELECT * from artykul_kurs_view 
                       WHERE artykul_id = %s
                       """,[id])
        row = cursor.fetchone()
    artykul = {"id": row[0],"tresc": row[1],"nazwa_kursu":row[2],"id_kursu":row[3]} 
    return Response(artykul)

@api_view(['GET'])
def start_quiz(request):
    kursy_param = request.GET.get("kursy")
    count = int(request.GET.get("liczba_pytan", 20))

    if not kursy_param:
        return Response({"error": "Brak podanego kursu"}, status=400)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.tresc
            FROM kursy_pytanie p
            JOIN artykul_kurs_view ak
            ON ak.artykul_id = p.artykul_id
            WHERE ak.nazwa_kursu = %s
        """, [kursy_param])
        rows = cursor.fetchall()

    if count < len(rows):
        rows = random.sample(rows, count)

    quiz = []
    for row in rows:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT o.tresc, o.poprawna
                FROM kursy_odpowiedz o
                WHERE pytanie_id = %s
            """, [row[0]])
            odpowiedzi = cursor.fetchall()
        quiz.append({
            "id": row[0],
            "tresc": row[1],
            "odpowiedzi": [{"text": o[0], "correct": o[1]} for o in odpowiedzi]
        })

    return Response(quiz)

@api_view(['POST'])
def sprawdz_quiz(request):
    odpowiedzi = request.data.get("odpowiedzi")
    if not odpowiedzi:
        return Response({"error":"zly format odpowiedzi"})
    wynik = 0
    with connection.cursor() as cursor:
        cursor.execute("""
                        SELECT tresc,pytanie_id from kursy_odpowiedz
                       where poprawna = true;
                       """)
        poprawne_odpowiedzi = cursor.fetchall()

    poprawne_id = []
    for odp in odpowiedzi:
        pyt_id = odp["pytanie_id"]
        wybrana = odp["wybrana_opcja"]
        if (wybrana,pyt_id) in poprawne_odpowiedzi:
            wynik+=1
            poprawne_id.append(pyt_id)
        
    return Response({"punkty": wynik,"poprawne":poprawne_id})
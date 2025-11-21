from django.shortcuts import render
from django.db import connection
from collections import defaultdict
import random



def home(request):
    return render(request, "base.html")

def quiz_start(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM kursy_pytanie;")
        pytania_ids = [row[0] for row in cursor.fetchall()]

    losowe_ids = random.sample(pytania_ids, min(20, len(pytania_ids)))

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT pytanie_id, pytanie_tresc, odpowiedz_id, odpowiedz_tresc, poprawna
            FROM quiz_view
            WHERE pytanie_id = ANY(%s);
        """, [losowe_ids])
        rows = cursor.fetchall()

    pytania_dict = defaultdict(lambda: {"tresc": "", "odpowiedzi": []})
    for pytanie_id, pyt_tresc, odp_id, odp_tresc, poprawna in rows:
        pytania_dict[pytanie_id]["tresc"] = pyt_tresc
        pytania_dict[pytanie_id]["odpowiedzi"].append({
            "id": odp_id,
            "tresc": odp_tresc,
            "poprawna": poprawna
        })

    pytania = [{"id": pid, **data} for pid, data in pytania_dict.items()]

    return render(request, "quiz_start.html", {"pytania": pytania})


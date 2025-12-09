import os
import time
import json
from openai import OpenAI
from django.core.management.base import BaseCommand
from django.db import connection

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
MAX_RETRIES = 5
INITIAL_BACKOFF = 1.0
MAX_ARTICLE_TEXT_CHARS = 3000


def call_openai_for_question(title, content):
    prompt = f"""
Jesteś asystentem, który na podstawie treści artykułu tworzy jedno wielokrotnego wyboru pytanie (multiple-choice).

WEJŚCIE:
Tytuł artykułu: {title}
Treść artykułu: {content}

WYMAGANIA:
- wygeneruj dokładnie JEDNO pytanie,
- wygeneruj dokładnie 4 odpowiedzi,
- DOKŁADNIE JEDNA z odpowiedzi ma mieć "correct": true,
- trzy pozostałe MUSZĄ mieć "correct": false,
- odpowiedzi muszą być różne, jednoznaczne,
- odpowiedzi muszą być sensowne w kontekście artykułu,
- format odpowiedzi: czysty JSON bez komentarzy:
{{
  "question": "Pytanie?",
  "options": [
    {{"text": "A", "correct": false}},
    {{"text": "B", "correct": true}},
    {{"text": "C", "correct": false}},
    {{"text": "D", "correct": false}}
  ]
}}
ZASADY:
- odpowiedzi po polsku,
- nie dodawaj żadnych wyjaśnień,
- zwróć TYLKO i WYŁĄCZNIE JSON.
    """

    attempt = 0
    backoff = INITIAL_BACKOFF

    while True:
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=600
            )

            text = resp.choices[0].message.content.strip()
            parsed = json.loads(text)

            if (
                "question" in parsed
                and "options" in parsed
                and isinstance(parsed["options"], list)
                and len(parsed["options"]) == 4
            ):
                return parsed

            raise ValueError("Niepoprawny format JSON")

        except json.JSONDecodeError:
            attempt += 1
            if attempt > MAX_RETRIES:
                raise
            try:
                start = text.find("{")
                end = text.rfind("}")
                parsed = json.loads(text[start:end+1])
                return parsed
            except Exception:
                time.sleep(backoff)
                backoff = min(backoff * 2, 60)

        except Exception:
            attempt += 1
            if attempt > MAX_RETRIES:
                raise
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)


class Command(BaseCommand):
    help = "Generuje pytania + odpowiedzi dla artykułów oraz zapisuje do bazy SQL."

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, tytul, tresc FROM kursy_artykul ORDER BY id;")
            articles = cursor.fetchall()

        total = len(articles)
        print(f"Znaleziono {total} artykułów.")

        count = 0

        for art_id, tytul, tresc in articles:
            count += 1
            print(f"[{count}/{total}] ArtID={art_id} Tytul={tytul!r}")

            if tresc and len(tresc) > MAX_ARTICLE_TEXT_CHARS:
                tresc_short = tresc[:MAX_ARTICLE_TEXT_CHARS]
            else:
                tresc_short = tresc or ""

            try:
                result = call_openai_for_question(tytul or "", tresc_short)
            except Exception as e:
                print(f"ERROR: {e}")
                continue

            q_text = result["question"].strip()
            options = result["options"]

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO kursy_pytanie (artykul_id, tresc) VALUES (%s, %s) RETURNING id;",
                    [art_id, q_text]
                )
                pytanie_id = cursor.fetchone()[0]

                for opt in options:
                    cursor.execute(
                        "INSERT INTO kursy_odpowiedz (pytanie_id, tresc, poprawna) VALUES (%s, %s, %s);",
                        [pytanie_id, opt["text"].strip(), bool(opt["correct"])]
                    )
                connection.commit()

            print(f"-> Dodano pytanie id={pytanie_id}")

        print("Zakończono generowanie pytań.")

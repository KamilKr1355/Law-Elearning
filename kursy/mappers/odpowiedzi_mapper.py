def map_odpowiedz_row(row):
    return {
        "id": row[0],
        "tresc": row[1],
        "poprawna": row[2],
        "pytanie_id": row[3]

    }

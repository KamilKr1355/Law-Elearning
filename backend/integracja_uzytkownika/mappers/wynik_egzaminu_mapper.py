def map_wyniki_row(row):
    return {
        "id": row[0],
        "data_zapisu": row[1],
        "wynik": float(row[2]),
        "kurs_id": row[3],
        "uzytkownik_id": row[4]
    }

def map_average_uzytkownik_kurs_row(row):
    return {
        "srednia": float(row[0]) if row[0] else 0.0,
        "kurs_id": row[1],
        "uzytkownik_id": row[2],
        "username": row[3]
    }

def map_average_kurs_row(row):
    return {
        "srednia_wynik": float(row[0]) if row[0] else 0.0,
        "kurs_id": row[1]
    }
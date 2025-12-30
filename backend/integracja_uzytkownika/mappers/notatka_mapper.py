def map_notatka_row(row):
    return {
        "id": row[0],
        "tresc": row[1].strip() if row[1] else "",
        "data_zapisu": row[2],
        "artykul_id": row[3],
        "uzytkownik_id": row[4],
    }

def map_notatka_row2(row):
    return {
        "id": row[0],
        "tresc": row[1].strip() if row[1] else "",
        "data_zapisu": row[2],
        "artykul_id": row[3],
        "uzytkownik_id": row[4],
        "kurs_id" : row[5],
        "nazwa_kursu" : row[6], 
        "nr_artykulu" : row[7]
    }
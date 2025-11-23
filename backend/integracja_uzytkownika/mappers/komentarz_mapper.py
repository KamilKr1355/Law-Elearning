def map_komentarz_row(row):
    return {
        "id": row[0],
        "tresc": row[1].strip() if row[1] else "",
        "uzytkownik_id": row[2],
        "artykul_id": row[3],
        "data_zapisu": row[4],
        "username": row[5] 
    }

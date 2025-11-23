def map_notatka_row(row):
    return {
        "id": row[0],
        "tresc": row[1].strip() if row[1] else "",
        "data_zapisu": row[2],
        "artykul_id": row[3],
        "uzytkownik_id": row[4],
    }
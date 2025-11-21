def map_artykul_row(row):
    return {
        "artykul_id": row[0], 
        "tresc": row[1], 
        "nazwa_kursu": row[2], 
        "id": row[3]
        }

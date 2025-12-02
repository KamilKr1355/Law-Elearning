def map_artykul_row(row):
    return {
        "artykul_id": row[0], 
        "tresc": row[1], 
        "nazwa_kursu": row[2], 
        "id": row[3]
        }

def map_artykul_row2(row):
    return {
        "artykul_id": row[0], 
        "tytul": row[1].strip(), 
        "tresc": row[2], 
        "nazwa_kursu": row[3], 
        "kurs_id": row[4],
        "rozdzial_id": row[5]
        }

def map_artykul_row3(row):
    return {
        "artykul_id": row[0], 
        "tytul": row[1].strip(), 
        "tresc": row[2], 
        "nazwa_kursu": row[3], 
        "kurs_id": row[4],
        }

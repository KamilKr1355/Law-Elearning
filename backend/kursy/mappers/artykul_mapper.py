def map_artykul_row(row):
    return {
        "artykul_id": row[0], 
        "tresc": row[1], 
        "nazwa_kursu": row[2], 
        "id": row[3],
        "nr_artykulu":row[4]
        }

def map_artykul_row2(row):
    return {
        "artykul_id": row[0], 
        "tytul": row[1].strip(), 
        "tresc": row[2], 
        "nazwa_kursu": row[3], 
        "kurs_id": row[4],
        "rozdzial_id": row[5],
        "nr_artykulu":row[6]
        }

def map_artykul_row3(row):
    return {
        "artykul_id": row[0], 
        "rozdzial_id": row[1],
        "tytul": row[2].strip(), 
        "tresc": row[3], 
        "nazwa_kursu": row[4], 
        "kurs_id": row[5],
        "nr_artykulu":row[6]
        }

def map_artykul_row4(row):
    return {
        "artykul_id": row[0], 
        "tytul": row[1].strip(), 
        "tresc": row[2], 
        "nazwa_kursu": row[3], 
        "kurs_id": row[4],
        "nr_artykulu":row[5]
        }


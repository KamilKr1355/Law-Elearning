def map_zapis_row(row):
    return {
        "id": row[0],
        "data_zapisu": row[1],
        "tresc": row[2].strip() if row[2] else "",
        "tytul": row[3].strip() if row[3] else "",
    }
def map_statystyki_pytania_row(wiersz):
    if not wiersz:
        return None 
        
    return {
        "id": wiersz[0],
        "pytanie_id": wiersz[1],
        "ilosc_odpowiedzi": wiersz[2],
        "poprawne_odpowiedzi": wiersz[3],
    }
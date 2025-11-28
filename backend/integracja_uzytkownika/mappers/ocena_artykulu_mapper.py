def map_ocena_artykulu_row(wiersz):
    if not wiersz:
        return None
    
    return {
        "id": wiersz[0],
        "ocena": wiersz[1],
        "data_zapisu": wiersz[2], 
        "artykul_id": wiersz[3],
        "uzytkownik_id": wiersz[4],
    }

def map_srednia_ocena_row(wiersz):
    if not wiersz or wiersz[0] is None:
        return {"srednia_ocena": 0.0, "artykul_id": None}
        
    return {
        "srednia_ocena": float(wiersz[0]), 
        "artykul_id": wiersz[1],
    }
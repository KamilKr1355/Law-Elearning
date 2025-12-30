def map_progress_pytan_row(wiersz):
    if not wiersz:
        return None
    
    return {
        "id": wiersz[0],
        "uzytkownik_id": wiersz[1],
        "pytanie_id": wiersz[2],
        "status": wiersz[3],
        "data_aktualizacji": wiersz[4],
    }
    
def map_progress_summary_row(wiersz):
    if not wiersz: 
        return {"total_questions": 0, "completed_count": 0}
        
    return {
        "total_questions": wiersz[0] or 0,
        "completed_count": wiersz[1] or 0,
    }
    
def map_postep_pytania_tryb_nauki_row(wiersz):
    if not wiersz:
        return None
        
    return {
        "pytanie_id": wiersz[0],
        "artykul_id": wiersz[1],
        "tresc": wiersz[2],
        "status_uzytkownika": wiersz[3] 
    }
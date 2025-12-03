from decimal import Decimal

def map_leaderboard_row(row):
    srednia_raw = row[0] 
    if srednia_raw is None:
        srednia_wartosc = Decimal('0.00')
    elif isinstance(srednia_raw, (float, Decimal)):
        srednia_wartosc = srednia_raw
    else:
        srednia_wartosc = Decimal(str(srednia_raw)) 
        
    return {
        "srednia": srednia_wartosc,
        "username": row[1]
    }
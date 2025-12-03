from ..repositories.leaderboard_repository import LeaderboardRepository
from ..mappers.leaderboard_mapper import map_leaderboard_row

class LeaderboardService:
    def pobierz_wszystkie_statystyki(self):
        rows = LeaderboardRepository.get_all()
        return [map_leaderboard_row(r) for r in rows]

 
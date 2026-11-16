from game.player import Player
from game.game_state import GameState

class MatchResult:
    def __init__(self, game_state: GameState, points=[5, 3, 1, 0]):
        self.ranking = game_state.final_ranking
        self.points = dict(zip(self.ranking, points))
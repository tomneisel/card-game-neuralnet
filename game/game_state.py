from game.card import Card
from game.player import Player

class GameState:
    def __init__(self):
        self.players: dict[Player] = []
        self.player_ids = []
        self.current_player = 0
        self.current_trick: list[Card] = []
        self.last_player = None
        self.passed_players = []
        self.finished_players = []
        self.game_over = False
        self.final_ranking = []
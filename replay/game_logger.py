from game.game_state import GameState
from game.action import Action

class GameLogger:
    def __init__(self):
        self.game_data = {
            "initial_state": {},
            "actions": [],
            "final_ranking": []
        }
        self.turn = 1

    def save_initial_state(self, game_state: GameState):
        self.game_data["initial_state"] = {
            "num_players": len(game_state.players),
            "player_hands": {
                    player_id: player.hand.copy()
                    for player_id, player in game_state.players.items()
            },
            "first_player": game_state.current_player
        }


    def log_action(self, player_id, gamestate: GameState, action: Action):
        self.game_data["actions"].append({
            "turn": self.turn,
            "player_id": player_id,
            "action": {
                "is_pass": action.is_pass,
                "cards": action.cards
            },
            "num_cards_left": len(gamestate.players.get(player_id).hand)
        })
        self.turn = self.turn + 1

    def save_final_ranking(self, ranking):
        self.game_data["final_ranking"] = ranking
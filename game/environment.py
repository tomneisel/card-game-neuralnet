from game.rules import Rules
from game.game_state import GameState
from game.game_engine import GameEngine

class Environment:
    def __init__(self, deck_size=32, num_players=4):
        self.deck_size = deck_size
        self.num_players = num_players

        self.rules = Rules()
        self.game_state = GameState()
        self.engine = GameEngine(self.rules, self.game_state)

    def reset(self):
        self.engine.start_game(
            deck_size=self.deck_size,
            num_players=self.num_players
        )

        return self.get_observation()

    def get_observation(self):
        player_id = self.game_state.current_player
        player = self.game_state.players[player_id]

        return {
            "current_player": player_id,
            "hand": player.hand.copy(),
            "current_trick": self.game_state.current_trick.copy(),
            "last_player": self.game_state.last_player,
            "passed_players": self.game_state.passed_players.copy(),
            "finished_players": self.game_state.finished_players.copy(),
            "legal_actions": self.get_legal_actions()
        }

    def get_legal_actions(self):
        player_id = self.game_state.current_player
        player = self.game_state.players[player_id]

        return self.rules.get_legal_actions(self.game_state,player)

    def step(self, action):
        player_id = self.game_state.current_player

        self.engine.apply_action(player_id, action)

        observation = self.get_observation()
        reward = 0
        done = self.game_state.game_over
        info = {}

        return observation, reward, done, info
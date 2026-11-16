from replay.game_logger import GameLogger

class GameReplay():
    def __init__(self, game_logger: GameLogger):
        self.game_logger = game_logger

    def replay(self):
        initial_state = self.game_logger.game_data["initial_state"]
        actions = self.game_logger.game_data["actions"]
        final_ranking = self.game_logger.game_data["final_ranking"]

        #Game start
        print(f"Number of players: {initial_state["num_players"]}")

        print("Player hands:")
        for player_id, hand in initial_state["player_hands"].items():
            print(f"Player {player_id}:")
            print(hand)

        print(f"First player: {initial_state["first_player"]}")

        #Game action
        for action in actions:
            if action["action"]["is_pass"]:
                print(f"Player {action["player_id"]} passes")
            else:
                print(f"Move by player {action["player_id"]}: {action["action"]["cards"]}. ({action["num_cards_left"]} cards left)")

            if action["num_cards_left"] == 0:
                print(f"Player {action["player_id"]} finished")

        #Game ranking
        print("Final ranking:")
        for place, rank in zip(range(1, len(final_ranking) + 1), final_ranking):
            print(f"Place {place}: Player {rank}")
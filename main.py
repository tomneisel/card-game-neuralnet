from game.environment import Environment

from tournament.match_result import MatchResult
from tournament.leaderbord import Leaderbord

from replay.game_logger import GameLogger
from replay.game_replay import GameReplay

from agents.random_agent import RandomAgent
from agents.simple_agent import SimpleAgent

import pandas as pd
import matplotlib.pyplot as plt

def play_game():
    agents = {
        1: SimpleAgent(1),
        2: SimpleAgent(2),
        3: SimpleAgent(3),
        4: SimpleAgent(4)
    }

    env = Environment(deck_size=32, players=agents)

    for _ in range(1):

        observation = env.reset()
        game_logger.save_initial_state(env.game_state)

        while True:
            current_player = observation["current_player"]

            agent = agents.get(current_player)

            action = agent.choose_action(observation)

            log_player = current_player

            observation, reward, done, info = env.step(action)

            game_logger.log_action(log_player, env.game_state, action)

            if done:
                break

        match_result = MatchResult(env.game_state)
        print(match_result.points)
        
        leaderbord.add_result(match_result)
        game_logger.save_final_ranking(env.game_state.final_ranking)

        print(f"ids: {env.game_state.player_ids}")

if __name__ == "__main__":
    leaderbord = Leaderbord()
    game_logger = GameLogger()

    play_game()

    leaderbord.get_leaderbord()

    game_replay = GameReplay(game_logger)
    game_replay.replay()

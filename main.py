from game.environment import Environment
from agents.random_agent import RandomAgent
from agents.simple_agent import SimpleAgent

import pandas as pd
import matplotlib.pyplot as plt

def play_game():
    env = Environment(deck_size=32, num_players=4)

    agents = [
        SimpleAgent(),
        SimpleAgent(),
        SimpleAgent(),
        SimpleAgent()
    ]

    for _ in range(1000):

        observation = env.reset()

        while True:
            current_player = observation["current_player"]

            agent = agents[current_player]

            action = agent.choose_action(observation)

            observation, reward, done, info = env.step(action)

            if done:
                break

        print("Game finished!")
        print("Final ranking:", env.game_state.final_ranking)
        winners.append(env.game_state.final_ranking[0])

if __name__ == "__main__":
    winners = []
    play_game()

    print(pd.Series(winners).value_counts())

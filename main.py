from game.environment import Environment

from tournament.match_result import MatchResult
from tournament.leaderbord import Leaderbord
from tournament.knockout_tournament import KnockoutTournament

from replay.game_logger import GameLogger
from replay.game_replay import GameReplay

from agents.random_agent import RandomAgent
from agents.simple_agent import SimpleAgent

import pandas as pd
import matplotlib.pyplot as plt

def play_tournament():
    agents = [
    RandomAgent(5),
    RandomAgent(6),
    RandomAgent(7),
    RandomAgent(8),
    RandomAgent(9),
    RandomAgent(10),
    RandomAgent(11),
    RandomAgent(12),
    RandomAgent(13),
    RandomAgent(14),
    RandomAgent(15),
    RandomAgent(16),
    SimpleAgent(17),
    SimpleAgent(18),
    SimpleAgent(19),
    SimpleAgent(20)
    ]

    tournament = KnockoutTournament(agents=agents, rounds=2, num_tournaments=100)

    tournament.run()
    final_ranking = tournament.get_ranking()

    print(final_ranking)

if __name__ == "__main__":
    play_tournament()

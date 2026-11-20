from game.environment import Environment

from tournament.match_result import MatchResult
from tournament.leaderbord import Leaderbord
from tournament.knockout_tournament import KnockoutTournament

from replay.game_logger import GameLogger
from replay.game_replay import GameReplay

from agents.random_agent import RandomAgent
from agents.simple_agent import SimpleAgent
from agents.neural_agent import NeuralAgent

from evolution.genome import Genome, NodeGene, ConnectionGene

import pandas as pd
import matplotlib.pyplot as plt

def play_single_game():

    input_size = 30
    
    nodes = {
        n: NodeGene(id=n, node_type="input", bias=0) for n in range(input_size)
    }
    nodes[input_size] = NodeGene(id=input_size, node_type="output", bias=0)

    connections = [
        ConnectionGene(21, 30, 0.1, True),
        ConnectionGene(22, 30, 0.2, True),
        ConnectionGene(23, 30, 0.3, True),
        ConnectionGene(24, 30, 0.4, True),
        ConnectionGene(25, 30, 0.5, True),
        ConnectionGene(26, 30, 0.6, True),
        ConnectionGene(27, 30, 0.7, True),
        ConnectionGene(28, 30, 0.8, True),
    ]

    genome = Genome(nodes=nodes, connections=connections)

    agents = [
        NeuralAgent(5, genome=genome),
        NeuralAgent(6, genome=genome),
        NeuralAgent(7, genome=genome),
        NeuralAgent(8, genome=genome)
    ]

    env = Environment(deck_size=32, players=agents)
    observation = env.reset()

    agents_by_id = {
        agent.id: agent
        for agent in agents
    }

    while True:
        current_player = observation["current_player"]
        agent = agents_by_id.get(current_player)

        encoded_gamestate = agent.encode_gamestate(env.game_state)

        action = agent.choose_action(observation, env.game_state)
        observation, reward, done, info = env.step(action)

        if done:
            break

def play_tournament():

    input_size = 30
        
    nodes = {
        n: NodeGene(id=n, node_type="input", bias=0) for n in range(input_size)
    }
    nodes[input_size] = NodeGene(id=input_size, node_type="output", bias=0)

    connections = [
        ConnectionGene(21, 30, 0.8, True),
        ConnectionGene(22, 30, 0.7, True),
        ConnectionGene(23, 30, 0.6, True),
        ConnectionGene(24, 30, 0.5, True),
        ConnectionGene(25, 30, 0.4, True),
        ConnectionGene(26, 30, 0.3, True),
        ConnectionGene(27, 30, 0.2, True),
        ConnectionGene(28, 30, 0.1, True),
    ]

    genome = Genome(nodes=nodes, connections=connections)

    agents = [
        NeuralAgent(5, genome=genome),
        NeuralAgent(6, genome=genome),
        NeuralAgent(7, genome=genome),
        NeuralAgent(8, genome=genome),
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

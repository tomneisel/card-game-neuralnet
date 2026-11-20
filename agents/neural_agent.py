from game.card import Card, Rank, Suit
from game.game_state import GameState
from game.action import Action
from game.environment import Environment

from evolution.genome import Genome

from neural_network.network import NeuralNetwork

import random

class NeuralAgent:
    def __init__(self, id, genome: Genome = None):
        self.id = id
        self.neural_net = NeuralNetwork(genome)

    def choose_action(self, observation: Environment, game_state: GameState):
            
        legal_actions: list[Action] = observation["legal_actions"]

        if not legal_actions:
            raise ValueError("No legal actions available!")

        best_action = None
        highest_action_rating = 0

        for action in legal_actions:
            if action.is_pass:
                network_input = self.encode_gamestate(game_state=game_state) + [0, 0, 0, 0, 0, 0, 0, 0, 1]
            else:
                network_input = self.encode_gamestate(game_state=game_state) + self.count_cards(action.cards) + [0]

            p = self.neural_net.forward(network_input)

            if p > highest_action_rating:
                best_action = action
                highest_action_rating = p

        return best_action

    def encode_gamestate(self, game_state: GameState):

        hand_cards = self.count_cards(game_state.players.get(game_state.current_player).hand)
        trick_cards = self.count_cards(game_state.current_trick)
        num_trick_cards = [len(game_state.current_trick)]
        num_other_players_cards = [len(game_state.players.get(game_state.player_ids[(game_state.current_player + i) % len(game_state.players)]).hand) for i in range(1, len(game_state.players))]
        last_player = [((game_state.last_player - game_state.current_player) % len(game_state.players)) if game_state.last_player else 0]

        return hand_cards + trick_cards + num_trick_cards + num_other_players_cards + last_player


    def count_cards(self, cards: list[Card]):
        rank_counts = {
            rank: 0
            for rank in Rank
            if rank.value >= 7
        }

        for card in cards:
            if card.rank.value >= 7:
                rank_counts[card.rank] += 1

        return list(rank_counts.values())
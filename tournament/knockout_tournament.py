import random

from game.environment import Environment

from tournament.leaderbord import Leaderbord
from tournament.match_result import MatchResult

from agents.random_agent import RandomAgent
from agents.simple_agent import SimpleAgent

class KnockoutTournament:
    def __init__(self, agents, rounds=3, num_players_per_match=4, num_tournaments=20):
        self.agents = agents
        self.rounds = rounds
        self.num_players_per_match = num_players_per_match
        self.num_tournaments = num_tournaments
        self.leaderbord = Leaderbord()

    def run(self):
        if self.num_players_per_match**self.rounds != len(self.agents):
            raise ValueError("No valid combination of number of agents, players per match and tournament rounds")

        for _ in range(self.num_tournaments):

            random.shuffle(self.agents)
            groups = self.create_groups(self.agents)

            for r in range(1, self.rounds + 1):

                survivours = []

                for group in groups:
                    match_result = self.run_match(group, r)
                    winner = next((agent for agent in group if agent.id == match_result.ranking[0]))
                    survivours.append(winner)
                    self.leaderbord.add_result(match_result=match_result)

                groups = self.create_groups(survivours)

    def create_groups(self, agents_to_group):
        groups = []
        group = []

        for i in range(1, len(agents_to_group) + 1):
            group.append(agents_to_group[i-1])

            if i % self.num_players_per_match == 0:
                groups.append(group)
                group = []

        return groups

    def run_match(self, match_agents, point_multiplier):
        env = Environment(deck_size=32, players=match_agents)
        observation = env.reset()

        agents_by_id = {
            agent.id: agent
            for agent in match_agents
        }

        while True:
            current_player = observation["current_player"]
            agent = agents_by_id.get(current_player)
            action = agent.choose_action(observation)
            observation, reward, done, info = env.step(action)

            if done:
                break

        match_result = MatchResult(env.game_state, points=[x * point_multiplier for x in [1, 0, 0, 0]])
        return match_result

    def get_ranking(self):
        return self.leaderbord.get_leaderbord()
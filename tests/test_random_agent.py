
import unittest

from agents.random_agent import RandomAgent
from game.environment import Environment


class TestRandomAgent(unittest.TestCase):

    def setUp(self):
        self.env = Environment(deck_size=32, num_players=4)
        self.agent = RandomAgent()

    def test_agent_returns_legal_action(self):
        observation = self.env.reset()

        action = self.agent.choose_action(observation)

        self.assertIn(action, observation["legal_actions"])

    def test_agent_returns_action(self):
        observation = self.env.reset()

        action = self.agent.choose_action(observation)

        self.assertIsNotNone(action)

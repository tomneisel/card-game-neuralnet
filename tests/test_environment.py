import unittest

from game.environment import Environment
from game.action import Action


class TestEnvironment(unittest.TestCase):

    def setUp(self):
        self.env = Environment(
            deck_size=32,
            num_players=4
        )

    def test_reset_starts_new_game(self):
        observation = self.env.reset()

        self.assertIsNotNone(observation)
        self.assertEqual(len(self.env.game_state.players), 4)

        for player in self.env.game_state.players:
            self.assertEqual(len(player.hand), 8)
            self.assertFalse(player.finished)

    def test_observation_contains_current_player_information(self):
        observation = self.env.reset()

        self.assertIn("current_player", observation)
        self.assertIn("hand", observation)
        self.assertIn("current_trick", observation)
        self.assertIn("legal_actions", observation)

        current_player = observation["current_player"]

        self.assertEqual(
            current_player,
            self.env.game_state.current_player
        )

    def test_get_legal_actions(self):
        self.env.reset()

        legal_actions = self.env.get_legal_actions()

        self.assertIsInstance(legal_actions, list)
        self.assertGreater(len(legal_actions), 0)

    def test_step_executes_action(self):
        self.env.reset()

        legal_actions = self.env.get_legal_actions()
        action = legal_actions[0]

        observation, reward, done, info = self.env.step(action)

        self.assertIsNotNone(observation)
        self.assertIsInstance(reward, (int, float))
        self.assertIsInstance(done, bool)
        self.assertIsInstance(info, dict)

    def test_step_rejects_illegal_action(self):
        self.env.reset()

        with self.assertRaises(ValueError):
            self.env.step(Action(is_pass=True))
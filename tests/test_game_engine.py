
import unittest

from game.card import Card, Rank, Suit
from game.action import Action
from game.game_state import GameState
from game.game_engine import GameEngine
from game.rules import Rules


class TestGameEngine(unittest.TestCase):

    def setUp(self):
        self.rules = Rules()
        self.game_state = GameState()
        self.engine = GameEngine(self.rules, self.game_state)

        self.engine.start_game(deck_size=32, num_players=4)

    def test_game_starts_correctly(self):
        # Four players should be created
        self.assertEqual(len(self.game_state.players), 4)

        # Every player should have 8 cards
        for player in self.game_state.players:
            self.assertEqual(len(player.hand), 8)

        # All 32 cards should be dealt
        total_cards = sum(
            len(player.hand) for player in self.game_state.players
        )
        self.assertEqual(total_cards, 32)

        # Starting player must have the Seven of Diamonds
        starting_player = self.game_state.players[
            self.game_state.current_player
        ]

        starting_card = Card(Rank.SEVEN, Suit.DIAMONDS)

        self.assertIn(starting_card, starting_player.hand)

    def test_starting_player_can_play_seven_of_diamonds(self):
        player_id = self.game_state.current_player
        player = self.game_state.players[player_id]

        starting_card = Card(Rank.SEVEN, Suit.DIAMONDS)

        action = Action(cards=[starting_card])

        self.engine.apply_action(player_id, action)

        # Card should be removed from hand
        self.assertNotIn(starting_card, player.hand)

        # Current trick should contain the played card
        self.assertEqual(self.game_state.current_trick, [starting_card])

        # Last player should be the starting player
        self.assertEqual(self.game_state.last_player, player_id)

        # Next player should be player 0 if starting player is player 3
        self.assertEqual(self.game_state.current_player, (player_id + 1) % 4)

    def test_wrong_player_cannot_play(self):
        wrong_player = (self.game_state.current_player + 1) % 4

        card = self.game_state.players[wrong_player].hand[0]
        action = Action(cards=[card])

        with self.assertRaises(ValueError):
            self.engine.apply_action(wrong_player, action)

    def test_player_cannot_play_card_they_do_not_have(self):
        player_id = self.game_state.current_player

        # Pick a card from another player's hand
        other_player_id = (player_id + 1) % 4
        card = self.game_state.players[other_player_id].hand[0]

        action = Action(cards=[card])

        with self.assertRaises(ValueError):
            self.engine.apply_action(player_id, action)

    def test_player_can_pass(self):
        player_id = self.game_state.current_player

        starting_card = Card(Rank.SEVEN, Suit.DIAMONDS)
        self.engine.apply_action(
            player_id,
            Action(cards=[starting_card])
        )

        next_player = self.game_state.current_player

        self.engine.apply_action(
            next_player,
            Action(is_pass=True)
        )

        self.assertIn(next_player, self.game_state.passed_players)
        self.assertEqual(self.game_state.current_player, (next_player + 1) % 4)

    def test_player_can_reenter_after_passing(self):
        self.game_state.players[0].hand = [
            Card(Rank.SEVEN, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.DIAMONDS)
        ]
        self.game_state.players[1].hand = [
            Card(Rank.NINE, Suit.HEARTS),
            Card(Rank.KING, Suit.HEARTS)
        ]
        self.game_state.players[2].hand = [
            Card(Rank.NINE, Suit.CLUBS),
            Card(Rank.QUEEN, Suit.CLUBS)
        ]
        self.game_state.players[3].hand = [
            Card(Rank.TEN, Suit.HEARTS),
            Card(Rank.QUEEN, Suit.HEARTS)
        ]

        self.game_state.current_player = 0

        # Player 0 plays 7
        self.engine.apply_action(
            0, Action(cards=[self.game_state.players[0].hand[0]])
        )

        # Player 1 passes
        self.engine.apply_action(1, Action(is_pass=True))

        # Player 2 plays 9
        self.engine.apply_action(
            2, Action(cards=[self.game_state.players[2].hand[0]])
        )

        # Player 3 passes
        self.engine.apply_action(3, Action(is_pass=True))

        # Player 0 passes
        self.engine.apply_action(0, Action(is_pass=True))

        # Player 1 plays King
        king = self.game_state.players[1].hand[1]
        self.engine.apply_action(1, Action(cards=[king]))

        self.assertEqual(self.game_state.last_player, 1)
        self.assertEqual(self.game_state.current_trick, [king])
        self.assertEqual(self.game_state.passed_players, [])
        self.assertEqual(self.game_state.current_player, 2)

    def test_trick_ends_when_all_opponents_pass(self):
        self.game_state.players[0].hand = [
            Card(Rank.SEVEN, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.DIAMONDS)
        ]

        self.game_state.players[1].hand = [
            Card(Rank.EIGHT, Suit.HEARTS)
        ]

        self.game_state.players[2].hand = [
            Card(Rank.NINE, Suit.HEARTS)
        ]

        self.game_state.players[3].hand = [
            Card(Rank.TEN, Suit.HEARTS)
        ]

        self.game_state.current_player = 0

        seven = self.game_state.players[0].hand[0]
        self.engine.apply_action(0, Action(cards=[seven]))

        self.engine.apply_action(1, Action(is_pass=True))
        self.engine.apply_action(2, Action(is_pass=True))
        self.engine.apply_action(3, Action(is_pass=True))

        self.assertEqual(self.game_state.current_trick, [])
        self.assertIsNone(self.game_state.last_player)
        self.assertEqual(self.game_state.current_player, 0)

    def test_player_finishes_after_playing_last_card(self):
        self.game_state.players[0].hand = [
            Card(Rank.SEVEN, Suit.DIAMONDS)
        ]
        self.game_state.current_player = 0

        self.engine.apply_action(
            0,
            Action(cards=[Card(Rank.SEVEN, Suit.DIAMONDS)])
        )

        self.assertTrue(self.game_state.players[0].finished)
        self.assertIn(0, self.game_state.finished_players)

    def test_next_active_player_starts_if_winner_is_finished(self):
        self.game_state.players[0].hand = [
            Card(Rank.SEVEN, Suit.DIAMONDS)
        ]
        self.game_state.players[1].hand = [
            Card(Rank.EIGHT, Suit.HEARTS)
        ]
        self.game_state.players[2].hand = [
            Card(Rank.NINE, Suit.CLUBS)
        ]
        self.game_state.players[3].hand = [
            Card(Rank.TEN, Suit.SPADES)
        ]

        self.game_state.current_player = 0

        # Spieler 0 spielt seine letzte Karte
        self.engine.apply_action(
            0,
            Action(cards=[Card(Rank.SEVEN, Suit.DIAMONDS)])
        )

        # Spieler 1 passt
        self.engine.apply_action(1, Action(is_pass=True))

        # Spieler 2 passt
        self.engine.apply_action(2, Action(is_pass=True))

        # Spieler 3 passt – der Stich endet
        self.engine.apply_action(3, Action(is_pass=True))

        self.assertEqual(self.game_state.current_player, 1)
        self.assertEqual(self.game_state.current_trick, [])
        self.assertIsNone(self.game_state.last_player)

    def test_game_ends_when_only_one_player_remains(self):
        self.game_state.players[0].hand = [
            Card(Rank.SEVEN, Suit.DIAMONDS)
        ]
        self.game_state.players[1].hand = [
            Card(Rank.EIGHT, Suit.HEARTS)
        ]
        self.game_state.players[2].hand = [
            Card(Rank.NINE, Suit.CLUBS)
        ]
        self.game_state.players[3].hand = [
            Card(Rank.TEN, Suit.SPADES)
        ]

        self.game_state.current_player = 0

        # Spieler 0 beendet sich
        self.engine.apply_action(
            0, Action(cards=[Card(Rank.SEVEN, Suit.DIAMONDS)])
        )

        # Spieler 1 beendet sich
        self.engine.apply_action(
            1, Action(cards=[Card(Rank.EIGHT, Suit.HEARTS)])
        )

        # Spieler 2 beendet sich – Spieler 3 bleibt übrig
        self.engine.apply_action(
            2, Action(cards=[Card(Rank.NINE, Suit.CLUBS)])
        )

        self.assertTrue(self.game_state.game_over)
        self.assertEqual(
            self.game_state.final_ranking,
            [0, 1, 2, 3]
        )

if __name__ == "__main__":
    unittest.main()

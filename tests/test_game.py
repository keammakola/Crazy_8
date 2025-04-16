import unittest
from unittest.mock import patch
import game

class TestCrazy8Game(unittest.TestCase):

    def test_create_deck(self):
        deck, suits = game.create_deck()
        self.assertEqual(len(deck), 104)
        self.assertIn(("\u2665"), suits)
        self.assertIn(("Jack", "\u2665"), deck)

    def test_shuffler_changes_order(self):
        deck, _ = game.create_deck()
        original_deck = deck.copy()
        game.shuffler(deck)
        self.assertNotEqual(deck, original_deck)

    def test_player_creator(self):
        players = game.player_creator(3)
        self.assertEqual(len(players), 3)
        self.assertEqual(players[0], "player_1")

        cpu_game = game.player_creator(1)
        self.assertIn("cpu", cpu_game)
        self.assertEqual(len(cpu_game), 2)

    def test_deal_cards(self):
        deck, _ = game.create_deck()
        hand = []
        deck, hand = game.deal_cards(hand, 5, deck)
        self.assertEqual(len(hand), 5)
        self.assertEqual(len(deck), 99)

    def test_pile_creator(self):
        deck, _ = game.create_deck()
        pile, deck = game.pile_creator(deck)
        self.assertEqual(len(pile), 2)
        self.assertEqual(len(deck), 103)

    def test_turn_selector(self):
        players = ["player_1", "player_2", "player_3"]
        current, new_players, next_turn = game.turn_selector(players)
        self.assertEqual(current, "player_1")
        self.assertEqual(next_turn, "player_2")
        self.assertEqual(new_players, ["player_2", "player_3", "player_1"])

    def test_take_two(self):
        deck, _ = game.create_deck()
        hand = []
        deck, hand = game.take_two(hand, deck)
        self.assertEqual(len(hand), 2)

    def test_skip(self):
        players = ["player_1", "player_2", "player_3"]
        new_order = game.skip(players)
        self.assertEqual(new_order, ["player_2", "player_3", "player_1"])

    @patch("builtins.input", return_value="2")
    def test_game_initialisation(self, mocked_input):
        deck, players, player_hands, pile, suits = game.game_initialisation()
        self.assertEqual(len(players), 2)
        for hand in player_hands.values():
            self.assertEqual(len(hand), 8)
        self.assertTrue(len(pile) > 0)

if __name__ == '__main__':
    unittest.main()

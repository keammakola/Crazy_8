import unittest
from unittest.mock import patch
from game import Deck, CrazyEightGame, Card

class TestCrazyEightGame(unittest.TestCase):

    def test_create_deck(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 104)
        self.assertIn("\u2665", deck.suits)
        self.assertTrue(any(card.rank == "Jack" and card.suit == "\u2665" for card in deck.cards))

    def test_shuffler_changes_order(self):
        deck = Deck()
        original_order = deck.cards.copy()
        deck.shuffle()
        self.assertNotEqual(deck.cards, original_order)

    def test_player_creator(self):
        game = CrazyEightGame()
        players = game.player_creator(3)
        self.assertEqual(len(players), 3)
        self.assertEqual(players[0], "player_1")

        cpu_game = game.player_creator(1)
        self.assertIn("cpu", cpu_game)
        self.assertEqual(len(cpu_game), 2)

    def test_deal_cards(self):
        deck = Deck()
        hand = []
        dealt_hand = deck.deal(5)
        hand.extend(dealt_hand)
        self.assertEqual(len(hand), 5)
        self.assertEqual(len(deck.cards), 99)

    def test_pile_creator(self):
        game = CrazyEightGame()
        game.pile_creator()
        self.assertEqual(len(game.pile), 1)
        self.assertEqual(len(game.deck.cards), 103)

    def test_turn_selector(self):
        game = CrazyEightGame()
        game.players = ["player_1", "player_2", "player_3"]
        current, next_turn = game.turn_selector()
        self.assertEqual(current, "player_1")
        self.assertEqual(next_turn, "player_2")
        self.assertEqual(game.players, ["player_2", "player_3", "player_1"])

    def test_take_two(self):
        game = CrazyEightGame()
        hand = []
        initial_deck_count = len(game.deck.cards)
        game.take_two(hand)
        self.assertEqual(len(hand), 2)
        self.assertEqual(len(game.deck.cards), initial_deck_count - 2)

    def test_skip(self):
        game = CrazyEightGame()
        game.players = ["player_1", "player_2", "player_3"]
        game.skip()
        self.assertEqual(game.players, ["player_2", "player_3", "player_1"])

    @patch("builtins.input", return_value="2")
    def test_game_initialisation(self, mocked_input):
        game = CrazyEightGame()
        game.game_initialisation()
        self.assertEqual(len(game.players), 2)
        for hand in game.player_hands.values():
            self.assertEqual(len(hand), 8)
        self.assertTrue(len(game.pile) > 0)

if __name__ == '__main__':
    unittest.main()

import pytest
from project import Card, Deck, CrazyEightGame

def test_deck_creation():
    deck = Deck()
    assert len(deck.cards) == 104
    assert isinstance(deck.cards[0], Card)

def test_shuffle_deck():
    deck = Deck()
    original_cards = deck.cards.copy()
    deck.shuffle()
    assert deck.cards != original_cards

def test_deal_cards():
    deck = Deck()
    hand = deck.deal(5)
    assert len(hand) == 5
    assert len(deck.cards) == 99 

def test_take_two():
    deck = Deck()
    hand = deck.deal(5)
    initial_len = len(hand)
    game = CrazyEightGame()
    game.take_two(hand)
    assert len(hand) == initial_len + 2 

def test_turn_selector():
    game = CrazyEightGame()
    game.players = ["player_1", "player_2"]
    current_turn, next_turn = game.turn_selector()
    assert current_turn == "player_1"
    assert next_turn == "player_2"
    assert game.players == ["player_2", "player_1"]

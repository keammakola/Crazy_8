import pytest
from project import Card, Deck, CrazyEightGame, is_valid_card, get_playable_cards, reverse_players

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
    game.deck = deck
    game.take_two(hand)
    assert len(hand) == initial_len + 2


def test_turn_selector():
    game = CrazyEightGame()
    game.players = ["player_1", "player_2"]
    current_turn, next_turn = game.turn_selector()
    assert current_turn == "player_1"
    assert next_turn == "player_2"
    assert game.players == ["player_2", "player_1"] 


def test_reverse_players():
    players = ["p1", "p2", "p3"]
    reversed_list = reverse_players(players)
    assert reversed_list == ["p3", "p1", "p2"]  
    
def test_is_valid_card():
    top_card = Card(8, "♠")
    card1 = Card(5, "♠")
    card2 = Card(8, "♥")
    card3 = Card(3, "♦")
    assert is_valid_card(card1, top_card, "null") 
    assert is_valid_card(card2, top_card, "null") 
    assert not is_valid_card(card3, top_card, "null")
    
def test_get_playable_cards():
    pile_card = Card("Queen", "♣")
    hand = [Card("Queen", "♠"), Card("7", "♣"), Card("2", "♦")]
    playable = get_playable_cards(hand, pile_card, "null")
    assert playable == [Card("Queen", "♠"), Card("7", "♣")]

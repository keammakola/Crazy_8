import os
import random
import time

def create_deck():
    deck = []
    suits = ("♥","♦","♠","♣")
    faces = ("jack","queen","king","ace")
    number_of_decks = 2

    for i in range(number_of_decks):
        for suit in suits:
            for i in range(2,11):
                deck.append((i,suit))
            for face in faces:
                deck.append((face,suit))
    return deck
def deck_shuffle(deck):
    random.shuffle(deck)
    return deck
def player_creator(number:int):
    players = []
    for i in range(number):
        players.append(f"player_{i+1}")
    if number == 1:
        players.append("cpu")
    return players
def deal_hands(players,deck):
    player_hands = {}
    for player in players:
        hand = []
        for i in range(8):
            hand.append(deck[0])
            deck.pop(0)
        player_hands[player] = hand
    return player_hands ,deck
def pile(deck):
    pile = []
    pile += deck[0]
    return pile
def turn_selector(players):
    current_turn = players[0]
    players.append(players[0])
    players.pop(0)
    return current_turn, players

if __name__ == "__main__":
    deck = create_deck()
    shuffled_deck = deck_shuffle(deck)
    players = player_creator(int(input("How many players will be playing today?\nCrazy 8 allows 2-8 players.If you want to play with CPU, enter 1: ")))
    hands, deck = deal_hands(players,deck)
    pile = pile(deck)
    print(pile)
    while True:

        os.system('cls' if os.name == 'nt' else 'clear')
        current_turn , players = turn_selector(players)
        player_hand = hands[current_turn]
        print(f"It is {current_turn}'s turn.\n\nHere are your cards:\n{player_hand} \n\nCurrent card on the pile: {pile}\n")
        pile_card_number = pile[0]
        pile_suit = pile[1]
        playable_cards = []
        for card in player_hand:
            if card[0] == pile_card_number or card[1] == pile_suit:
                if card not in playable_cards:
                    playable_cards.append(card)
        print(f"Select one of the following playable options to play. Pick from 1 to {len(playable_cards)+1}.")

        for i in playable_cards:
            print(f"{playable_cards.index(i)+1}. {i}")
        deck_command = f"{len(playable_cards) + 1}. Pick card from deck."
        print(deck_command)
        deck_command = int(deck_command.split(".")[0])
        played_card = int(input(""))

        if played_card != deck_command:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"You have played {playable_cards[played_card-1]}")
            time.sleep(2.5)
            pile = playable_cards[played_card-1]
            player_hand.remove(pile)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"You picked up {deck[0]}")
            time.sleep(2.5)
            player_hand.append(deck[0])
            deck.pop(0)
        if len(player_hand) == 0:
            print(f"{current_turn} has won the game!")
            time.sleep(5)
            break

        continue







import os
import random
import time

def create_deck():
    deck = []
    suits = ("\u2665","\u2666","\u2660","\u2663")
    ranks = ("Jack","Queen","King","Ace")
    number_of_decks = 2

    for i in range(number_of_decks):
        for suit in suits:
            for j in range(2,11):
                deck.append((j,suit))
            for rank in ranks:
                deck.append((rank,suit))
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
def terminal_clear():
    return os.system('cls' if os.name == 'nt' else 'clear')
def time_delay():
    return time.sleep(2)

if __name__ == "__main__":
    deck = create_deck()
    shuffled_deck = deck_shuffle(deck)
    players = player_creator(int(input("How many players will be playing today?\nCrazy 8 allows 2-8 players.If you want to play with CPU, enter 1: ")))
    hands, deck = deal_hands(players,deck)
    pile = pile(deck)
    print(pile)
    while True:

        terminal_clear()
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
        deck_command = f"{len(playable_cards) + 1}. Pick card from deck."
        if current_turn == "cpu":
            time.sleep(2)
            played_card = random.choice(range(1,len(playable_cards)+1))
        else:
            print(f"Select one of the following playable options to play. Pick from 1 to {len(playable_cards)+1}.")

            for i in playable_cards:
                print(f"{playable_cards.index(i)+1}. {i}")
            print(deck_command)
            played_card = int(input(""))
        deck_command = int(deck_command.split(".")[0])

        if played_card != deck_command:
            terminal_clear()
            print(f"{current_turn} has played {playable_cards[played_card-1]}")
            time_delay()
            pile = playable_cards[played_card-1]
            player_hand.remove(pile)
        else:
            terminal_clear()
            print(f"You picked up {deck[0]}")
            time_delay()
            player_hand.append(deck[0])
            deck.pop(0)
        if len(player_hand) == 0:
            print(f"{current_turn} has won the game!")
            time_delay()
            break

        continue







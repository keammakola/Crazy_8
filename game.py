import random
import os
import time

def create_deck():
    deck = []
    suits = ("\u2665","\u2666","\u2660","\u2663")
    ranks = ("Jack","Queen","King","Ace")
    decks_num = 2

    for i in range(decks_num):
        for suit in suits:
            for j in range(2,11):
                deck.append((j,suit))
            for rank in ranks:
                deck.append((rank,suit))

    return deck,suits
def shuffler(deck):
    random.shuffle(deck)
def player_creator(number:int):
    players = []
    for i in range(number):
        players.append(f"player_{i + 1}")
    if number == 1:
        players.append("cpu")
    return players
def deal_cards(hand,number,deck):
    for i in range(number):
        hand.append(deck[0])
        deck.pop(0)
    return deck,hand
def pile_creator(deck):
    pile = []
    pile += deck[0]
    deck.pop(0)
    return pile,deck
def terminal_clear():
    return os.system('cls' if os.name == 'nt' else 'clear')
def turn_selector(players):
    current_turn = players[0]
    next_turn = players[1]
    players.append(players[0])
    players.pop(0)
    return current_turn , players, next_turn
def time_delay():
    return time.sleep(0)
def game_initialisation():
    deck,suits = create_deck()
    shuffler(deck)
    players_input = int(input("How many players will be playing today?\nCrazy 8 allows 2-8 players.If you want to play with CPU, enter 1: "))
    players = player_creator(players_input)
    player_hands = {}
    for player in players:
        hand = []
        deck , hand = deal_cards(hand,8,deck)
        player_hands[player] = hand
    pile,deck = pile_creator(deck)

    return deck , players , player_hands,pile,suits
def take_two(next_hand,deck):
    return deal_cards(next_hand,2,deck)
def skip(players):
    players.append(players[0])
    players.pop(0)
    return players

def game_loop(players,pile):
    next_suit = "null"
    while True:
        terminal_clear()
        current_turn , players, next_turn= turn_selector(players)
        next_hand = player_hands[next_turn]
        player_hand = player_hands[current_turn]
        print(f"It is {current_turn}'s turn.\n\nHere are your cards:\n{player_hand} \n\nCurrent card on the pile: {pile}\n")
        pile_card_number = pile[0]
        if pile_card_number == 8:
            pile_suit = next_suit
        else:
            pile_suit = pile[1]
        playable_cards = []
        for card in player_hand:
            if next_suit == "null":
                if card[0] == pile_card_number or card[1] == pile_suit or card[0] == 8:
                    if card not in playable_cards:
                        playable_cards.append(card)
            else:
                if card[1] == next_suit or card[0] == 8:
                    if card not in playable_cards:
                        playable_cards.append(card)
        deck_command = f"{len(playable_cards) + 1}. Pick card from deck."
        if current_turn == "cpu":
            time.sleep(2)
            played_card = random.choice(range(1, len(playable_cards) + 1))
        else:
            if next_suit == "null":
                print(f"Select one of the following playable options to play. Pick from 1 to {len(playable_cards) + 1}.")
            else:
                print(f"You can now play any card that is {next_suit} or an 8. Pick from 1 to {len(playable_cards) + 1}.")

            for i in playable_cards:
                print(f"{playable_cards.index(i) + 1}. {i}")
            print(deck_command)
            played_card = int(input(""))
        deck_command = int(deck_command.split(".")[0])

        if played_card != deck_command:
            terminal_clear()
            print(f"{current_turn} has played {playable_cards[played_card - 1]}")
            next_suit = "null"
            if playable_cards[played_card - 1][0] == 2:
                take_two(next_hand,deck)
                print(f"{current_turn} has made {next_turn} pick up 2 cards")
            elif playable_cards[played_card - 1][0] == 7:
                players = skip(players)
                print(f"{current_turn} has skipped {next_turn}.")
            elif playable_cards[played_card - 1][0] == "Jack":
                players.reverse()
                players = skip(players)
                print(f"{current_turn} has reversed the order of play.")
            elif playable_cards[played_card - 1][0] == 8:
                suit_choice = int(input(
                    f"You have played a 'change suits' card. Pick one colour you wish the next player should play\n1. {suits[0]}\n2. {suits[1]}\n3. {suits[2]}\n4. {suits[3]}\n "))
                if suit_choice == 1:
                    next_suit = suits[0]
                elif suit_choice == 2:
                    next_suit = suits[1]
                elif suit_choice == 3:
                    next_suit = suits[2]
                elif suit_choice == 4:
                    next_suit = suits[3]
                else:
                    print("Invalid choice, defaulting to Hearts.")
                    next_suit = suits[0]

            time_delay()
            pile = playable_cards[played_card - 1]
            player_hand.remove(pile)
        else:
            terminal_clear()
            print(f"You picked up {deck[0]}")
            time_delay()
            deal_cards(player_hand,1,deck)
        if len(player_hand) == 0:
            print(f"{current_turn} has won the game!")
            time_delay()
            break

        continue

if __name__ == "__main__":
    deck,players,player_hands,pile,suits = (game_initialisation())
    game_loop(players,pile)


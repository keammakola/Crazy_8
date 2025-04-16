import random
import os
import time

def create_deck():
    deck = []
    suits = ("\u2665","\u2666","\u2660","\u2663")
    ranks = ("Jack","Queen","King","Ace")
    decks_num = 2

    for _ in range(decks_num):
        for suit in suits:
            for j in range(2, 11):
                deck.append((j, suit))
            for rank in ranks:
                deck.append((rank, suit))

    return deck, suits

def shuffler(deck):
    random.shuffle(deck)

def player_creator(number: int):
    players = [f"player_{i + 1}" for i in range(number)]
    if number == 1:
        players.append("cpu")
    return players

def deal_cards(hand, number, deck):
    for _ in range(number):
        if deck:
            hand.append(deck.pop(0))
        else:
            print("Deck is empty, cannot deal more cards.")
    return deck, hand

def pile_creator(deck):
    pile = []
    if deck:
        pile += deck.pop(0)
    else:
        print("Deck is empty, no starting pile card.")
    return pile, deck

def terminal_clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def turn_selector(players):
    current_turn = players[0]
    next_turn = players[1]
    players.append(players.pop(0))
    return current_turn, players, next_turn

def time_delay():
    time.sleep(2)

def game_initialisation():
    deck, suits = create_deck()
    shuffler(deck)

    while True:
        try:
            players_input = int(input("How many players will be playing today?\nCrazy 8 allows 2-8 players. Enter 1 for CPU: "))
            if 1 <= players_input <= 8:
                break
            else:
                print("Please enter a valid number between 1 and 8.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    players = player_creator(players_input)
    player_hands = {}
    for player in players:
        hand = []
        deck, hand = deal_cards(hand, 8, deck)
        player_hands[player] = hand

    pile, deck = pile_creator(deck)

    return deck, players, player_hands, pile, suits

def take_two(next_hand, deck):
    return deal_cards(next_hand, 2, deck)

def skip(players):
    players.append(players.pop(0))
    return players

def game_loop(players, pile, player_hands, suits, deck):
    next_suit = "null"
    while True:
        terminal_clear()
        current_turn, players, next_turn = turn_selector(players)
        next_hand = player_hands[next_turn]
        player_hand = player_hands[current_turn]

        print(f"It is {current_turn}'s turn.")
        time_delay()
        print(f"\n\nYour cards:\n{player_hand}\n\nCurrent pile card: {pile}\n")
        pile_card_number = pile[0]
        pile_suit = next_suit if pile_card_number == 8 else pile[1]

        playable_cards = []
        for card in player_hand:
            if next_suit == "null":
                if card[0] == pile_card_number or card[1] == pile_suit or card[0] == 8:
                    playable_cards.append(card)
            else:
                if card[1] == next_suit or card[0] == 8:
                    playable_cards.append(card)

        deck_command = f"{len(playable_cards) + 1}. Pick card from deck."

        if current_turn == "cpu":
            time.sleep(1)
            played_card = random.choice(range(1, len(playable_cards) + 1)) if playable_cards else len(playable_cards) + 1
        else:
            if next_suit == "null":
                print(f"Select an option 1 to {len(playable_cards) + 1}")
            else:
                print(f"You can play a {next_suit} or an 8. Pick from 1 to {len(playable_cards) + 1}.")

            for i, card in enumerate(playable_cards):
                print(f"{i + 1}. {card}")
            print(deck_command)

            while True:
                try:
                    played_card = int(input("Enter your choice: "))
                    if 1 <= played_card <= len(playable_cards) + 1:
                        break
                    else:
                        print("Choice out of range.")
                except ValueError:
                    print("Invalid input. Enter a number.")

        deck_command_number = int(deck_command.split(".")[0])

        if played_card != deck_command_number:
            terminal_clear()
            played_card_value = playable_cards[played_card - 1]
            print(f"{current_turn} played {played_card_value}")
            next_suit = "null"

            if played_card_value[0] == 2:
                take_two(next_hand, deck)
                print(f"{current_turn} makes {next_turn} pick 2 cards.")
            elif played_card_value[0] == 7:
                players = skip(players)
                print(f"{current_turn} skipped {next_turn}.")
            elif played_card_value[0] == "Jack":
                players.reverse()
                players = skip(players)
                print(f"{current_turn} reversed the order.")
            elif played_card_value[0] == 8:
                while True:
                    try:
                        suit_choice = int(input(
                            f"Choose a suit:\n1. {suits[0]}\n2. {suits[1]}\n3. {suits[2]}\n4. {suits[3]}\nChoice: "))
                        if 1 <= suit_choice <= 4:
                            next_suit = suits[suit_choice - 1]
                            break
                        else:
                            print("Pick a number 1-4.")
                    except ValueError:
                        print("Invalid input. Enter a number.")

            time_delay()
            pile = played_card_value
            player_hand.remove(played_card_value)
        else:
            if deck:
                print(f"You picked up {deck[0]}")
                time_delay()
                deal_cards(player_hand, 1, deck)
            else:
                print("Deck is empty. Skipping pick up.")
            time_delay()

        if not player_hand:
            print(f"{current_turn} wins the game!")
            time_delay()
            break

if __name__ == "__main__":
    deck, players, player_hands, pile, suits = game_initialisation()
    game_loop(players, pile, player_hands, suits, deck)

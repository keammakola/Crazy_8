import random
import os
import time
from typing import List, Tuple

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.suits = ("\u2665","\u2666","\u2660","\u2663")
        self.ranks = ("Jack","Queen","King","Ace")
        self.decks_num = 2
        self.cards: List[Card] = []
        self.create_deck()

    def create_deck(self):
        for _ in range(self.decks_num):
            for suit in self.suits:
                for j in range(2, 11):
                    self.cards.append(Card(j, suit))
                for rank in self.ranks:
                    self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, number: int) -> List[Card]:
        hand = []
        for _ in range(number):
            if self.cards:
                hand.append(self.cards.pop(0))
            else:
                print("Deck is empty, cannot deal more cards.")
        return hand

    def draw(self) -> Card:
        if self.cards:
            return self.cards.pop(0)
        else:
            print("Deck is empty.")
            return None

class CrazyEightGame:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.player_hands = {}
        self.pile = []
        self.suits = self.deck.suits
        self.next_suit = "null"

    def terminal_clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def time_delay(self):
        time.sleep(2)

    def player_creator(self, number):
        players = [f"player_{i + 1}" for i in range(number)]
        if number == 1:
            players.append("cpu")
        return players

    def deal_cards(self, hand, number):
        hand.extend(self.deck.deal(number))
        return hand

    def pile_creator(self):
        if self.deck.cards:
            self.pile = [self.deck.draw()]
        else:
            print("Deck is empty, no starting pile card.")

    def turn_selector(self):
        current_turn = self.players[0]
        next_turn = self.players[1]
        self.players.append(self.players.pop(0))
        return current_turn, next_turn

    def take_two(self, hand):
        hand.extend(self.deck.deal(2))

    def skip(self):
        self.players.append(self.players.pop(0))

    def game_initialisation(self):
        self.deck.shuffle()

        while True:
            try:
                players_input = int(input("How many players will be playing today?\nCrazy 8 allows 2-8 players. Enter 1 for CPU: "))
                if 1 <= players_input <= 8:
                    break
                else:
                    print("Please enter a valid number between 1 and 8.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        self.players = self.player_creator(players_input)

        for player in self.players:
            hand = []
            hand = self.deal_cards(hand, 8)
            self.player_hands[player] = hand

        self.pile_creator()

    def game_loop(self):
        while True:
            self.terminal_clear()
            current_turn, next_turn = self.turn_selector()
            next_hand = self.player_hands[next_turn]
            player_hand = self.player_hands[current_turn]

            print(f"It is {current_turn}'s turn.")
            self.time_delay()
            print(f"\n\nYour cards:\n{player_hand}\n\nCurrent pile card: {self.pile[0]}\n")

            pile_card_number = self.pile[0].rank
            pile_suit = self.next_suit if pile_card_number == 8 else self.pile[0].suit

            playable_cards = []
            for card in player_hand:
                if self.next_suit == "null":
                    if card.rank == pile_card_number or card.suit == pile_suit or card.rank == 8:
                        playable_cards.append(card)
                else:
                    if card.suit == self.next_suit or card.rank == 8:
                        playable_cards.append(card)

            deck_command = f"{len(playable_cards) + 1}. Pick card from deck."

            if current_turn == "cpu":
                time.sleep(1)
                played_card = random.choice(range(1, len(playable_cards) + 1)) if playable_cards else len(playable_cards) + 1
            else:
                if self.next_suit == "null":
                    print(f"Select an option 1 to {len(playable_cards) + 1}")
                else:
                    print(f"You can play a {self.next_suit} or an 8. Pick from 1 to {len(playable_cards) + 1}.")

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
                self.terminal_clear()
                played_card_value = playable_cards[played_card - 1]
                print(f"{current_turn} played {played_card_value}")
                self.next_suit = "null"

                if played_card_value.rank == 2:
                    self.take_two(next_hand)
                    print(f"{current_turn} makes {next_turn} pick 2 cards.")
                elif played_card_value.rank == 7:
                    self.skip()
                    print(f"{current_turn} skipped {next_turn}.")
                elif played_card_value.rank == "Jack":
                    self.players.reverse()
                    self.skip()
                    print(f"{current_turn} reversed the order.")
                elif played_card_value.rank == 8:
                    while True:
                        try:
                            suit_choice = int(input(
                                f"Choose a suit:\n1. {self.suits[0]}\n2. {self.suits[1]}\n3. {self.suits[2]}\n4. {self.suits[3]}\nChoice: "))
                            if 1 <= suit_choice <= 4:
                                self.next_suit = self.suits[suit_choice - 1]
                                break
                            else:
                                print("Pick a number 1-4.")
                        except ValueError:
                            print("Invalid input. Enter a number.")

                self.time_delay()
                self.pile[0] = played_card_value
                player_hand.remove(played_card_value)
            else:
                if self.deck.cards:
                    drawn_card = self.deck.draw()
                    print(f"You picked up {drawn_card}")
                    self.time_delay()
                    player_hand.append(drawn_card)
                else:
                    print("Deck is empty. Skipping pick up.")
                self.time_delay()

            if not player_hand:
                print(f"{current_turn} wins the game!")
                self.time_delay()
                break

if __name__ == "__main__":
    game = CrazyEightGame()
    game.game_initialisation()
    game.game_loop()

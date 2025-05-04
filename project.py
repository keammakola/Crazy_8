import random
import os
import time
from typing import List, Optional

class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = str(rank)
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.suits = ("\u2665", "\u2666", "\u2660", "\u2663")
        self.ranks = [str(n) for n in range(2, 11)] + ["Jack", "Queen", "King", "Ace"]
        self.decks_num = 2
        self.cards: List[Card] = []
        self.create_deck()

    def create_deck(self):
        self.cards.clear()
        for _ in range(self.decks_num):
            for suit in self.suits:
                for rank in self.ranks:
                    self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, number: int) -> List[Card]:
        hand = []
        for _ in range(number):
            if not self.cards:
                break
            hand.append(self.cards.pop(0))
        return hand

    def draw(self) -> Optional[Card]:
        if self.cards:
            return self.cards.pop(0)
        else:
            return None

class CrazyEightGame:
    def __init__(self):
        self.deck = Deck()
        self.players: List[str] = []
        self.player_hands: dict[str, List[Card]] = {}
        self.pile: List[Card] = []
        self.suits = self.deck.suits
        self.next_suit = "null"

    def terminal_clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def time_delay(self, seconds: int = 2):
        time.sleep(seconds)

    def player_creator(self, number: int) -> List[str]:
        players = [f"player_{i + 1}" for i in range(number)]
        if number == 1:
            players.append("cpu")
        return players

    def deal_cards(self, number: int) -> List[Card]:
        return self.deck.deal(number)

    def pile_creator(self):
        while True:
            card = self.deck.draw()
            if card and card.rank != "8":
                self.pile.append(card)
                break

    def turn_selector(self) -> tuple[str, str]:
        current_turn = self.players[0]
        next_turn = self.players[1]
        self.players.append(self.players.pop(0))
        return current_turn, next_turn

    def take_two(self, hand: List[Card]):
        hand.extend(self.deck.deal(2))

    def skip(self):
        self.players.append(self.players.pop(0))

    def recycle_pile_into_deck(self):
        if len(self.pile) > 1:
            top_card = self.pile.pop(0)
            self.deck.cards.extend(self.pile)
            self.deck.shuffle()
            self.pile = [top_card]
            print("Deck was empty. Recycled discard pile into deck.")

    def game_initialisation(self):
        self.deck.shuffle()

        while True:
            try:
                players_input = int(input("How many players will be playing today?\nCrazy 8 allows 2-8 players. Enter 1 for CPU: "))
                if 1 <= players_input <= 8:
                    break
                else:
                    self.terminal_clear()
                    print("Please enter a valid number between 1 and 8.")
            except ValueError:
                self.terminal_clear()
                print("Invalid input. Please enter a number.")

        self.players = self.player_creator(players_input)

        for player in self.players:
            self.player_hands[player] = self.deal_cards(8)

        self.pile_creator()

    def game_loop(self):
        while True:
            self.terminal_clear()
            if not self.deck.cards:
                self.recycle_pile_into_deck()

            current_turn, next_turn = self.turn_selector()
            next_hand = self.player_hands[next_turn]
            player_hand = self.player_hands[current_turn]

            print(f"It is {current_turn}'s turn.")
            self.time_delay()

            pile_card = self.pile[0]
            pile_suit = self.next_suit if self.next_suit != "null" else pile_card.suit
            print(f"\nYour cards:\n{player_hand}\n\nCurrent pile card: {pile_card} (Suit in play: {pile_suit})\n")

            playable_cards = get_playable_cards(player_hand, pile_card, self.next_suit)
            self.next_suit = "null"

            if current_turn == "cpu":
                if playable_cards:
                    played_card_value = random.choice(playable_cards)
                    print(f"CPU played {played_card_value}")
                    self.time_delay()
                else:
                    drawn = self.deck.draw()
                    if not drawn:
                        self.recycle_pile_into_deck()
                        drawn = self.deck.draw()
                    print(f"CPU picked up {drawn}")
                    player_hand.append(drawn)
                    self.time_delay()
                    continue
            else:
                for i, card in enumerate(playable_cards, start=1):
                    print(f"{i}. {card}")
                print(f"{len(playable_cards) + 1}. Pick card from deck.")

                while True:
                    try:
                        choice = int(input("Enter your choice: "))
                        if 1 <= choice <= len(playable_cards) + 1:
                            break
                        else:
                            print("Choice out of range.")
                    except ValueError:
                        print("Invalid input. Enter a number.")

                if choice == len(playable_cards) + 1:
                    drawn = self.deck.draw()
                    if not drawn:
                        self.recycle_pile_into_deck()
                        drawn = self.deck.draw()
                    print(f"You picked up {drawn}")
                    self.time_delay()
                    if drawn and is_valid_card(drawn, pile_card, pile_suit):
                        print(f"You can play {drawn}")
                        play = input("Play it? (y/n): ").strip().lower()
                        if play == "y":
                            played_card_value = drawn
                        else:
                            player_hand.append(drawn)
                            continue
                    else:
                        player_hand.append(drawn)
                        continue
                else:
                    played_card_value = playable_cards[choice - 1]

            print(f"{current_turn} played {played_card_value}")
            self.pile[0] = played_card_value
            player_hand.remove(played_card_value)

            if played_card_value.rank == "2":
                self.take_two(next_hand)
                print(f"{current_turn} makes {next_turn} pick 2 cards.")
            elif played_card_value.rank == "7":
                self.skip()
                print(f"{current_turn} skipped {next_turn}.")
            elif played_card_value.rank == "Jack":
                self.players = reverse_players(self.players)
                print(f"{current_turn} reversed the order.")
            elif played_card_value.rank == "8":
                if current_turn == "cpu":
                    self.next_suit = random.choice(self.suits)
                    print(f"CPU chose the suit {self.next_suit}")
                else:
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

            if not player_hand:
                print(f"{current_turn} wins the game!")
                break


def is_valid_card(card: Card, pile_card: Card, next_suit: str) -> bool:
    if next_suit != "null":
        return card.suit == next_suit or card.rank == "8"
    return card.rank == pile_card.rank or card.suit == pile_card.suit or card.rank == "8"

def get_playable_cards(hand: List[Card], pile_card: Card, next_suit: str) -> List[Card]:
    return [card for card in hand if is_valid_card(card, pile_card, next_suit)]

def reverse_players(players: List[str]) -> List[str]:
    reversed_players = players[::-1]
    reversed_players.insert(0, reversed_players.pop())
    return reversed_players

def main():
    game = CrazyEightGame()
    game.game_initialisation()
    game.game_loop()

if __name__ == "__main__":
    main()

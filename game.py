import random
import os
import time


def create_deck(decks_num=2):
    suits = ("\u2665", "\u2666", "\u2660", "\u2663")
    ranks = list(range(2, 11)) + ["Jack", "Queen", "King", "Ace"]
    return [(rank, suit) for _ in range(decks_num) for suit in suits for rank in ranks]


def shuffle_deck(deck):
    random.shuffle(deck)


def create_players(num_players):
    players = [f"player_{i + 1}" for i in range(num_players)]
    if num_players == 1:
        players.append("cpu")
    return players


def deal_cards(deck, num_cards=8):
    return [deck.pop(0) for _ in range(num_cards)]


def initialize_game():
    deck = create_deck()
    shuffle_deck(deck)
    num_players = int(input("How many players? (2-8, enter 1 for CPU): "))
    players = create_players(num_players)
    player_hands = {player: deal_cards(deck) for player in players}
    pile = [deck.pop(0)]
    return deck, players, player_hands, pile


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def next_turn(players):
    players.append(players.pop(0))
    return players[0]


def display_game_state(current_turn, player_hand, pile):
    clear_terminal()
    print(f"{current_turn}'s turn.\nYour cards: {player_hand}\nCurrent card: {pile[-1]}\n")


def get_playable_cards(player_hand, pile):
    pile_rank, pile_suit = pile[-1]
    return [card for card in player_hand if card[0] == pile_rank or card[1] == pile_suit]


def player_move(current_turn, player_hand, pile, deck):
    playable_cards = get_playable_cards(player_hand, pile)
    if playable_cards:
        if current_turn == "cpu":
            time.sleep(2)
            chosen_card = random.choice(playable_cards)
        else:
            for idx, card in enumerate(playable_cards, 1):
                print(f"{idx}. {card}")
            print(f"{len(playable_cards) + 1}. Pick from deck")
            choice = int(input("Choose an option: "))
            if choice == len(playable_cards) + 1:
                chosen_card = None
            else:
                chosen_card = playable_cards[choice - 1]

        if chosen_card:
            player_hand.remove(chosen_card)
            pile.append(chosen_card)
            print(f"{current_turn} played {chosen_card}")
            time.sleep(2)


    if playable_cards or chosen_card is not None:
        drawn_card = deck.pop(0)
        player_hand.append(drawn_card)
        print(f"{current_turn} picked {drawn_card}")
        time.sleep(2)

def game_loop(players, player_hands, pile, deck):
    while True:
        clear_terminal()
        current_turn = next_turn(players)
        display_game_state(current_turn, player_hands[current_turn], pile)
        player_move(current_turn, player_hands[current_turn], pile, deck)

        if player_hands[current_turn] is not True:
            print(f"{current_turn} has won!")
            break


if __name__ == "__main__":
    deck, players, player_hands, pile = initialize_game()
    game_loop(players, player_hands, pile, deck)

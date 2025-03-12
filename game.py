import random

def create_deck():
    deck = []
    suits = ("hearts","diamonds","spades","clubs")
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

if __name__ == "__main__":
    deck = create_deck()
    shuffled_deck = deck_shuffle(deck)
    players = player_creator(int(input("How many players will be playing today?\nCrazy 8 allows 2-8 players.If you want to play with CPU, enter 1: ")))
    hands, deck = deal_hands(players,deck)
    pile = pile(deck)
    print(pile)



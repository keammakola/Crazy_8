import random

def create_deck():
    deck = []
    suits = ("hearts","diamonds","spades","clubs")
    faces = ("jack","queen","king","ace")

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

if __name__ == "__main__":
    deck = create_deck()
    shuffled_deck = deck_shuffle(deck)
    players = player_creator(int(input("How many players will be playing today?\nCrazy 8 allows 2-8 players.If you want to play with CPU, enter 1: ")))
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


if __name__ == "__main__":
    deck = create_deck()
    deck_shuffle(deck)
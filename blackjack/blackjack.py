# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


class Card:
    """ This class will create the cards """

    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        

class Hand:
    """ This class will create the hands """

    def __init__(self):
        self.hand = [] # create Hand object

    def __str__(self):
        return "Hand contains " + ' '.join(map(str,self.hand))# return a string representation of a hand

    def add_card(self, card):
        self.hand.append(card)# add a card object to a hand

    def get_value(self):
        value = 0
        has_ace = False
        for card in self.hand:
            rank = card.get_rank()
            value += VALUES[rank]
            if rank == 'A':
                has_ace = True
        if has_ace and value < 12:
            value += 10
        return value # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        for card in self.hand:
            card.draw(canvas,pos)
            pos[0] += CARD_SIZE[0] + 10 # draw a hand on the canvas, use the draw method for cards
        

class Deck:
    """ This class will create the decks """
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        return "Deck contains " + ' '.join(map(str,self.deck))


def deal():
    """
    defining the event handlers
    """
    global outcome, in_play, deck, player_hand, dealer_hand, score

    if in_play:
        score -= 1
        outcome = "You lost the round! New deal?"
    else:
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        dealer_hand = Hand()

        for i in range(2):
            player_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())

        outcome = ""
        in_play = True


def hit():
    global outcome, in_play, deck, player_hand, score

    if in_play:
        player_hand.add_card(deck.deal_card())

        if player_hand.get_value() > 21:
            outcome = "You have busted! New deal?"
            in_play = False
            score -= 1


def stand():
    global outcome, in_play, deck, dealer_hand, player_hand, score

    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())

        if dealer_hand.get_value() > 21:
            outcome = "Dealer busted! New deal?"
            score += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = "Dealer wins! New deal?"
            score -= 1
        else:
            outcome = "You win! New deal?"
            score += 1

        in_play = False


def draw(canvas):
    """
    Draw handler
    """
    global player_hand, dealer_hand, in_play

    canvas.draw_text("Blackjack", (200, 50), 50, "White")

    canvas.draw_text("Dealer", (50, 150), 30, "Black")
    dealer_hand.draw(canvas, [50, 170])

    canvas.draw_text("Player", (50, 350), 30, "Black")
    player_hand.draw(canvas, [50, 370])

    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [86,218], CARD_BACK_SIZE)

    # draw outcome and score
    canvas.draw_text(outcome, (200, 350), 30, "Black")
    canvas.draw_text("Score: " + str(score), (400, 150), 30, "Black")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

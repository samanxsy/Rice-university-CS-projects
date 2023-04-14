import simplegui
import random


def new_game():
    """
    helper function to initialize globals
    """
    global deck, exposed, state, card1, card2, turns
    deck = [i % 8 for i in range(16)]
    random.shuffle(deck)
    exposed = [False] * 16
    state = 0
    card1, card2 = None, None
    turns = 0
    label.set_text("Turns = " + str(turns))


def mouseclick(pos):
    """
    define event handlers
    """
    global state, card1, card2, turns
    card_index = pos[0] // 50
    if not exposed[card_index]:
        exposed[card_index] = True
        if state == 0:
            state = 1
            card1 = card_index
        elif state == 1:
            state = 2
            card2 = card_index
            turns += 1
        else:
            state = 1
            if deck[card1] != deck[card2]:
                exposed[card1], exposed[card2] = False, False
            card1 = card_index
        label.set_text("Turns = " + str(turns))


def draw(canvas):
    """
    cards are logically 50x100 pixels in size  
    """
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(deck[i]), (50*i+15, 60), 40, "White")
        else:
            canvas.draw_polygon([(50*i, 0), (50*(i+1), 0), (50*(i+1), 100), (50*i, 100)], 1, "Black", "Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

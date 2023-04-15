import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == RIGHT:
        ball_vel = [random.randrange(2, 4),-random.randrange(1, 3)]
    elif direction == LEFT:
        ball_vel = [-random.randrange(2, 4),-random.randrange(1, 3)]


def new_game():
    """
    This function defines the event handlers
    """

    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    paddle1_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(random.choice([LEFT, RIGHT]))


def draw(canvas):
    """
    This Function draws the game (Canvas) 
    """
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # Draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # Update paddle's vertical position, keeping paddle on the screen
    if paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT and paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT and paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    # Draw paddles
    canvas.draw_polygon([(0, paddle1_pos - HALF_PAD_HEIGHT), (PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT),
                         (PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), (0, paddle1_pos + HALF_PAD_HEIGHT)], 1, "White", "White")
    canvas.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), (WIDTH, paddle2_pos - HALF_PAD_HEIGHT),
                         (WIDTH, paddle2_pos + HALF_PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT)], 1, "White", "White")
    
    # Determine whether paddle and ball collide
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)
    
    # Draw scores
    canvas.draw_text(str(score1), [WIDTH / 4, 50], 50, "White")
    canvas.draw_text(str(score2), [3 * WIDTH / 4, 50], 50, "White")

        
def keydown(key):
    """
    Defining the keydown event handler behaviour
    """
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -5
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 5
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -5
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 5


def keyup(key):
    """
    Defining the keyup event handler behaviour
    """
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()

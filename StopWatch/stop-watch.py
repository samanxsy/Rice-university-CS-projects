import simplegui

# Global variables
time = 0
stop_count = 0
win_count = 0
is_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """
    This function will define the format
    """
    minutes = t // 600
    seconds = (t // 10 ) % 60
    tenths_of_seconds = t % 10
    return "{:01d}:{:02d}.{:01d}".format(minutes, seconds, tenths_of_seconds)


def start_handler():
    """
    This function defines event handlers for buttons; 'Start', 'Stop', 'Reset'
    """
    global is_running
    is_running = True
    timer.start()
    

def stop_handler():
    """
    This function stops the handler
    """
    global stop_count, win_count, is_running
    if is_running:
        timer.stop()
        is_running = False
        stop_count += 1
        if time % 10 == 0:
            win_count += 1

            
def reset_handler():
    """
    This function Restarts the timer
    """
    global time, stop_count, win_count
    time = stop_count = win_count = 0
    timer.stop()


def timer_handler():
    """
    This Function defines event handler for timer with 0.1 sec interval
    """
    global time
    time += 1

    
def draw_handler(canvas):
    """
    Draw Handlers
    """
    canvas.draw_text(format(time), [90, 110], 42, "White")
    canvas.draw_text("{}/{}".format(win_count, stop_count), [245, 30], 24, "Green")

# Creating the Frame
frame = simplegui.create_frame("Stopwatch: The Game!", 300, 200)

# Registering the event handlers
frame.add_button("Start", start_handler, 100)
frame.add_button("Stop", stop_handler, 100)
frame.add_button("Reset", reset_handler, 100)
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)

# Starting the Frame
frame.start()

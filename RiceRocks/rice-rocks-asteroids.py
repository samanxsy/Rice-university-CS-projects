import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
MAX_ROCK = 12
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__ (self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float ('inf')
        self.animated = animated

    def get_center (self):
        return self.center

    def get_size (self):
        return self.size

    def get_radius (self):
        return self.radius

    def get_lifespan (self):
        return self.lifespan

    def get_animated (self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-ued in non-commercial projects, please credit Kim
debris_info = ImageInfo ([320, 240], [640, 480])
debris_image = simplegui.load_image ("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris_blend.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo ([400, 300], [800, 600])
nebula_image = simplegui.load_image ("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")

# splash image
splash_info = ImageInfo ([200, 150], [400, 300])
splash_image = simplegui.load_image ("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo ([45, 45], [90, 90], 35)
ship_image = simplegui.load_image ("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo ([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image ("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo ([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image ("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo ([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image ("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound ("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound ("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume (.5)
ship_thrust_sound = simplegui.load_sound ("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound ("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


def angle_to_vector (ang):
    return [math.cos (ang), math.sin (ang)]

def dist (p, q):
    return math.sqrt ( ( (p[0] - q[0]) ** 2) +  ( (p[1] - q[1]) ** 2))


class Ship:
    """ This is the Ship Class """
    def __init__ (self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center ()
        self.image_size = info.get_size ()
        self.radius = info.get_radius ()


    def draw (self,canvas):
        global started
        if self.thrust and started:
            canvas.draw_image (self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image (self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)


    def update (self):
        global started
        if started:
            # update angle
            self.angle += self.angle_vel
            # update position
            self.pos[0] =  (self.pos[0] + self.vel[0]) % WIDTH
            self.pos[1] =  (self.pos[1] + self.vel[1]) % HEIGHT
            # update velocity
            if self.thrust:
                acc = angle_to_vector (self.angle)
                self.vel[0] += acc[0] * .3
                self.vel[1] += acc[1] * .3
            self.vel[0] *= .99
            self.vel[1] *= .99


    def set_thrust (self, on):
        global started
        self.thrust = on
        if on and started:
            ship_thrust_sound.rewind ()
            ship_thrust_sound.play ()
        else:
            ship_thrust_sound.pause ()

    def increment_angle_vel (self):
        self.angle_vel += .06

    def decrement_angle_vel (self):
        self.angle_vel -= .06

    def shoot (self):
        global missile_group, started
        if started:
            forward = angle_to_vector (self.angle)
            missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
            missile_vel = [self.vel[0] + 8 * forward[0], self.vel[1] + 8 * forward[1]]
            missile_group.add (Sprite (missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))

    def get_position (self):
        return self.pos

    def get_radius (self):
        return self.radius


class Sprite:
    """ This is the Sprite Class """
    def __init__ (self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center ()
        self.image_size = info.get_size ()
        self.radius = info.get_radius ()
        self.lifespan = info.get_lifespan ()
        self.animated = info.get_animated ()
        self.age = 0
        if sound:
            sound.rewind ()
            sound.play ()

    def draw (self, canvas):
        if self.animated:
            canvas.draw_image (self.image, [self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image (self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update (self):
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] =  (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] =  (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        if self.age < self.lifespan:
            return False
        else:
            return True

    def get_position (self):
        return self.pos
    
    def get_radius (self):
        return self.radius
    
    def collide (self, other):
        if dist (self.pos, other.get_position ()) <= self.radius + other.get_radius ():
            return True
        else:
            return False


# key handlers to control ship
def keydown (key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel ()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel ()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust (True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot ()
        
def keyup (key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel ()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel ()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust (False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click (pos):
    global started, score, lives, MAX_ROCK
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size ()
    inwidth =  (center[0] - size[0] / 2) < pos[0] <  (center[0] + size[0] / 2)
    inheight =  (center[1] - size[1] / 2) < pos[1] <  (center[1] + size[1] / 2)
    if  (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = 3
        MAX_ROCK = 10
        ship_thrust_sound.rewind ()
        explosion_sound.rewind ()
        missile_sound.rewind ()
        soundtrack.rewind ()
        soundtrack.play ()


def draw (canvas):
    global time, started, score, lives, MAX_ROCK, rock_group, my_ship, explosion_group, missile_group

    # background
    time += 1
    wtime =  (time / 4) % WIDTH
    center = debris_info.get_center ()
    size = debris_info.get_size ()
    canvas.draw_image (nebula_image, nebula_info.get_center (), nebula_info.get_size (), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image (debris_image, center, size,  (wtime - WIDTH / 2, HEIGHT / 2),  (WIDTH, HEIGHT))
    canvas.draw_image (debris_image, center, size,  (wtime + WIDTH / 2, HEIGHT / 2),  (WIDTH, HEIGHT))

    # UI
    canvas.draw_text ("Lives", [50, 50], 22, "White")
    canvas.draw_text ("Score", [680, 50], 22, "White")
    canvas.draw_text (str (lives), [50, 80], 22, "White")
    canvas.draw_text (str (score), [680, 80], 22, "White")

    # The Ships Drawing & Updating
    my_ship.draw (canvas)
    my_ship.update ()

    # Sprites
    process_sprite_group (rock_group, canvas)
    process_sprite_group (explosion_group, canvas)
    process_sprite_group (missile_group, canvas)

    # collisions handling
    if group_collide (rock_group, my_ship) > 0:
        lives -= 1
    if lives == 0:
        started = False
        soundtrack.pause ()
        soundtrack.rewind ()
        my_ship = Ship ([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        rock_group = set ([])
        missile_group = set ([])
        explosion_group = set ([])
    score += group_group_collide (rock_group, missile_group) * 10
    if score > 360:
        ROCK_MAX = score // 30
    if not started:
        canvas.draw_image (splash_image, splash_info.get_center (), splash_info.get_size (), [WIDTH / 2, HEIGHT / 2], splash_info.get_size ())


def rock_spawner ():
    """
    Time handler for spawning a rock
    """
    global rock_group, my_ship, started, MAX_ROCK, asteroid_info
    rock_pos = [random.randrange (0, WIDTH), random.randrange (0, HEIGHT)]
    rock_vel = [random.random () * .6 - .3, random.random () * .6 - .3]
    rock_avel = random.random () * .2 - .1
    if started:
        if len (rock_group) < MAX_ROCK:
            if dist (rock_pos, my_ship.get_position ()) > asteroid_info.get_radius () + my_ship.get_radius () + 10:
                rock_group.add (Sprite (rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))


def group_collide (group, other):
    """
    Group Object collisions handling
    """
    noCollisions = 0
    removeSet = set ([])
    for sprite in group:
        if sprite.collide (other):
            explosion_group.add (Sprite (sprite.pos, [0, 0], 0, 0, explosion_image, explosion_info))
            explosion_sound.rewind ()
            explosion_sound.play ()
            removeSet.add (sprite)
            noCollisions += 1
    if len (removeSet) > 0:
        group.difference_update (removeSet)
    return noCollisions


def group_group_collide (groupOne, groupTwo):
    """
    Group-Group collisions handling
    """
    noCollisions = 0
    removeSet = set ([])
    for sprite in groupOne:
        if group_collide (groupTwo, sprite) > 0:
            removeSet.add (sprite)
            noCollisions += 1
    if len (removeSet) > 0:
        groupOne.difference_update (removeSet)
    return noCollisions


def process_sprite_group (group, canvas):
    """
    Updates and Draws the Sprites
    """
    removeSet = set ([])
    for sprite in group:
        if sprite.update ():
            removeSet.add (sprite)
        else:
            sprite.draw (canvas)
    if len (removeSet) > 0:
        group.difference_update (removeSet)

# initialize stuff
frame = simplegui.create_frame ("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship ([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set ([])
missile_group = set ([])
explosion_group = set ([])

# register handlers
frame.set_keyup_handler (keyup)
frame.set_keydown_handler (keydown)
frame.set_mouseclick_handler (click)
frame.set_draw_handler (draw)

timer = simplegui.create_timer (1000.0, rock_spawner)

# get things rolling
timer.start ()
frame.start ()
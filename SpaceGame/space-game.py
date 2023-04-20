import simplegui
import math
import random

# Globals
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

class ImageInfo:
    """
    Image specifications
    """
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


def angle_to_vector(ang):
    """
    helper functions to handle transformations
    """
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


class Ship:
    """ The Ship Class """
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image,[130,45],self.image_size,self.pos,self.image_size,self.angle)
        else:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)

    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0])% WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1])% HEIGHT
        friction = 0.04
        acceleration = 0.11
        self.vel[0] *= (1-friction)
        self.vel[1] *= (1-friction)
        if self.thrust:
            direction = angle_to_vector(self.angle)
            self.vel[0] += direction[0] * acceleration
            self.vel[1] += direction[1] * acceleration
    def decrease_angle_vel(self):
        self.angle_vel -= 0.06
    def increase_angle_vel(self):
        self.angle_vel += 0.06
    def update_thrust(self,is_thrust):
        self.thrust = is_thrust
        if self.thrust:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()

    def shoot_missile(self):      
        global a_missile
        direction = angle_to_vector(self.angle)
        missile_position = [self.pos[0] + direction[0] * self.radius,self.pos [1] + direction[1] * self.radius]
        missile_velocity = [self.vel[0] + direction[0] * 5 , self.vel[1] + direction[1] * 5]
        a_missile = Sprite (missile_position, missile_velocity, self.angle, 0, missile_image,missile_info, missile_sound)


class Sprite:
    """ Sprite Class """
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0])% WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1])% HEIGHT       


def down(key):
    """ Key Handlers """
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrease_angle_vel()
    elif key ==  simplegui.KEY_MAP['right']:
        my_ship.increase_angle_vel()
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot_missile()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.update_thrust(True)


def up(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increase_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrease_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.update_thrust(False)


def draw(canvas):
    global time
    
    # Background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    my_ship.update()
    a_rock.update()
    a_missile.update()

    canvas.draw_text ('Lives: '+ str(lives), (50, 50), 50, "White")
    canvas.draw_text ('Score: '+ str(score), (600, 50), 50, "White")

   
def rock_spawner():
    """ Time Handler """
    global a_rock
    a_rock = Sprite ([random.randrange(WIDTH),random.randrange(HEIGHT)],[random.random()/2,random.random()/2],
                     0,random.random()/20, asteroid_image, asteroid_info)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(down)
frame.set_keyup_handler(up)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

import sys
import pygame
import random
pygame.init()
pygame.display.set_caption("RaceTraaaaaaaack")

# -------General
screen_width = 1680
screen_height = 1050
screenSize = screen_width, screen_height
screen = pygame.display.set_mode((screenSize))

Track_surf = pygame.Surface((screenSize))
Racer_surf = pygame.Surface((screenSize), pygame.SRCALPHA)
Menue_surf = pygame.Surface((screenSize))
Gui_surf = pygame.Surface((screenSize), pygame.SRCALPHA)

debug = True
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

fields = []
racersToChoose = [pygame.image.load("sprites/racers/racer01.png"),pygame.image.load("sprites/racers/racer02.png"),pygame.image.load("sprites/racers/racer03.png"),
                  pygame.image.load("sprites/racers/racer04.png"),pygame.image.load("sprites/racers/racer05.png"),pygame.image.load("sprites/racers/racer06.png"),
                  pygame.image.load("sprites/racers/racer07.png"),pygame.image.load("sprites/racers/racer08.png"),pygame.image.load("sprites/racers/racer09.png"),
                  pygame.image.load("sprites/racers/racer10.png"),pygame.image.load("sprites/racers/racer11.png"),pygame.image.load("sprites/racers/racer13.png")]

tracksToChoose = [pygame.image.load("sprites/tracks/track01.png"),pygame.image.load("sprites/tracks/track02.png")]

#fakeStreet = pygame.Rect(0, 574, 1678, 214)

# Colors
white, black, red, green, blue, yellow, magenta, cyan, gray, light_gray, dark_gray, orange, purple, pink, brown, olive = (
    (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 128, 128), (200, 200, 200),
    (64, 64, 64), (255, 165, 0), (128, 0, 128), (255, 182, 193), (165, 42, 42), (128, 128, 0))


starting_screen = True
gameIsRunning = True


# ---Funktions

def imoprt_track():
    global track, road, offroad, startingLine, startingBox, checkPoints, track_center_x, track_center_y
    track = pygame.transform.scale(pygame.image.load("sprites/tracks/track02.png"), screenSize)
    road = (120, 120, 120, 255)
    offroad = (0, 120, 0, 255)

    track_center_x = screen_width // 2 - track.get_width() // 2
    track_center_y = screen_height // 2 - track.get_height() // 2

    startingLine = (567 + track_center_x, 80 + track_center_y)
    startingBox = pygame.Rect(566 + track_center_x, 51 + track_center_y, 2, 106)

    checkPoints = []
    checkPoints.append(pygame.Rect(600 + track_center_x, 740 + track_center_y, 2, 370))

global track, road, offroad, startingLine, startingBox, checkPoints, track_center_x, track_center_y

# Inputs

def racer1_handle_input(racer1, keys):
    if keys[pygame.K_w] and racer1.speed < racer1.max_acc_speed_speed:
        racer1.acc = True
        racer1.speed += racer1.acceleration
    elif racer1.speed > 0:
        racer1.speed -= racer1.resistance
    if keys[pygame.K_a]:
        racer1.direction += 2
    if keys[pygame.K_s] and racer1.speed > -100:
        racer1.acc = True
        racer1.speed -= racer1.brake
    elif racer1.speed < 0:
        racer1.speed += racer1.resistance
    if keys[pygame.K_d]:
        racer1.direction -= 2
    racer1.move()

def racer2_handle_input(racer2, keys):
    if keys[pygame.K_UP] and racer2.speed < racer2.max_acc_speed_speed:
        racer2.acc = True
        racer2.speed += racer2.acceleration
    elif racer2.speed > 0:
        racer2.speed -= racer2.resistance
    if keys[pygame.K_LEFT]:
        racer2.direction += 2
    if keys[pygame.K_DOWN] and racer2.speed > -100:
        racer2.acc = True
        racer2.speed -= racer2.brake
    elif racer2.speed < 0:
        racer2.speed += racer2.resistance
    if keys[pygame.K_RIGHT]:
        racer2.direction -= 2
    racer2.move()



# Debugging

def debug(screen, debug, font, racer1, racer2, keys):
    if keys[pygame.K_F1]:
        debug = not debug
    if debug:
        debug_text = f"Racer1 Speed: {racer1.speed:.0f}"
        debug_surface = font.render(debug_text, True, (255, 0, 0))
        screen.blit(debug_surface, (10, 10))

        debug_text = f"Racer2 Speed: {racer2.speed:.0f}"
        debug_surface = font.render(debug_text, True, (255, 0, 0))
        screen.blit(debug_surface, (10, 30))

        debug_text = f"Drift R1: {racer1.drift}"
        debug_surface = font.render(debug_text, True, (255, 0, 0))
        screen.blit(debug_surface, (10, 50))
        debug_text = f"Drift R2: {racer2.drift}"
        debug_surface = font.render(debug_text, True, (255, 0, 0))
        screen.blit(debug_surface, (10, 70))

        debug_text = f"Lap R1: {racer1.lap}"
        debug_surface = font.render(debug_text, True, (255, 0, 0))
        screen.blit(debug_surface, (10, 110))
        debug_text = f"Lap R2: {racer2.lap}"
        debug_surface = font.render(debug_text, True, (255, 0, 0))
        screen.blit(debug_surface, (10, 130))



def spawn_fake_racers():
    global fakeRacer1,fakeRacer2
    fakeRacer1 = FakeRacer(-50, 630, pygame.transform.scale(pygame.image.load("sprites/racers/racer11.png"), (15,30)))
    fakeRacer2 = FakeRacer(-50, 700, pygame.transform.scale(pygame.image.load("sprites/racers/racer13.png"), (15,30)))

def move_fake_racers():
    fakeRacer1.move(random.randrange(50,200,10))
    fakeRacer2.move(random.randrange(50,200,10))

def draw_fields(fields):
    for e in fields:
        pygame.draw.rect(Menue_surf, gray, e.rect, 100)
        Menue_surf.blit(e.gfx, (e.x - e.gfx.get_width(), e.y - e.gfx.get_height()))


# Add racers as fields to a 4 by 3 matrix
        
def add_racer_fields():
    global fields, racersToChoose
    fields.clear()
    column_count = 4
    row_count = 3

    zone_x = screen_width // (column_count + 1)
    zone_y = screen_height // (row_count + 1)
    zone_width = screen_width - screen_width // (column_count + 1)
    zone_height = screen_height - screen_height // (row_count + 1)

    column_width = zone_width // column_count
    row_height = zone_height // row_count

    for row in range(row_count):
        for column in range(column_count):
            index = row * column_count + column
            if index < len(racersToChoose):
                racer_gfx = racersToChoose[index]
                racerToChoose = Field(zone_x + column * column_width - racer_gfx.get_width() // 2, zone_y + row * row_height - racer_gfx.get_height() // 2, pygame.transform.scale(racer_gfx, (20,40)))
                fields.append(racerToChoose)



# Add tracks as fields to a 4 by 3 matrix
                
def add_track_fields():
    global fields, tracksToChoose
    fields.clear()
    column_count = 4
    row_count = 3

    zone_x = screen_width // (column_count + 1)
    zone_y = screen_height // (row_count + 1)
    zone_width = screen_width - screen_width // (column_count + 1)
    zone_height = screen_height - screen_height // (row_count + 1)

    column_width = zone_width // column_count
    row_height = zone_height // row_count

    for row in range(row_count):
        for column in range(column_count):
            index = row * column_count + column
            if index < len(tracksToChoose):
                track_gfx = tracksToChoose[index]
                trackToChoose = Field(zone_x + column * column_width - track_gfx.get_width() // 2, zone_y + row * row_height - track_gfx.get_height() // 2, pygame.transform.scale(track_gfx, (20,40)))
                fields.append(trackToChoose)


# Gameloops
    
def starting_screen(): 
    starting_screen = True
    background = pygame.transform.scale(pygame.image.load("sprites/menue/starting_screen.png"), screenSize)
    spawn_fake_racers()
    
    while starting_screen:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    starting_screen = False
                    menue_player_select()

        Menue_surf.blit(background, (0,0))

        move_fake_racers()

        screen.blit(Menue_surf, (0,0))
        pygame.display.flip()
        clock.tick(120)



def menue_player_select():
    menue_p = True
    background = pygame.image.load("sprites/menue/pselect.png")
    add_racer_fields()

    while menue_p:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menue_p = False
                    starting_screen()
                else:
                    menue_p = False
                    menue_track_select()

        Menue_surf.blit(background, (0,0))
        draw_fields(fields)

        screen.blit(Menue_surf, (0,0))
        pygame.display.flip()
        clock.tick(120)



def menue_track_select():
    menue_t = True
    background = pygame.image.load("sprites/menue/tselect.png")
    add_track_fields()

    while menue_t:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menue_t = False
                    menue_player_select()
                else:
                    menue_t = False
                    race()

        Menue_surf.blit(background, (0,0))
        draw_fields(fields)

        screen.blit(Menue_surf, (0,0))
        pygame.display.flip()
        clock.tick(120)



def race():
    global delta_time, racer1, racer2
    race_is_running = True
    imoprt_track()
    



# ---Classes
        
class FakeRacer:
    def __init__(self, x, y, gfx):
        self.x = x
        self.y = y
        self.gfx = gfx
        self.sped = []

    def move(self, speed):
        self.sped.append(speed)
        self.x += self.sped[0] * 0.1
        self.draw()

    def draw(self):
        Menue_surf.blit(pygame.transform.rotate(self.gfx, -90), (self.x, self.y))



class Racer:
    def __init__(self, x, y, gfx, direction):
        self.x = x
        self.y = y
        self.gfx = pygame.image.load(gfx)
        self.direction = direction

#        self.mass = self.gfx.get_width() * self.gfx.get_height()
        self.size = (self.gfx.get_width() + self.gfx.get_height()) / 4
        self.body = pygame.Rect(self.x - self.size, self.y - self.size, self.size, self.size)

        self.speed_Vec = pygame.math.Vector2()
        self.speed = self.speed_Vec.length
        self.max_acc_speed = 500
        self.resistance = 3
        self.acceleration = 3
        self.acc = False
        self.brake = 10

        self.lap = 1
        self.checks = []

    def update_n_draw(self):
        rotated_gfx = pygame.transform.rotate(self.gfx, self.direction)
        Racer_surf.blit(rotated_gfx, (self.x, self.y))
        #self.body = pygame.Rect(self.x - self.size, self.y - self.size, self.size, self.size)
        self.body.update()
        self.speed_Vec.update()

        if self.body.colliderect(checkPoints):
            self.checks.append(1)
        if self.body.colliderect(startingBox) and self.checks:
            self.lap += 1
            self.checks.clear()

    def handle_Collision(self):
        if self.body.colliderect(startingBox):
            if self.speed_Vec.x < 0:
                self.speed_Vec.x = -self.speed_Vec.x
            else:
                pass
        pass

    def move(self):
        ground = Track_surf.get_at((self.x, self.y))
        if ground != road:
            self.speed *= 0.97  # Reduce speed on offroad
            

        self.x += self.speed_Vec.x
        self.handle_Collision()
        self.y += self.speed_Vec.y
        self.handle_Collision()

        if self.speed > -5 and self.speed < 5 and not self.acc:
            self.speed = 0

            self.y = min(max(self.y, track_center_y), screen_height // 2 + track.get_height() // 2 - self.gfx.get_height())
            self.x = min(max(self.x, track_center_x), screen_width // 2 + track.get_width() // 2 - self.gfx.get_width())


class Field:
    def __init__(self, x, y, gfx):
        self.x = x
        self.y = y
        self.gfx = gfx
        self.rect = pygame.Rect(self.x - self.gfx.get_width() // 2 - 35, self.y - self.gfx.get_height() // 2 - 35, 70, 70)

starting_screen()

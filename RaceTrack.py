import pygame
import math
import random
pygame.init()
pygame.display.set_caption("RaceTrack")

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

# Colors
white, black, red, green, blue, yellow, magenta, cyan, gray, light_gray, dark_gray, orange, purple, pink, brown, olive = (
    (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 128, 128), (200, 200, 200),
    (64, 64, 64), (255, 165, 0), (128, 0, 128), (255, 182, 193), (165, 42, 42), (128, 128, 0))




# ---Funktions

def imoprt_track():
    global track, road, offroad, startingLine, startingBox, checkPoint1, track_center_x, track_center_y
    track = pygame.image.load("sprites/tracks/track02.png")
    road = (120, 120, 120, 255)
    offroad = (0, 120, 0, 255)

    track_center_x = screen_width // 2 - track.get_width() // 2
    track_center_y = screen_height // 2 - track.get_height() // 2

    startingLine = (567 + track_center_x, 80 + track_center_y)
    startingBox = pygame.Rect(566 + track_center_x, 51 + track_center_y, 2, 106)

    checkPoints = []
    checkPoints.append(pygame.Rect(600 + track_center_x, 740 + track_center_y, 2, 370))



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

def debug(screen, debug_mode, font, racer1, racer2, keys):
    if keys[pygame.K_F1]:
        debug_mode = not debug_mode
    if debug_mode:
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




# ---Classes
        
class FakeRacer:
    def __init__(self, x, y, gfx):
        self.x = x
        self.y = y
        self.gfx = gfx

    def move(self, speed):
        self.x += speed

    def draw(self):
        Menue_surf.blit(pygame.transform.rotate(self.gfx, 90), (self.x, self.y))



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

        if self.body.colliderect(checkpoints):
            self.check1 = True
        if self.body.colliderect(startingBox) and self.check1:
            self.lap += 1
            self.check1 = False

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

        self.y = min(self.max_acc_speed(self.y, track_center_y), screen_height // 2 + track.get_height() // 2 - self.gfx.get_height())
        self.x = min(self.max_acc_speed(self.x, track_center_x), screen_width // 2 + track.get_width() // 2 - self.gfx.get_width())
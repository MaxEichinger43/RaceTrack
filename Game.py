import sys
import math
import pygame
pygame.init()

debug_mode = True
font = pygame.font.Font(None, 24)

# Preparing screen
screen_width = 1680
screen_height = 1050
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("RaceTrack")

# Creating surfaces
Track_surface = pygame.Surface((screen_width, screen_height))
Racer_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

# Track Graphics loading
track = pygame.image.load("sprites/tracks/track01.png")

class Racer:
    def __init__(self, x, y, gfx):
        self.x = x
        self.y = y
        self.gfx = pygame.image.load(gfx)
        self.speed = 0
        self.dir = 0
        self.mass = self.gfx.get_width() * self.gfx.get_height()
        self.body = pygame.Rect(self.x, self.y, self.gfx.get_width(), self.gfx.get_height())
        #self.max_speed = self.mass

    def update_n_draw(self):
        self.body.x = self.x
        self.body.y = self.y
        rotated_gfx = pygame.transform.rotate(self.gfx, self.dir)
        rotated_body = rotated_gfx.get_rect(center=self.body.center)
        Racer_surface.blit(rotated_gfx, rotated_body)

    def move(self):
        self.x -= self.speed * math.sin(math.radians(self.dir)) * delta_time
        self.y -= self.speed * math.cos(math.radians(self.dir)) * delta_time

        self.y = min(max(self.y, screen_height // 2 - track.get_height() // 2), screen_height // 2 + track.get_height() // 2)
        self.x = min(max(self.x, screen_width // 2 - track.get_width() // 2), screen_width // 2 + track.get_width() // 2)

# Create racer instances
racer1 = Racer(screen_width // 2, screen_height // 2, "sprites/racers/racer01.png")
racer2 = Racer(screen_width // 2, screen_height // 2, "sprites/racers/racer02.png")

# Constants
acceleration = 10
friction = 3
brake = 20

# Creating clock
clock = pygame.time.Clock()

# Gameloop
RaceIsRunning = True
while RaceIsRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    delta_time = clock.tick(120) / 1000.0

    # Input system
    keys = pygame.key.get_pressed()

    # Racer1
    if keys[pygame.K_w] and racer1.speed < 400:
        racer1.speed += acceleration
    elif racer1.speed > 0:
        racer1.speed -= friction
    if keys[pygame.K_a]:
        racer1.dir += 2
    if keys[pygame.K_s] and racer1.speed > -100:
        racer1.speed -= brake
    if keys[pygame.K_d]:
        racer1.dir -= 2

    # Racer2
    if keys[pygame.K_UP] and racer2.speed < 400:
        racer2.speed += acceleration
    elif racer2.speed > 0:
        racer2.speed -= friction
    if keys[pygame.K_LEFT]:
        racer2.dir += 2
    if keys[pygame.K_DOWN] and racer2.speed > -100:
        racer2.speed -= brake
    if keys[pygame.K_RIGHT]:
        racer2.dir -= 2

    # Debug mode
    if keys[pygame.K_F1]:
        debug_mode = not debug_mode

    racer1.move()
    racer2.move()

    if debug_mode:
        debug_text = f"Racer1 Speed: {racer1.speed:.2f}, Position: ({racer1.x:.2f}, {racer1.y:.2f}), Keys pressed: {keys}"
        debug_surface = font.render(debug_text, True, (255, 0, 0))
        screen.blit(debug_surface, (10, 10))

    # Drawing the track and the clear racer surface
    Track_surface.fill((255, 255, 255))
    Track_surface.blit(track, (screen_width // 2 - track.get_width() // 2, screen_height // 2 - track.get_height() // 2))
    Racer_surface.fill((0, 0, 0, 0))

    racer1.update_n_draw()
    racer2.update_n_draw()

    # Blit the Track_surface and Racer_surface onto the screen
    screen.blit(Track_surface, (0, 0))
    screen.blit(Racer_surface, (0, 0))

    pygame.display.flip()
    pygame.display.update()
    clock.tick(120)

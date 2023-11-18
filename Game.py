from os import DirEntry
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
track = pygame.image.load("sprites/tracks/track02.png")
road = (120, 120, 120, 255)
offroad = (0, 120, 0, 255)
startingLine = (567 + screen_width // 2 - track.get_width() // 2, 80 + screen_height // 2 - track.get_height() // 2)

delta_time = 120//1000

class Racer:
    def __init__(self, x, y, gfx, direction):
        self.x = x
        self.y = y
        self.gfx = pygame.image.load(gfx)
        self.direction = direction
        self.speed = 0
        self.speed_x = self.speed * math.sin(math.radians(self.direction)) * delta_time
        self.speed_y = self.speed * math.cos(math.radians(self.direction)) * delta_time
        self.mass = self.gfx.get_width() * self.gfx.get_height()
        self.body = pygame.Rect(self.x, self.y, self.gfx.get_width(), self.gfx.get_height())
        self.max_speed = self.mass + 300
        self.resistance = 3
        self.ground_friction = self.mass * self.max_speed * 0.7
        self.drift = False
        self.acceleration = 3
        self.brake = 10

    def update_n_draw(self):
        self.body.x = self.x
        self.body.y = self.y
        rotated_gfx = pygame.transform.rotate(self.gfx, self.direction)
        rotated_body = rotated_gfx.get_rect(center=self.body.center)
        Racer_surface.blit(rotated_gfx, rotated_body)

    def move(self):
        ground = Track_surface.get_at((int(self.x + self.gfx.get_width() // 2), int(self.y + self.gfx.get_height() // 2)))
        if ground == road:
            self.speed = min(self.speed, self.max_speed)  # Limit speed on road
        elif ground == offroad:
            self.speed *= 0.97  # Reduce speed on offroad

        dermarkusdifference = abs(math.degrees(math.sin(self.direction)) - math.degrees(math.atan2(self.speed * math.sin(math.radians(self.direction)), self.speed * math.cos(math.radians(self.direction)))))
        if dermarkusdifference > 5:
            self.drift = True
        else:
            self.drift = False

        if not self.drift:
            self.x -= self.speed_x
            self.y -= self.speed_y
        else:
            self.x -= self.speed * math.sin(math.radians(self.direction)) * delta_time   # Reduce drift effect
            self.y -= self.speed * math.cos(math.radians(self.direction)) * delta_time 

        self.y = min(max(self.y, screen_height // 2 - track.get_height() // 2), screen_height // 2 + track.get_height() // 2)
        self.x = min(max(self.x, screen_width // 2 - track.get_width() // 2), screen_width // 2 + track.get_width() // 2)

# Create racer instances
racer1 = Racer(startingLine[0], startingLine[1], "sprites/racers/racer03(dermark)us.png", 90)
racer2 = Racer(screen_width // 2, screen_height // 2, "sprites/racers/racer02.png", 90)


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
    if keys[pygame.K_w] and racer1.speed < racer1.max_speed:
        racer1.speed += racer1.acceleration
    elif racer1.speed > 0:
        racer1.speed -= racer1.resistance
    if keys[pygame.K_a]:
        racer1.direction += 2
    if keys[pygame.K_s] and racer1.speed > -100:
        racer1.speed -= racer1.brake
    elif racer1.speed < 0:
        racer1.speed += racer1.resistance
    if keys[pygame.K_d]:
        racer1.direction -= 2

    # Racer2
    if keys[pygame.K_UP] and racer2.speed < racer2.max_speed:
        racer2.speed += racer2.acceleration
    elif racer2.speed > 0:
        racer2.speed -= racer2.resistance
    if keys[pygame.K_LEFT]:
        racer2.direction += 2
    if keys[pygame.K_DOWN] and racer2.speed > -100:
        racer2.speed -= racer2.brake
    elif racer2.speed < 0:
        racer2.speed += racer2.resistance
    if keys[pygame.K_RIGHT]:
        racer2.direction -= 2

    # Debug mode
    if keys[pygame.K_F1]:
        debug_mode = not debug_mode

    racer1.move()


    racer2.move()

    # Drawing the track and the clear racer surface
    Track_surface.fill((255, 255, 255))
    Track_surface.blit(track, (screen_width // 2 - track.get_width() // 2, screen_height // 2 - track.get_height() // 2))
    Racer_surface.fill((0, 0, 0, 0))

    racer1.update_n_draw()
    racer2.update_n_draw()

    # Blit the Track_surface and Racer_surface onto the screen
    screen.blit(Track_surface, (0, 0))
    screen.blit(Racer_surface, (0, 0))

    if debug_mode:
        debug_text1 = f"Racer1 Speed: {racer1.speed:.2f}"
        debug_surface = font.render(debug_text1, True, (255, 0, 0))
        screen.blit(debug_surface, (10, 10))

        debug_text2 = f"Racer2 Speed: {racer2.speed:.2f}"
        debug_surface = font.render(debug_text2, True, (255, 0, 0))
        screen.blit(debug_surface, (10, 30))

        debug_text3 = f"Drift R1: {racer1.drift}"
        debug_surface = font.render(debug_text3, True, (255, 0, 0))
        screen.blit(debug_surface, (10, 50))
        debug_text4 = f"Drift R2: {racer2.drift}"
        debug_surface = font.render(debug_text4, True, (255, 0, 0))
        screen.blit(debug_surface, (10, 70))


    pygame.display.flip()
    pygame.display.update()
    clock.tick(120)

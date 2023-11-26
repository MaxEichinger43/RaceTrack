import sys
import math
import pygame
pygame.init()


# Preparing screen
screen_width = 1680
screen_height = 1050
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("RaceTrack")

# Creating surfaces
Track_surface = pygame.Surface((screen_width, screen_height))
Racer_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)


debug_mode = True
font = pygame.font.Font(None, 24)
delta_time = 120//1000
clock = pygame.time.Clock()





# Import track n stuff
def import_track():
    global track, road, offroad, startingLine, startingBox, checkPoint1, track_center_x, track_center_y
    track = pygame.image.load("sprites/tracks/track02.png")
    road = (120, 120, 120, 255)
    offroad = (0, 120, 0, 255)

    track_center_x = screen_width // 2 - track.get_width() // 2
    track_center_y = screen_height // 2 - track.get_height() // 2

    startingLine = (567 + track_center_x, 80 + track_center_y)
    startingBox = pygame.Rect(566 + track_center_x, 51 + track_center_y, 2, 106)

    checkPoint1 = pygame.Rect(600 + track_center_x, 740 + track_center_y, 2, 370)
import_track()




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
        self.max_speed = 500
        self.resistance = 3
        self.ground_friction = self.mass * self.max_speed * 0.7
        self.drift = False
        self.acceleration = 3
        self.acc = False
        self.brake = 10
        self.lap = 1
        self.check1 = False

    def update_n_draw(self):
        self.body.x = self.x
        self.body.y = self.y
        rotated_gfx = pygame.transform.rotate(self.gfx, self.direction)
        rotated_body = rotated_gfx.get_rect(center=self.body.center)
        Racer_surface.blit(rotated_gfx, rotated_body)

        self.speed_x = self.speed * math.sin(math.radians(self.direction)) * delta_time
        self.speed_y = self.speed * math.cos(math.radians(self.direction)) * delta_time

        if self.body.colliderect(checkPoint1):
            self.check1 = True
        if self.body.colliderect(startingBox) and self.check1:
            self.lap += 1
            self.check1 = False

    def handle_Collision(self):
        if self.body.colliderect(startingBox):
            if self.speed_x < 0:
                self.speed_x = -self.speed_x
            else:
                pass
        pass

    def move(self):
        ground = Track_surface.get_at((int(self.x + self.gfx.get_width() // 2), int(self.y + self.gfx.get_height() // 2)))
        if ground == road:
            self.speed = self.speed
        elif ground == offroad:
            self.speed *= 0.97  # Reduce speed on offroad

        self.x -= self.speed_x
        self.handle_Collision()
        self.y -= self.speed_y
        self.handle_Collision()

        if self.speed > -5 and self.speed < 5 and not self.acc:
            self.speed = 0

        self.y = min(max(self.y, track_center_y), screen_height // 2 + track.get_height() // 2 - self.gfx.get_height())
        self.x = min(max(self.x, track_center_x), screen_width // 2 + track.get_width() // 2 - self.gfx.get_width())


# Create racer instances
racer1 = Racer(startingLine[0], startingLine[1], "sprites/racers/racer03(dermark)us.png", 90)
racer2 = Racer(startingLine[0], startingLine[1], "sprites/racers/racer02.png", 90)





def racer1_handle_input(racer1, keys):
    if keys[pygame.K_w] and racer1.speed < racer1.max_speed:
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
    if keys[pygame.K_UP] and racer2.speed < racer2.max_speed:
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
    racer1_handle_input(racer1, keys)
    racer2_handle_input(racer2, keys)

    # Drawing the track and the clear racer surface
    Track_surface.fill((255, 255, 255))
    Track_surface.blit(track, (track_center_x, track_center_y))
    Racer_surface.fill((0, 0, 0, 0))

    racer1.update_n_draw()
    racer2.update_n_draw()

    # Blit the Track_surface and Racer_surface onto the screen
    screen.blit(Track_surface, (0, 0))
    screen.blit(Racer_surface, (0, 0))

    debug(screen, debug_mode, font, racer1, racer2, keys)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(120)
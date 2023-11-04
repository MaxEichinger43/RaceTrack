import sys
import math
import pygame
pygame.init()

#Defining Vektor
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_rotation(self):
        if self.y == 0:
            if self.x > 0:
                return 90
            elif self.x < 0:
                return -90
            else:
                return 0
        else:
            angle = math.degrees(math.atan(self.x / self.y))
            if self.y < 0:
                angle += 180
            return angle



#Preparing screen
screen_width = 1680
screen_height = 1050
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("RaceTrack")

#Creating surfaces
Track_surface = pygame.Surface((screen_width,screen_height))
Racer_surface = pygame.Surface((screen_width,screen_height), pygame.SRCALPHA)



#Track Graphics loading
track = pygame.image.load("Tracks/Track01.png")

#Racers Graphics loading
racer1_gfx = pygame.image.load("Racers/racer01.png")
racer2_gfx = pygame.image.load("Racers/racer01.png")
white = (255, 255, 255)




#Creating racer class
class Racer:
    def __init__(self, x, y, gfx):
        self.x = x
        self.y = y
        self.gfx = pygame.image.load(gfx)

    def mass(self):
        self.mass = racer1_gfx.get_width() * racer1_gfx.get_height()

    def draw(self):
        Racer_surface.blit(self.gfx, (self.x, self.y))

    def body(self):
        pygame.Rect(self.x, self.y, self.gfx.get_width(), self.gfx.get_height())

    def speed(self):
        Vector(0, 0)

    def acceleration(self):
        5 * self.mass

    def deceleration(self):
        30 * self.mass

    def Turning(self):
        20 * self.mass





#racer1 = pygame.Rect(screen_width // 2, screen_height // 2, racer1_gfx.get_width(), racer1_gfx.get_height())
#racer2 = pygame.Rect(screen_width // 2, screen_height // 2, racer2_gfx.get_width(), racer2_gfx.get_height())



#Racers
racer1 = Racer(screen_width // 2, screen_height // 2, "Racers/racer01.png")
racer2 = Racer(screen_width // 2, screen_height // 2, "Racers/racer02.png")






#Creating clock
clock = pygame.time.Clock()

#-------------------------------------------------------------------------------Gameloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    time = clock.tick(120) / 1000.0


    #Calculate the rotation of the racers based on the x and y components  
    rotRacer1 = racer1.speed.get_rotation()
    rotRacer2 = racer2.speed.get_rotation()


    # Input system
    keys = pygame.key.get_pressed()

    # Racer1
    if keys[pygame.K_w]:
        racer1.speed.y -= 10
        racer1.speed.x -= racer1.speed.x * 0.01
    if keys[pygame.K_a]:
        racer1.speed.x -= 10
        racer1.speed.y -= racer1.speed.y * 0.01
    if keys[pygame.K_s]:
        racer1.speed.y += 10
        racer1.speed.x -= racer1.speed.x * 0.01
    if keys[pygame.K_d]:
        racer1.speed.x += 10
        racer1.speed.y -= racer1.speed.y * 0.01

    # Racer2
    if keys[pygame.K_UP]:
        racer2.speed.y -= 10
    if keys[pygame.K_LEFT]:
        racer2.speed.x -= 10
    if keys[pygame.K_DOWN]:
        racer2.speed.y += 10
    if keys[pygame.K_RIGHT]:
        racer2.speed.x += 10

    # ...

    racer1.y += racer1.speed.y * time
    racer1.x += racer1.speed.x * time

    # ...

    racer2.y += racer2.speed.y * time
    racer2.x += racer2.speed.x * time
    #.........................................



    #Drawing the track and the clear racer surface
    Track_surface.fill((255,255,255))
    Track_surface.blit(track, (screen_width // 2 - track.get_width // 2,screen_height // 2 - track.get_height // 2))
    Racer_surface.fill((0, 0, 0, 0))


# Blit the racers on the racer surface based on their center points
    racer1_gfx_rotated = pygame.transform.rotate(racer1_gfx, rotRacer1)
    racer2_gfx_rotated = pygame.transform.rotate(racer2_gfx, rotRacer2)
    Racer_surface.blit(racer1_gfx_rotated, racer1.center)
    Racer_surface.blit(racer2_gfx_rotated, racer2.center)


    # Blit the Track_surface and Racer_surface onto the screen
    screen.blit(Track_surface, (0, 0))
    screen.blit(Racer_surface, (0, 0))

    pygame.display.flip()
    clock.tick(120)
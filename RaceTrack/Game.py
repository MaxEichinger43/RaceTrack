import math
import sys
import pygame
pygame.init()

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

#Creating racers as objects
racer1 = pygame.Rect(screen_width // 2, screen_height // 2, racer1_gfx.get_width(), racer1_gfx.get_height())
racer2 = pygame.Rect(screen_width // 2, screen_height // 2, racer2_gfx.get_width(), racer2_gfx.get_height())

#Racerspeed
def_speed = 0

racer1_speed_y = def_speed
racer1_speed_x = def_speed

racer2_speed_y = def_speed
racer2_speed_x = def_speed


#Creating clock
clock = pygame.time.Clock()

#-------------------------------------------------------------------------------Gameloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    time = clock.tick(120) / 1000.0


#Input system...........................
    keys = pygame.key.get_pressed()

#Racer1
    if keys[pygame.K_w]:
        racer1_speed_y -= 10
        racer1_speed_x -= racer1_speed_x * 0.01
    if keys[pygame.K_a]:
        racer1_speed_x -= 10
        racer1_speed_y -= racer1_speed_y * 0.01
    if keys[pygame.K_s]:
        racer1_speed_y += 10
        racer1_speed_x -= racer1_speed_x * 0.01
    if keys[pygame.K_d]:
        racer1_speed_x += 10
        racer1_speed_y -= racer1_speed_y * 0.01

#Racer2
    if keys[pygame.K_UP]:
        racer2_speed_y -= 10
    if keys[pygame.K_LEFT]:
        racer2_speed_x -= 10
    if keys[pygame.K_DOWN]:
        racer2_speed_y += 10
    if keys[pygame.K_RIGHT]:
        racer2_speed_x += 10


    racer1.y += racer1_speed_y * time
    racer1.x += racer1_speed_x * time
    racet1_dir = math.degrees(math.atan2(racer1_speed_y, racer1_speed_x)) + 90


    racer2.y += racer2_speed_y * time
    racer2.x += racer2_speed_x * time
    
    #Make sure the racers dont drive to ikea while racing
    racer1.y = min(max(racer1.y, screen_height // 2 - 500), screen_height // 2 + 500)
    racer1.x = min(max(racer1.x, screen_width // 2 - 500), screen_width // 2 + 500)

    racer2.y = min(max(racer2.y, screen_height // 2 - 500), screen_height // 2 + 500)
    racer2.x = min(max(racer2.x, screen_width // 2 - 500), screen_width // 2 + 500)
    #.........................................



    #Drawing the track and the clear racer surface
    Track_surface.fill((255,255,255))
    Track_surface.blit(track, (screen_width // 2 - 500,screen_height // 2 - 500))
    Racer_surface.fill((0, 0, 0, 0))


# Blit the racers on the racer surface based on their center points
    racer1_gfx_rotated = pygame.transform.rotate(racer1_gfx, racet1_dir)
    Racer_surface.blit(racer1_gfx_rotated, racer1.center)
    Racer_surface.blit(racer2_gfx, racer2.center)


    # Blit the Track_surface and Racer_surface onto the screen
    screen.blit(Track_surface, (0, 0))
    screen.blit(Racer_surface, (0, 0))

    pygame.display.flip()
    clock.tick(120)
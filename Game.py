import sys
import math
from numpy import arctan
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
track = pygame.image.load("sprites/tracks/track01.png")

class Racer:
    def __init__ (self, x, y, gfx):
        self.x = x
        self.y = y
        self.gfx = pygame.image.load(gfx)
        self.speed = 0
        self.dir = 0
        self.mass = self.gfx.get_width() * self.gfx.get_height()
        self.body = pygame.Rect(self.x, self.y, self.gfx.get_width(), self.gfx.get_height())

    def update_n_draw(self):
        self.body.x = self.x
        self.body.y = self.y
        rotated_gfx = pygame.transform.rotate(self.gfx, self.dir)
        rotated_body = rotated_gfx.get_rect(center=self.body.center)
        Racer_surface.blit(rotated_gfx, rotated_body)



racer1 = Racer(screen_width // 2, screen_height // 2, "sprites/racers/racer01.png")
racer2 = Racer(screen_width // 2, screen_height // 2, "sprites/racers/racer02.png")



#Creating clock
clock = pygame.time.Clock()

#-------------------------------------------------------------------------------Gameloop
RaceIsRunning = True
while RaceIsRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    time = clock.tick(120) / 1000.0


#Input system...........................
    
    keys = pygame.key.get_pressed()

#Racer1
#    if keys[pygame.K_w]:
#
#    if keys[pygame.K_a]:
#
#    if keys[pygame.K_s]:
#
#    if keys[pygame.K_d]:


#Racer2
#    if keys[pygame.K_UP]:
#        
#    if keys[pygame.K_LEFT]:
#        
#    if keys[pygame.K_DOWN]:
#        
#    if keys[pygame.K_RIGHT]:
#        

    
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

    racer1.update_n_draw()
    racer2.update_n_draw()

    # Blit the Track_surface and Racer_surface onto the screen
    screen.blit(Track_surface, (0, 0))
    screen.blit(Racer_surface, (0, 0))
    pygame.display.flip()
    clock.tick(120)
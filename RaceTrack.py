import pygame
import random
pygame.init()
pygame.display.set_caption("RaceTrack")

# -------General
screen_width = 1680
screen_height = 1050
screenSize = screen_width, screen_height
screen = pygame.display.set_mode((screenSize),0,0,0,1)

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

tracksToChoose = [pygame.image.load("sprites/tracks/track01.png"), pygame.image.load("sprites/tracks/track02.png")]

#fakeStreet = pygame.Rect(0, 574, 1678, 214)

# Colors
white, black, red, green, blue, yellow, magenta, cyan, gray, light_gray, dark_gray, orange, purple, pink, brown, olive = (
    (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 128, 128), (200, 200, 200),
    (64, 64, 64), (255, 165, 0), (128, 0, 128), (255, 182, 193), (165, 42, 42), (128, 128, 0))


starting_screen = True



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
        self.gfx = gfx
        self.direction = direction

#        self.mass = self.gfx.get_width() * self.gfx.get_height()
        self.size = (self.gfx.get_width() + self.gfx.get_height()) / 4
        #self.body = pygame.Rect(self.x - self.size, self.y - self.size, self.size, self.size)

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
        #self.body.update()
        self.speed_Vec.update()
#TODO
        #if self.body.colliderect(checkPoints):
        #    self.checks.append(1)
        #if self.body.colliderect(startingBox) and self.checks:
        #    self.lap += 1
        #    self.checks.clear()

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
        self.rect1 = pygame.Rect(self.x - self.gfx.get_width() // 2 - 40, self.y - self.gfx.get_height() // 2 - 40, 80, 80)
        self.rect2 = pygame.Rect(self.x - self.gfx.get_width() // 2 - 45, self.y - self.gfx.get_height() // 2 - 45, 90, 90)




# ---Funktions

def import_track(chosen_track):
    global track, road, offroad, rand_start_point, startingBox, checkPoints, track_center_x, track_center_y, importing
    importing = True

    track = pygame.transform.scale(chosen_track, (chosen_track.get_width(), chosen_track.get_height()))
    track_center_x = screen_width // 2 - track.get_width() // 2
    track_center_y = screen_height // 2 - track.get_height() // 2

    road = (120, 120, 120, 255)
    offroad = (0, 120, 0, 255)
    start = (0, 0, 0, 255)
    fin = (255, 255, 255, 255)
    start_pixels = []
    fin_pixels = []
    
        


    rand_start_point = start_pixels[random.randrange(0, len(start_pixels))]
    startingBox = pygame.Rect(566 + track_center_x, 51 + track_center_y, 2, 106)

    checkPoints = []
    checkPoints.append(pygame.Rect(600 + track_center_x, 740 + track_center_y, 2, 370))
    importing = False

global track, road, offroad, rand_start_point, startingBox, checkPoints, track_center_x, track_center_y


# Input handeling

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



# Draw all fields

def draw_fields(fields):
    for e in fields:
        pygame.draw.rect(Menue_surf, gray, e.rect, 100)
        Menue_surf.blit(e.gfx, (e.x - e.gfx.get_width(), e.y - e.gfx.get_height()))



# Add racers as fields to a 4 by 3 matrix
        
def add_racer_fields():
    global fields, racersToChoose
    fields.clear()
    columns = 4
    rows = 3

    zone_x = screen_width // (columns + 1)
    zone_y = screen_height // (rows + 1)
    zone_width = screen_width - screen_width // (columns + 1)
    zone_height = screen_height - screen_height // (rows + 1)

    column_width = zone_width // columns
    row_height = zone_height // rows

    for row in range(rows):
        for column in range(columns):
            index = row * columns + column
            if index < len(racersToChoose):
                racer_gfx = racersToChoose[index]
                racerToChoose = Field(zone_x + column * column_width - racer_gfx.get_width() // 2, zone_y + row * row_height - racer_gfx.get_height() // 2, pygame.transform.scale(racer_gfx, (20,40)))
                fields.append(racerToChoose)



# Add tracks as fields to a 4 by 3 matrix
                
def add_track_fields():
    global fields, tracksToChoose
    fields.clear()
    columns = 4
    rows = 3

    zone_x = screen_width // (columns + 1)
    zone_y = screen_height // (rows + 1)
    zone_width = screen_width - screen_width // (columns + 1)
    zone_height = screen_height - screen_height // (rows + 1)

    column_width = zone_width // columns
    row_height = zone_height // rows

    for row in range(rows):
        for column in range(columns):
            index = row * columns + column
            if index < len(tracksToChoose):
                track_gfx = pygame.transform.scale(tracksToChoose[index],(40,40))
                trackToChoose = Field(zone_x + column * column_width - track_gfx.get_width() // 2, zone_y + row * row_height - track_gfx.get_height() // 2, track_gfx)
                fields.append(trackToChoose)



def handle_selection(menue_p, menue_t):
    global p1_chose, p2_chose, racer1, racer2, fields, selected_field_p1, selected_field_p2

    keys = pygame.key.get_pressed()

# Player 1
    if keys[pygame.K_w]:
        p1_chose = True
    if keys[pygame.K_a] and not p1_chose:
        selected_field_p1 -= 1
    if keys[pygame.K_s]:
        p1_chose = False
    if keys[pygame.K_d] and not p1_chose:
        selected_field_p1 += 1

# Player 2
    if keys[pygame.K_UP]:
        p2_chose = True
    if keys[pygame.K_LEFT] and not p2_chose:
        selected_field_p2 -= 1
    if keys[pygame.K_DOWN]:
        p2_chose = False
    if keys[pygame.K_RIGHT] and not p2_chose:
        selected_field_p2 += 1

    selected_field_p1 %= len(fields)
    selected_field_p2 %= len(fields)

# Drawing and stuff depending on which menue is open
    if menue_p:
        if p1_chose and p2_chose:
            racer1 = Racer(None, None, racersToChoose[selected_field_p1], 90)
            racer2 = Racer(None, None, racersToChoose[selected_field_p2], 90)
            menue_p = False
            menue_track_select()

    if menue_t:
        if p1_chose and p2_chose:
            if  selected_field_p1 == selected_field_p2:
                chosen_track = tracksToChoose[selected_field_p1]
            else:
                x = random.randrange(0,1)
                if x == 0:
                    chosen_track = tracksToChoose[selected_field_p1]
                else:
                    chosen_track = tracksToChoose[selected_field_p2]
            menue_t = False
            race(racer1, racer2, chosen_track)

# Draw "cursors"
    pygame.draw.rect(Menue_surf, red, fields[selected_field_p1].rect1, 5)
    pygame.draw.rect(Menue_surf, blue, fields[selected_field_p2].rect2, 5)


def spawn_racers(racer1, racer2):
    global rand_start_point
    racer1.x = rand_start_point[0]
    racer1.y = rand_start_point[1]
    racer2.x = rand_start_point[0]
    racer2.y = rand_start_point[1]

# Gameloops
                
# Starting screen
    
def starting_screen(): 
    starting_screen = True
    background = pygame.transform.scale(pygame.image.load("sprites/menue/starting_screen.png"), screenSize)
    spawn_fake_racers()
    
    while starting_screen:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                else:
                    starting_screen = False
                    menue_player_select()

        Menue_surf.blit(background, (0,0))

        move_fake_racers()

        screen.blit(Menue_surf, (0,0))
        pygame.display.flip()
        clock.tick(360)



# Player selection

def menue_player_select():
    global p1_chose, p2_chose, menue_p, menue_t, selected_field_p1, selected_field_p2
    menue_p = True
    menue_t = False
    background = pygame.image.load("sprites/menue/pselect.png")
    add_racer_fields()
    p1_chose = False
    p2_chose = False
    selected_field_p1 = 0
    selected_field_p2 = 0

    while menue_p:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menue_p = False
                    starting_screen()
            if event.type == pygame.QUIT:
                pygame.quit()

        Menue_surf.blit(background, (0,0))
        draw_fields(fields)
        
        handle_selection(menue_p, menue_t)

        screen.blit(Menue_surf, (0,0))
        pygame.display.flip()
        clock.tick(10)



# Track selektion

def menue_track_select():
    global p1_chose, p2_chose, menue_p, menue_t
    menue_t = True
    menue_p = False
    background = pygame.image.load("sprites/menue/tselect.png")
    add_track_fields()
    p1_chose = False
    p2_chose = False

    while menue_t:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menue_t = False
                    menue_player_select()
            if event.type == pygame.QUIT:
                pygame.quit()
    
        Menue_surf.blit(background, (0,0))
        draw_fields(fields)
        
        handle_selection(menue_p, menue_t)

        screen.blit(Menue_surf, (0,0))
        pygame.display.flip()
        clock.tick(10)



# Race

def race(racer1, racer2, chosen_track):
    global delta_time
    
    import_track(chosen_track)

    spawn_racers(racer1, racer2)
 
    racing = True
    while racing:
        for event in pygame.event.get():
            if event.type == pygame.K_ESCAPE:
                racing = False
                menue_track_select()
            if event.type == pygame.QUIT:
                pygame.quit()
        
        Track_surf.blit(track, (screen_width // 2 - track.get_width() // 2, screen_height // 2 - track.get_height() // 2))
        racer1.update_n_draw()
        racer2.update_n_draw()

        screen.blit(Track_surf, (0,0))
        screen.blit(Racer_surf, (0,0))
        pygame.display.flip()
        clock.tick(300)
        


# Start of the program

starting_screen()

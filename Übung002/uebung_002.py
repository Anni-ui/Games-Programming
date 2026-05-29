import pygame
import random

# ---- Bildschirm ----
SCREEN_WIDTH = 600 
SCREEN_HEIGHT = 400

# ---- Farben (Rot, Grün, Blau, [Alpha]) ----
BACKGROUND_COL = (20, 100, 200)
GROUND_COL = (80, 70, 30)
PLAYER_COL = (30, 210, 76)
CIRCLE_COL = (200, 200, 255)
TEXT_COL = (255, 255, 255)

# ---- pygame starten ----
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump & Run")
clock = pygame.time.Clock()

# ---- Sound ----
jump_sound = pygame.mixer.Sound("jump.wav")


# ---- Player ----
player_x = 100.0
player_y = 100.0
player_radius = 20
player_moving_left = False
player_moving_right = False
player_movement_y = 0
player_gravity = 0.1
player_image = pygame.image.load("otter_3.png").convert_alpha()

# ---- Bouncing circle (aus dem "Boing boing"-Beispiel) ----
circle_x = 300.0
circle_y = 50.0
circle_radius = 10
circle_movement_x = 1.0
circle_movement_y = 0.0
gravity = 0.1

# ---- Obstacles (Boden + Plattformen) ----
# Jedes Obstacle ist ein pygame.Rect(x, y, breite, hoehe)
obstacles = []

# Boden
obstacles.append(pygame.Rect(5, SCREEN_HEIGHT - 10, SCREEN_WIDTH - 10, 10))

# convert_alpha für sprites mit transparentem bg . convert mit solid bg - immer png 

# Plattform 001
obstacles.append(pygame.Rect(0, SCREEN_HEIGHT - 60, 150, 10))

# Plattform 002
obstacles.append(pygame.Rect(170, SCREEN_HEIGHT - 200, 40, 10))

# Plattform 003
obstacles.append(pygame.Rect(250, SCREEN_HEIGHT - 110, 60, 10))

# Plattform 004
obstacles.append(pygame.Rect(370, SCREEN_HEIGHT - 150, 80, 10))

# Plattform 005
obstacles.append(pygame.Rect(500, SCREEN_HEIGHT - 40, 100, 10))


# ---- Status-Text ----
status = "Wheee!"

#Player rect und circle rect definiert, um mit einander und anderen Dingen zu collidieren 
player_rect = pygame.Rect(player_x, player_y, player_radius * 2, player_radius * 2)
circle_rect = pygame.Rect(circle_x, circle_y, circle_radius, circle_radius)

#funktion (Spieler ist am Boden) die Gravitation vom Spieler wird ausgeschaltet, sodass er nicht durch den Boden fällt
def on_ground():
        global player_gravity
        player_gravity = 0
        global status
        status = "Ouch!"

    #funktion (Spieler ist nicht am Boden) die Gravitaion vom Spieler wird angeschaltet, sodass er nach dem Sprung wieder zu Boden fällt.    
def of_ground():
        global player_gravity
        player_gravity = 0.1   
        global status
        status = "Wheee!"

    #funktion Collision, checkt, ob der Player mit den Objekten aus Obstacles kolliediert. Falls ja wird die Bewegung auf der x-Achse angehalten und die Gravitation des Players auf 0 gesetzt, um ihn nicht weiter nach unten zu ziehen.
def collision():
        global player_movement_y
    
    #if funktion, um zu checken, ob der Player mit einem Obejekt aus der Obstacles liste kollidiert 
        if player_rect.collidelistall(obstacles):
            player_movement_y = 0
            on_ground()

        #Sprung (Tasteninput erhalten, Movement ausgeben und gravity wieder anstellen)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                player_movement_y  -= 5.5
                jump_sound.play()
                of_ground()
            elif keys[pygame.K_w]:
                player_movement_y  -= 5.5
                jump_sound.play()
                of_ground()
        else:
        #Wenn Player kein Objekt aus der Ostacles liste berührt wird die Gravitation wieder angestellt 
            of_ground()  

# ============================================================
# Game Loop
# ============================================================

running = True
while running:

    # ---- Events ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_moving_left = True
            elif event.key == pygame.K_d:
                player_moving_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_moving_left = False
            elif event.key == pygame.K_d:
                player_moving_right = False

    
    # ---- Update ----

    # Player-Bewegung + Gravitation 
    if player_moving_right:
        player_rect.x += 3
    elif player_moving_left:
        player_rect.x -= 3
    player_movement_y += player_gravity
    player_rect.y += player_movement_y

    # Checken, ob der Player mit den Wänden Collidiert. Falls ja wird die Bewegung auf der y-Achse des Players angehalten, sodass er nicht außerhalb des Bildschirms sein kann.
    if player_rect.x < 0:
       player_rect.x = 0
    if player_rect.x >= SCREEN_WIDTH - 40:
       player_rect.x = SCREEN_WIDTH - 40 
       

    #aufrufen der Collision funktion
    collision()

    if player_rect.colliderect(circle_rect):
        status = "Ouch!"
    # Bouncing circle: Gravitation + Bewegung
    circle_movement_y += gravity
    circle_x += circle_movement_x
    circle_y += circle_movement_y

    # Bouncing circle: Am Boden abprallen
    if circle_y >= SCREEN_HEIGHT - 20 - circle_radius:
        circle_movement_y = -circle_movement_y

    # Bouncing circle: An den Seiten abprallen
    if circle_x <= circle_radius or circle_x >= SCREEN_WIDTH - circle_radius:
        circle_movement_x = -circle_movement_x

    # ---- Draw ----
    screen.fill(BACKGROUND_COL)

    # Obstacles zeichnen
    for obs in obstacles:
        pygame.draw.rect(screen, GROUND_COL, obs)

    # Bouncing circle zeichnen
    pygame.draw.circle(screen, CIRCLE_COL, (int(circle_x), int(circle_y)), circle_radius)

    # Player zeichnen
    rect = player_image.get_rect(center=(player_rect.x, player_rect.y))
    screen.blit(player_image, rect)

    # Text zeichnen
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(status, True, TEXT_COL)
    screen.blit(text_surface, (30, 30))

    # ---- Flip ----
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
# main.py
# Game loop for RealFakeGame.
#
# Controls:
#   Mouse X  — move player left/right
#   ESC      — quit
#
# This skeleton provides:
#   - Player that follows mouse and auto-fires shots
#   - Level with background image
#   - Parsed (but inactive) enemies and obstacles

import pygame
from game import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from player import Player
from level import Level
from shot import Shot
from enemy import Enemy
#   from obstacle import Obstacle


def main():
    # ------------------------------------------------------------------ #
    #  Initialize pygame                                                 #
    # ------------------------------------------------------------------ #
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RealFakeGame")
    clock = pygame.time.Clock()

    # ------------------------------------------------------------------ #
    #  Setup — create player and load level (ofApp::setup)   #
    # ------------------------------------------------------------------ #
    player = Player()
    player.setup(
        x=SCREEN_WIDTH // 2,           # Center of screen
        y=SCREEN_HEIGHT - 50,           # Near bottom of screen
        dx=0,
        dy=0,
        image_prefix="player_stage",
        anim_speed=1,
        hp=100,
    )
    player.set_might(rng=1000,dmg=10, cad=10, shotspd=10)

    shot = Shot()

    enemy = Enemy()
    enemy.setup(
        x=SCREEN_WIDTH // 2,
        y=SCREEN_HEIGHT,
        dx=0,
        dy=0,
        image_prefix="enemy",
        anim_speed=1,
        hp=10,
        damage=1
    )

    #obstacle = Obstacle()
    #obstacle.setup(
    #)

    level = Level()
    level.load("lvl001.rfg")

    game_state = Game()     
    
       #game_state.change_state("titel")

    # ------------------------------------------------------------------ #
    #  Game loop                                                         #
    # ------------------------------------------------------------------ #
    #if game_state == "playing":
    running = True
    while running:
        dt = clock.tick(FPS)
        events = pygame.event.get()

        # -------------------------------------------------------------- #
        #  Event handling                                                #
        # -------------------------------------------------------------- #
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                     running = False

        # -------------------------------------------------------------- #
        #  Update                                                        #
        # -------------------------------------------------------------- #
        if game_state.state == "title":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        game_state.change_state("playing")

           #Draw
            screen.fill(BLACK)

            title_font = pygame.font.SysFont(None, 96)
            hint_font = pygame.font.SysFont(None, 40)

            title_text = title_font.render("Shooty^^", True, (255, 255, 255))
            hint_text = hint_font.render("Press E to play", True, (200, 200, 200))
           
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
            screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT // 2))

            pygame.display.flip()


        elif game_state.state == "playing":
            player.step()
            level.step()

        # -------------------------------------------------------------- #
        #  Collision                                                     
        # -------------------------------------------------------------- #
        # TODO: Check collisions (shots vs enemies, enemies vs player)
            for obstacle in level.obstacles:
                if obstacle.collision(player.get_rect()):
                    player.hp -= 1
                #elif obstacle.collision(Shot.get_rect()):
                    #print("hit")
            
            # Collison enemies and player (player verliert hp, enemies verlieren hp und despawnen)
            for enemies in level.enemies:
                if not enemy.alive:
                    continue

                if enemies.collision(player.get_rect()):
                    player.hp -= 1
                    enemies.hp -= 5
                    enemies.is_alive()

                elif enemies.collision(shot.get_rect()):
                    enemies.hp -= 100
                    enemies.is_alive()


        # TODO: Check player.hp <= 0 for death / game_state transition
            if player.hp <= 0:
                game_state.change_state("gameover")

        # -------------------------------------------------------------- #
        #  Draw                                                          #
        # -------------------------------------------------------------- #
            screen.fill(BLACK)

        # Draw level background first
            level.draw(screen)

            # TODO: Draw enemies
            for enemies in level.enemies:
                enemies.draw(screen)

            # TODO: Draw obstacles
            for obstacle in level.obstacles:
                obstacle.draw(screen)

            # Draw player (also draws its shots internally)
            player.draw(screen)

        # Game Over Text anzeigen     
        #screen.blit(text_image, (200, 250))

        # TODO: Draw player HP (text or health bar)

            pygame.display.flip()
            clock.tick(FPS)

        elif game_state.state == "gameover":
            screen.fill(BLACK)
            font = pygame.font.SysFont(None, 72)
            text = font.render("Game Over!", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()

    # ------------------------------------------------------------------ #
    #  Cleanup                                                           #
    # ------------------------------------------------------------------ #
    pygame.quit()


if __name__ == "__main__":
    main()

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
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from player import Player
from level import Level
#from player import Shot


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
    player.set_might(rng=1000, dmg=1, cad=50, shotspd=1)

    level = Level()
    level.load("lvl001.rfg")

    game_state = "gameover" # game over state (alles anhalten und Game over printen)
    game_state = "titel"    # titel state (title screen)
    game_state = "playing"  # TODO: Add "title" and "gameover" states
    
    #if game_state == "gameover":
    #font = pygame.font.Font()
    #text_image = font.render("Game Over!", True, (255, 255, 255))
    
    # ------------------------------------------------------------------ #
    #  Game loop                                                         #
    # ------------------------------------------------------------------ #
    #if game_state == "playing":
    running = True
    while running:

        # -------------------------------------------------------------- #
        #  Event handling                                                #
        # -------------------------------------------------------------- #
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

        # -------------------------------------------------------------- #
        #  Update                                                        #
        # -------------------------------------------------------------- #
            player.step()
            level.step()

        # TODO: Check collisions (shots vs enemies, enemies vs player)
            for obstacle in level.obstacles:
                if obstacle.collision(player.get_rect()):
                    player.hp -= 1
                #elif obstacle.collision(Shot.get_rect()):
                    #print("hit")
            
            # Collison enemies and player (player verliert hp, enemies verlieren hp und despawnen)
            for enemies in level.enemies:
                if enemies.collision(player.get_rect()):
                    player.hp -= 1
                    enemies.hp -= 5
                    enemies.is_alive()
                #elif enemies.collision(shot.get_rect()):
                    #enemies.hp -= 1
            
            #for shot in self.shots:
                #if shot.collision(enemies.get_rect):
                    #enemies.hp -= 5


        # TODO: Check player.hp <= 0 for death / game_state transition
            if player.hp <= 0:
                #game_state = "gameover"
                pygame.quit()

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

    # ------------------------------------------------------------------ #
    #  Cleanup                                                           #
    # ------------------------------------------------------------------ #
    pygame.quit()


if __name__ == "__main__":
    main()

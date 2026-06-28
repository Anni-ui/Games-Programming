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
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE
from player import Player
from level import Level
from shot import Shot
from enemy import Enemy


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
        y=20 ,
        dx=0,
        dy=0,
        image_prefix="enemy",
        anim_speed=1,
        hp=10,
        damage=1
    )

    level = Level()
    level.load("lvl001.rfg")

    game_state = Game()     
    

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

        # ------------------------------------------------------------------ #
        #  PLAYING                                                           #
        # ------------------------------------------------------------------ #
        elif game_state.state == "playing":
            player.step()
            level.step()

            for enemies in level.enemies:
                enemies.step(target_pos = player.pos, speed = 1)
  

        # -------------------------------------------------------------- #
        #  Collision                                                     #
        # -------------------------------------------------------------- #
            # Check collisions obstacle und player
            for obstacle in level.obstacles:
                if obstacle.active and obstacle.collision(player.get_rect()):
                    obstacle.active = False
                    player.random_upgrade()

                    #Upgrade Text anzeigen 
                    upgrade_font = pygame.font.SysFont(None, 30)
                    upgrade_text = upgrade_font.render("Upgrade", True, (BLACK))
                    screen.blit(upgrade_text, (SCREEN_WIDTH // 2 - upgrade_text.get_width() // 2, 10))
                    pygame.display.flip()

                # Enemy kann Obstacle nicht mehr überschreiten 
                for enemies in level.enemies:
                    if obstacle.collision(enemies.get_rect()):
                        # Position um einen Schritt zurücksetzen
                        direction = player.pos - enemies.pos
                        if direction.length() > 0:
                            direction = direction.normalize()
                        enemies.pos -= direction * 1  # Einen Schritt zurück


            # Collison enemies und player(player verliert hp, enemies verlieren hp und despawnen)
            for enemies in level.enemies:
                if not enemy.alive:
                    continue

                if enemies.collision(player.get_rect()):
                    player.hp -= 1
                    enemies.hp -= 5
                    enemies.is_alive()

            # Collision enemies und shots 
            for s in player.shots:
                if enemies.collision(s.get_rect()):
                    enemies.hp -= s.dmg                 # enemie verliert hp, je nach zugewiesenem Schadenswert des Shots
                    enemies.is_alive()                  # checkt, ob enemie noch hp hat 
                    s.life = 0                          # Schuss nach Treffer entfernen
                    break

            # Check player.hp <= 0 for death / game_state transition
            if player.hp <= 0:
                game_state.change_state("gameover")

        # -------------------------------------------------------------- #
        #  Draw                                                          #
        # -------------------------------------------------------------- #
            screen.fill(BLACK)

            # Draw level background first
            level.draw(screen)

            # Draw enemies
            for enemies in level.enemies:
                enemies.draw(screen)

            # Draw obstacles
            for obstacle in level.obstacles:
                if not obstacle.active:
                    continue
                obstacle.draw(screen)

            # Draw player (also draws its shots internally)
            player.draw(screen)

            # Draw player HP (text)
            hp_font = pygame.font.SysFont(None, 30)
            hp_text = hp_font.render(f"HP: {player.hp}", True, (WHITE))
            screen.blit(hp_text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)

        # ------------------------------------------------------------------ #
        #  GAME OVER                                                         #
        # ------------------------------------------------------------------ #
        elif game_state.state == "gameover":
            screen.fill(BLACK)
            gameover_font = pygame.font.SysFont(None, 72)
            gameover_text = gameover_font.render("Game Over!", True, (WHITE))
            screen.blit(gameover_text, (SCREEN_WIDTH // 2 - gameover_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()

        # ------------------------------------------------------------------ #
        #  SHOP                                                              #
        # ------------------------------------------------------------------ #
        elif game_state == "shop":
            screen.fill(BLACK)
            shop_font = pygame.font.SysFont(None, 72)
            shop_text = shop_font.render("Shop", True, (WHITE))
            screen.blit(shop_text, (SCREEN_WIDTH // 2 - shop_text.get_width() // 2, 10))


    # ------------------------------------------------------------------ #
    #  Cleanup                                                           #
    # ------------------------------------------------------------------ #
    pygame.quit()


if __name__ == "__main__":
    main()

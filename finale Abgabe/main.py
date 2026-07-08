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
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from title_context import TitleContext 


def main():
    # ------------------------------------------------------------------ #
    #  Initialize pygame                                                 #
    # ------------------------------------------------------------------ #
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RealFakeGame")
    clock = pygame.time.Clock()

    game = Game()
    game.push(TitleContext(game))

    # ------------------------------------------------------------------ #
    #  Game loop                                                         #
    # ------------------------------------------------------------------ #
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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if len(game.stack) > 1:
                    game.pop()
                else:
                    running = False
            else:
                game.handle_event(event)

        game.update(dt)

        game.draw(screen)
        pygame.display.flip()         

    # ------------------------------------------------------------------ #
    #  Cleanup                                                           #
    # ------------------------------------------------------------------ #
    pygame.quit()


if __name__ == "__main__":
    main()

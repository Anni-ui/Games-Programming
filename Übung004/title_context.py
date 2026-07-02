# title State

import pygame
from game import Context
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK

class TitleContext(Context):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.SysFont(None, 96)
        self.hint_font = pygame.font.SysFont(None, 40)

    # ------------------------------------------------------------------ #
    #  Events                                                            #
    # ------------------------------------------------------------------ #
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            from playing_context import PlayingContext
            self.game.replace(PlayingContext(self.game))

    # ------------------------------------------------------------------ #
    #  Draw                                                              #
    # ------------------------------------------------------------------ #
    def draw(self, screen):
        screen.fill(BLACK)
        title_text = self.title_font.render("Shooty^^", True, (255, 255, 255))
        hint_text = self.hint_font.render("Press E to play", True, (200, 200, 200))
           
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT // 2))
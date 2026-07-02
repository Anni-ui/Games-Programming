# Game Over State

import pygame
from game import Context
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, BLACK

class GameOver(Context):
    def __init__(self, game):
        super().__init__(game)
        self.points 

        self.gameover_font = pygame.font.SysFont(None, 72)
        self.high_score_font = pygame.font.SysFont(None, 30)

    # -------------------------------------------------------------- #
    #  Event                                                         #
    # -------------------------------------------------------------- #
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            from playing_context import PlayingContext
            self.game.replace(PlayingContext(self.game))  # neuer Run

    # -------------------------------------------------------------- #
    #  Draw                                                          #
    # -------------------------------------------------------------- #
    def draw(self, screen):
        screen.fill(BLACK)

        gameover_text = self.gameover_font.render("Game Over!", True, (WHITE))
        high_score_text = self.high_score_font.render(f"Highscore: {self.points.points}", True, (WHITE))

        screen.blit(high_score_text, (100, 10)) 
        screen.blit(gameover_text, (SCREEN_WIDTH // 2 - gameover_text.get_width() // 2, SCREEN_HEIGHT // 2))


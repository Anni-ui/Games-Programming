# Game Over State

import pygame
from game import Context
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, BLACK, RED

class GameWon(Context):
    def __init__(self, game, points):
        super().__init__(game)
        self.points = points

        self.gamewon_font = pygame.font.SysFont(None, 80)
        self.high_score_font = pygame.font.SysFont(None, 60)
        self.play_again_font = pygame.font.SysFont(None, 50)

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

        gamewon_text = self.gamewon_font.render("You Won!", True, (WHITE))
        high_score_text = self.high_score_font.render(f"Highscore: {self.points.points}", True, (WHITE))
        play_again_text = self.play_again_font.render("Press E to play again", True, (WHITE))

        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 10)) 
        screen.blit(gamewon_text, (SCREEN_WIDTH // 2 - gamewon_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))


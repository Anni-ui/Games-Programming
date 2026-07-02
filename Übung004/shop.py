#Shop klasse
import pygame
from game import Context
from settings import  SCREEN_WIDTH, WHITE

class ShopContext(Context):
    def __init__(self, game):
        super().__init__(game)
        self.shop_font = pygame.font.SysFont(None, 72)

    # -------------------------------------------------------------- #
    #  Event                                                         #
    # -------------------------------------------------------------- #
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.try_buy(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.pop()

    # -------------------------------------------------------------- #
    # buy                                                            #
    # -------------------------------------------------------------- #
    def try_buy(self, pos):
        pass

    # -------------------------------------------------------------- #
    #  Update                                                        #
    # -------------------------------------------------------------- #
    def update(self, dt):
         pass 

    # -------------------------------------------------------------- #
    #  Draw                                                          #
    # -------------------------------------------------------------- #
    def draw(self, screen):
            shop_text = self.shop_font.render("Shop", True, (WHITE))
            screen.blit(shop_text, (SCREEN_WIDTH // 2 - shop_text.get_width() // 2, 10))
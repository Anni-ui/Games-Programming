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
        for event in pygame.event.get():
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
            transparent_bg = pygame.Surface((600, 800), pygame.SRCALPHA)
            transparent_bg.fill((0, 0, 255, 100))

            shop_text = self.shop_font.render("Shop", True, (WHITE))
            screen.blit(transparent_bg, (0, 0))
            screen.blit(shop_text, (SCREEN_WIDTH // 2 - shop_text.get_width() // 2, 10))
#Shop klasse
import pygame
import random 
from game import Context
from settings import  SCREEN_WIDTH, WHITE


class ShopContext(Context):
    RARITY = {"common": 10, "rare": 3, "legendary": 1}

    UPGRADES = [
    {"name": "Blades", "rarity": "common", "cost": 1, "effect": {"stat": "dmg", "op": "add", "value": 10}},
    {"name": "Heal", "rarity": "common", "cost": 1, "effect": {"stat": "hp", "op": "add", "value": 10}},
    {"name": "Berserk", "rarity": "rare", "cost": 5, "effect": {"stat": "dmg", "op": "mul", "value": 5}},
    {"name": "Speed", "rarity": "common", "cost": 1, "effect": {"stat": "shotspd", "op": "mul", "value": 1.5}},
    ]

    def __init__(self, game, player, points):
        super().__init__(game)
        self.player = player
        self.points = points
        self.shop_font = pygame.font.SysFont(None, 72)
        self.item_font = pygame.font.SysFont(None, 40)

        self.offers = self.draft(self.UPGRADES, k=3)                 # 3 zufällige angebote werden ausgewählt
        self.offer_rects : list[pygame.Rect] = []

    # -------------------------------------------------------------- #
    #  Event                                                         #
    # -------------------------------------------------------------- #
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.try_buy(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.game.pop()

    def draft(self, pool, k=3):
        pool = pool[:]                      # copy to mutate
        picks = []
        for _ in range(k):
            weights = [self.RARITY[u["rarity"]] for u in pool]
            chosen = random.choices(pool, weights)[0]
            pool.remove(chosen)             # no dupes
            picks.append(chosen)
        return picks

    # -------------------------------------------------------------- #
    # buy                                                            #
    # -------------------------------------------------------------- #
    def try_buy(self, pos):
        from sounds import Sounds                                    # Sounds werden importiert, da sie nur in dieser funktion verwendet werden 
        sounds = Sounds()
        for rect, upgrade in zip(self.offer_rects, self.offers):
            if rect.collidepoint(pos):
                if self.points.trümmer >= upgrade["cost"]:           # checkt, ob genügend Trümmer vorhanden sind um das Upgrade zu kaufen 
                    self.points.trümmer -= upgrade["cost"]           # verringert Trümmer um die Kosten des Upgrades 
                    sounds.buy.play()                                # Sound für das kaufen wird abgespielt 
                    self.apply_effect(self.player, upgrade["effect"])
                    self.offers.remove(upgrade)                      # gekauftes Angebot verschwindet
                    print(f"Gekauft: {upgrade['name']}")
                else:
                    print("Nicht genug Trümmer!")
                    sounds.decline.play()                            # sound für nicht genug Trümmer wird abgespielt 
                break

    # -------------------------------------------------------------- #
    # Effekt auf den Spieler anwenden                                #
    # -------------------------------------------------------------- #
    def apply_effect(self, player, effect):                          # every upgrade
        stat = effect["stat"]
        op, value = effect["op"], effect["value"]
        
        current = getattr(player, stat)
        if op == "add":
            setattr(player, stat, current + value)
        elif op == "mul":
            setattr(player, stat, current * value)

        player.set_might(rng=player.rng, dmg=player.dmg, cad=player.cad, shotspd=player.shotspd, hp=player.hp)


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
            trümmer_text = self.item_font.render(f"Trümmer: {self.points.trümmer}", True, WHITE)

            screen.blit(transparent_bg, (0, 0))
            screen.blit(shop_text, (SCREEN_WIDTH // 2 - shop_text.get_width() // 2, 10))
            screen.blit(trümmer_text, (10, 90))

            self.offer_rects = []
            card_w, card_h = 160, 200
            gap = 20
            start_x = (SCREEN_WIDTH - (card_w * len(self.offers) + gap * (len(self.offers) - 1))) // 2
            y = 150

            for i, upgrade in enumerate(self.offers):
                x = start_x + i * (card_w + gap)
                rect = pygame.Rect(x, y, card_w, card_h)
                self.offer_rects.append(rect)

                pygame.draw.rect(screen, (40, 40, 60), rect)
                pygame.draw.rect(screen, WHITE, rect, width=2)

                name_text = self.item_font.render(upgrade["name"], True, WHITE)
                cost_text = self.item_font.render(f"{upgrade['cost']} Trümmer", True, WHITE)
                rarity_text = self.item_font.render(upgrade["rarity"], True, WHITE)

                screen.blit(name_text, (x + 10, y + 10))
                screen.blit(rarity_text, (x + 10, y + 40))
                screen.blit(cost_text, (x + 10, y + card_h - 30))

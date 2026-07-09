# Playing Klasse 
import pygame  
from game import Context
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK, RED, WHITE
from player import Player
from level import Level
from enemy import Enemy
from points import Points 
from shooting_enemy import ShotEnemy
from sounds import Sounds

LEVEL: list[str] = [
    "lvl001.rfg",
    "lvl002.rfg",
    "lvl003.rfg"
]
 
class PlayingContext(Context):
    def __init__(self, game, points = None):
        super().__init__(game)

        self.player = Player()
        self.player.setup(
            x=SCREEN_WIDTH // 2,                                    # Center of screen
            y=SCREEN_HEIGHT - 50,                                   # Near bottom of screen
            dx=0,
            dy=0,
            image_prefix="player_stage",
            anim_speed=1,
            hp=100,
        )
        

        
        self.points = points if points is not None else Points()

        self.enemy = Enemy()

        self.player.set_might(rng=1000,dmg=5, cad=30, shotspd=5, hp=100)

        self.sounds = Sounds()

        current_level = LEVEL[self.game.level_index]
        self.level = Level()
        self.level.load(current_level)

        self.font = pygame.font.SysFont(None, 30)
        self.boss_font = pygame.font.SysFont(None, 40)
        

    # -------------------------------------------------------------- #
    #  Update                                                        #
    # -------------------------------------------------------------- #
    def update(self, dt):
        self.player.step()
        self.level.step()

        for enemies in self.level.enemies:
            enemies.step(target_pos = self.player.pos)
        
        self.handle_collision()

        # Check player.hp <= 0 for death / game_state transition
        if self.player.hp <= 0:
            self.points.add_score()
            self.points.save_highscore(self.points.score)
            self.sounds.player_dead.play()
            from gameover_context import GameOver
            self.game.replace(GameOver(self.game, self.points))

        if self.level.boss is not None and self.level.boss.hp <= 0:
            if self.game.next_level():
                self.game.replace(PlayingContext(self.game, points = self.points))         # nächstes Level laden
            else:
                from gamewon_context import GameWon
                self.sounds.win.play()
                self.game.replace(GameWon(self.game, self.points))

    # -------------------------------------------------------------- #
    #  Event                                                         #
    # -------------------------------------------------------------- #    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            from shop_context import ShopContext
            self.game.push(ShopContext(self.game, self.player, self.points))       


    # -------------------------------------------------------------- #
    #  Collision                                                     #
    # -------------------------------------------------------------- #
    def handle_collision(self):
        # Check collisions obstacle und player
        for obstacle in self.level.obstacles:
            if obstacle.active and obstacle.collision(self.player.get_rect()):
                obstacle.active = False
                self.sounds.power_up.play()
                self.player.random_upgrade()

            # Enemy kann Obstacle nicht mehr überschreiten 
            for enemies in self.level.enemies:
                if obstacle.active and obstacle.collision(enemies.get_rect()):
                                                                     # Position um einen Schritt zurücksetzen
                    direction = self.player.pos - enemies.pos
                    if direction.length() > 0:
                        direction = direction.normalize()
                    enemies.pos -= direction * 1                     # Einen Schritt zurück


        # Collison enemies und player(player verliert hp, enemies verlieren hp und despawnen)
        for enemies in self.level.enemies:                           # checkt für jeden Enemy
            if not enemies.alive:                                    # checkt nicht, wenn der Enemy nicht mehr lebt 
                continue
 
            if enemies.collision(self.player.get_rect()):            # Collision enemy und player
                self.player.hp -= 1                          
                enemies.hp -= 5
                enemies.is_alive()                                   # checkt, ob enemy noch lebt 
                self.game.screen_shake.start(dauer = 17, intens = 4)
                if not enemies.alive:
                    self.points.bus.publish("enemy_died", enemy=enemies, points=10, trümmer=10)
                    Sounds.play_vary(Sounds.enemy_dead, 0.2, 0.6)
                    self.sounds.enemy_dead.play()
                self.points.bus.publish("player_hit")

        # Collision enemies und shots 
        for enemies in self.level.enemies:                           # checkt für jeden Enemy
            if not enemies.alive:                                    # checkt nicht, wenn der Enemy nicht mehr lebt
                continue
            for shot in self.player.shots:
                if enemies.collision(shot.get_rect()):
                    enemies.hp -= shot.dmg                           # enemie verliert hp, je nach zugewiesenem Schadenswert des Shots
                    enemies.is_alive()                               # checkt, ob enemie noch hp hat 
                    if not enemies.alive:
                        self.points.bus.publish("enemy_died", enemy=enemies, points=10, trümmer=10)
                        self.sounds.enemy_dead.play()
                    shot.life = 0                                    # Schuss nach Treffer entfernen
                    break
            
            # Collision enemy shots und Player
            if isinstance(enemies, ShotEnemy):
                for shot in enemies.shots:
                    if self.player.collision(shot.get_rect()):
                        self.game.screen_shake.start(dauer = 17, intens = 4)
                        self.player.hp -= shot.dmg
                        shot.life = 0
                        break

        if self.level.frame_count == self.level.boss.spawn_frame:      # checks if Boss is spawned 
            self.game.screen_shake.start(dauer = 30, intens = 7)

    # -------------------------------------------------------------- #
    # Draw                                                           #
    # -------------------------------------------------------------- #
    def draw(self, screen):
        screen.fill(BLACK)

        # Draw level background first
        self.level.draw(screen)

        # Draw enemies
        for enemies in self.level.enemies:
            enemies.draw(screen)

        # Draw obstacles
        for obstacle in self.level.obstacles:
            if not obstacle.active:
                continue
            obstacle.draw(screen)

        # Draw player (also draws its shots internally)
        self.player.draw(screen)

        # Draw Boss hp 
        if self.level.frame_count >= self.level.boss.spawn_frame:      # checks if Boss is spawned 
            self.game.screen_shake.start(dauer = 10, intens = 3)
            # Draw Boss Hp
            rect = pygame.Rect(SCREEN_WIDTH // 2 - self.level.boss.hp, 50, self.level.boss.hp * 2, 10)
            pygame.draw.rect(screen, (RED), rect) 

            # Draw "Boss" over boss hp 
            boss_text = self.boss_font.render("Boss", True, (WHITE))
            screen.blit(boss_text, (SCREEN_WIDTH // 2 - 34, 10))

        # Draw player HP (text)
        hp_text = self.font.render(f"HP: {self.player.hp}", True, (RED))
        screen.blit(hp_text, (10, 10))

        # Draw Points 
        point_text = self.font.render(f"Points: {self.points.points}", True, (WHITE))
        screen.blit(point_text, (100, 10))

        # Draw Points 
        trümmer_text = self.font.render(f"Trümmer: {self.points.trümmer}", True, (WHITE))
        screen.blit(trümmer_text, (10, 770))
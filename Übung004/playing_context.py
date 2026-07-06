# Playing Klasse 
import pygame  
from game import Context
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK, RED
from player import Player
from level import Level
from enemy import Enemy
from points import Points 
from shooting_enemy import ShotEnemy
from enemy_shot import EnemyShot

class PlayingContext(Context):
    def __init__(self, game):
        super().__init__(game)

        self.player = Player()
        self.player.setup(
            x=SCREEN_WIDTH // 2,           # Center of screen
            y=SCREEN_HEIGHT - 50,           # Near bottom of screen
            dx=0,
            dy=0,
            image_prefix="player_stage",
            anim_speed=1,
            hp=100,
        )
        
        
        self.points = Points()

        self.enemy = Enemy()

        self.player.set_might(rng=1000,dmg=5, cad=30, shotspd=5)


        self.level = Level()
        self.level.load("lvl001.rfg")

        self.hp_font = pygame.font.SysFont(None, 30)
        self.point_font = pygame.font.SysFont(None, 30)
        self.trümmer_font = pygame.font.SysFont(None, 30)

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
            from gameover_context import GameOverContext
            self.game.replace(GameOverContext(self.game, self.points))

    # -------------------------------------------------------------- #
    #  Event                                                         #
    # -------------------------------------------------------------- #    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            from shop_context import ShopContext
            self.game.push(ShopContext(self.game))       
  
    # -------------------------------------------------------------- #
    #  Collision                                                     #
    # -------------------------------------------------------------- #
    def handle_collision(self):
        # Check collisions obstacle und player
        for obstacle in self.level.obstacles:
            if obstacle.active and obstacle.collision(self.player.get_rect()):
                obstacle.active = False
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
                if not enemies.alive:
                    self.points.bus.publish("enemy_died", enemy=enemies, points=10, trümmer=10)
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
                    shot.life = 0                                    # Schuss nach Treffer entfernen
                    break
            
            # Collision enemy shots und Player
            if isinstance(enemies, ShotEnemy):
                for shot in enemies.shots:
                    if self.player.collision(shot.get_rect()):
                        self.player.hp -= shot.dmg
                        shot.life = 0
                        break

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

        # Draw player HP (text)
        hp_text = self.hp_font.render(f"HP: {self.player.hp}", True, (RED))
        screen.blit(hp_text, (10, 10))

        # Draw Points 
        point_text = self.point_font.render(f"Points: {self.points.points}", True, (BLACK))
        screen.blit(point_text, (100, 10))

        # Draw Points 
        trümmer_text = self.trümmer_font.render(f"Trümmer: {self.points.trümmer}", True, (BLACK))
        screen.blit(trümmer_text, (10, 770))

    #def handle_event(self, e):
    #    if e.type == KEYDOWN and e.key == K_SPACE:
    #        self.player.fire()
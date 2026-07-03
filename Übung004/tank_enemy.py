# Enemy für Level 2 (langsamer mit mehr hp)
import pygame
from enemy import Enemy

class TankEnemy(Enemy):
    # ------------------------------------------------------------------ #
    #  setup — initialize tank enemy (extends Enemy.setup)               #
    # ------------------------------------------------------------------ #
    def setup(
        self,
        x: float,
        y: float,
        dx: float,
        dy: float,
        image_prefix: str,
        anim_speed: int,
        hp: int = 30,
        damage: int = 1,
        speed: int = 1
        ):
        """Initialize enemy with position, images, and damage."""
        super().setup(x, y, dx, dy, image_prefix, anim_speed)
        self.damage = damage
        self.ready = False
        self.alive = True
        self.speed = speed 
        self.hp = hp
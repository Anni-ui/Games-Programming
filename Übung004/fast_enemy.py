# Enemy für Level 1 (schnell)
import pygame
from enemy import Enemy

class FastEnemy(Enemy):
    # ------------------------------------------------------------------ #
    #  setup — initialize fast enemy (extends Enemy.setup)               #
    # ------------------------------------------------------------------ #
    def setup(
        self,
        x: float,
        y: float,
        dx: float,
        dy: float,
        image_prefix: str,
        anim_speed: int,
        hp: int = 10,
        damage: int = 1,
        speed: int = 3
        ):
        """Initialize enemy with position, images, and damage."""
        super().setup(x, y, dx, dy, image_prefix, anim_speed)
        self.damage = damage
        self.ready = False
        self.alive = True
        self.speed = speed 
        self.hp = hp

    
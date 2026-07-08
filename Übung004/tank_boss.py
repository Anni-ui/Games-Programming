# Enemy für Level 2 (langsamer mit mehr hp)
import pygame
from tank_enemy import TankEnemy

class TankBoss(TankEnemy):
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
        hp: int = 400,
        damage: int = 1,
        speed: int = 1
        ):
        """Initialize enemy with position, images, and damage."""
        super().setup(x, y, dx, dy, image_prefix, anim_speed, hp, damage, speed)
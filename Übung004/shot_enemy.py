# Enemy für Level 3 (schießt zurück)
import pygame
from enemy import Enemy

class ShotEnemy(Enemy):
    def setup(self, x, y, dx, dy, image_prefix, anim_speed, hp, damage = 1, speed = 1):
        return super().setup(x, y, dx, dy, image_prefix, anim_speed, hp, damage, speed)
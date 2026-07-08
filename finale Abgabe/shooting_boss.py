# Boss Klasse

from shooting_enemy import ShotEnemy

class ShotBoss(ShotEnemy):
    # ------------------------------------------------------------------ #
    #  setup — initialize shooting enemy (extends Enemy.setup)           #
    # ------------------------------------------------------------------ #
    def setup(
        self,
        x: float,
        y: float,
        dx: float,
        dy: float,
        image_prefix: str,
        anim_speed: int,
        hp: int = 200,
        damage: int = 1,
        speed: float = 0.5
        ):
        """Initialize enemy with position, images, and damage."""
        super().setup(x, y, dx, dy, image_prefix, anim_speed, hp, damage, speed)
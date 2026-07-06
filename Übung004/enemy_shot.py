# shot for shotting enemy

from shot import Shot 

class EnemyShot(Shot):
    # ------------------------------------------------------------------ #
    #  setup — initialize shot with position, direction, range, damage   #
    # ------------------------------------------------------------------ #
    def setup(
        self,
        x: float,
        y: float,
        dx: float,
        dy: float,
        image_prefix: str,
        anim_speed: int,
        hp: int,
        rng: int = 1000,
        dmg: int = 1,
    ):
        """Set up the shot. Range determines lifetime in frames."""
        super().setup(x, y, dx, dy, image_prefix, anim_speed, hp)
        self.rng = rng
        self.dmg = dmg
        self.life = rng

        # Set hitbox to image dimensions (matches C++ behavior)
        if self.images:
            rect = self.images[0].get_rect()
            self.hitbox_w = rect.width
            self.hitbox_h = rect.height

    # ------------------------------------------------------------------ #
    #  step — move and decrement lifetime                                #
    # ------------------------------------------------------------------ #
    def step(self):
        """Move the shot and reduce its remaining life."""
        super().step()
        self.life -= abs(self.dir.y)

    def collision(self, rect):
        if self.get_rect().colliderect(rect):
            return True
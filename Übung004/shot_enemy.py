# Enemy für Level 3 (schießt zurück)
import pygame
from enemy import Enemy
from shot import Shot

class ShotEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.shots: list[Shot] = []   # Active shots

        # Weapon stats (matching C++ defaults)
        self.rng = 100                                                   # Shot range in frames
        self.dmg = 1                                                     # Damage per shot
        self.cad = 50                                                    # Cadence: frames between shots
        self.shotspd = 1                                                 # Shot speed (pixels per frame, upward)

        self._cad_counter = 0                                            # Countdown to next shot
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
        hp: int = 10,
        damage: int = 1,
        speed: int = 1
        ):
        """Initialize enemy with position, images, and damage."""
        super().setup(x, y, dx, dy, image_prefix, anim_speed, hp, damage, speed)

    # ------------------------------------------------------------------ #
    #  set_might — configure weapon stats (mirrors C++ setMight)         #
    # ------------------------------------------------------------------ #
    def set_might(self, rng: int, dmg: int, cad: int, shotspd: int):
        """Configure weapon stats. Called from main after setup."""
        self.rng = rng
        self.dmg = dmg
        self.cad = cad
        self.shotspd = shotspd
        self._cad_counter = cad

    # ------------------------------------------------------------------ #
    #  step — STUB: calculates direction toward target                   #
    # ------------------------------------------------------------------ #
    def step(self, target_pos: pygame.Vector2):
        """STUB: Calculate direction toward target.
        The C++ version computes the vector but doesn't apply it.
        Students should implement actual movement here."""
        if self.alive:
            direction = target_pos - self.pos                            # Calculate direction toward target (not applied — stub)
            if direction.length() > 0:
                direction = direction.normalize()                        # Normalize direction

            self.pos += direction * self.speed                           # bewegung in richtung des Ziels mit der Geschwindigkeit multipliziert 

        # Cadence countdown — fire a shot when it reaches 0
        self._cad_counter -= 1
        if self._cad_counter <= 0:
            self._cad_counter = self.cad
            self.create_shot()

        # Step all active shots
        for shot in self.shots:
            shot.step()

        # Remove dead shots
        self.shots = [s for s in self.shots if s.is_alive()]

    # ------------------------------------------------------------------ #
    #  create_shot — spawn a new shot below Enemy                        #
    # ------------------------------------------------------------------ #
    def create_shot(self):
        """Create a shot 10px above the player, moving upward."""
        shot = Shot()
        shot.setup(
            x=self.pos.x,
            y=self.pos.y + 10,      # 10 px unter dem enemy 
            dx=0,
            dy= self.shotspd,        # Moving downward (positiv Y)
            image_prefix="Shot",
            anim_speed=1,
            hp=1,
            rng=self.rng,
            dmg=self.dmg,
        )
        self.shots.append(shot)

    # ------------------------------------------------------------------ #
    #  Draw Enemy and all Shots                                          #
    # ------------------------------------------------------------------ #
    def draw(self, screen: pygame.Surface):
        """Draw the player and all active shots."""
        # Draw shots first (behind player)
        for shot in self.shots:
            shot.draw(screen)
        # Draw player
        super().draw(screen)
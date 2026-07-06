# enemy.py
# STUBBED enemy class. Students will implement AI, drawing, and collision.

import pygame
from eventBus import EventBus
from entity import Entity

bus = EventBus()

class Enemy(Entity):
    """STUB: Enemy entity. Has fields but no real behavior yet.

    Students should implement:
    - step(target): move toward target
    - draw(): render the enemy
    - Collision with player shots
    - Spawning from level data
    """

    def __init__(self):
        super().__init__()
        self.damage = 0                                                  # Damage dealt to player on contact
        self.starting_point = 0                                          # Spawn frame (when in the level duration)
        self.ready = False                                               # Whether the enemy has been activated
        self.alive = True                                                # Whether the enemy is still alive

    # ------------------------------------------------------------------ #
    #  setup — initialize enemy (extends Entity.setup)                   #
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
        damage: int = 1,
        speed: float = 1
    ):
        """Initialize enemy with position, images, and damage."""
        super().setup(x, y, dx, dy, image_prefix, anim_speed, hp)
        self.damage = damage
        self.ready = False
        self.alive = True
        self.speed = speed 

    # ------------------------------------------------------------------ #
    #  step — STUB: calculates direction toward target but doesn't move  #
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


    # ------------------------------------------------------------------ #
    #  wird nur gezeichnet, wenn enemy lebt                              #
    # ------------------------------------------------------------------ #
    def draw(self, screen):
        if not self.alive:
            return              # Toter Enemy wird nicht gezeichnet
        super().draw(screen)

    # ------------------------------------------------------------------ #
    #  gets rect for collision                                           #
    # ------------------------------------------------------------------ #
    def collision(self, rect):
        if not self.alive:
            return False
        return self.get_rect().colliderect(rect)

    # ------------------------------------------------------------------ #
    #  is_alive — check if enemy HP is above 0 (latches to dead)         #
    # ------------------------------------------------------------------ #
    def is_alive(self) -> bool:
        """Return True if the enemy is alive. Once HP drops to 0,
        alive is permanently set to False (mirrors C++ behavior)."""
        if self.hp <= 0 and self.alive:
            self.alive = False
            self.die()
        return self.alive
    
    def die(self):
        bus.publish("enemy_died", enemy=self, points=10)

# obstacle.py
# Simple obstacle data class. Parsed from level file but NOT drawn or
# collision-checked in the skeleton. Students implement this in Uebung 003.
import pygame
from entity import Entity

class Obstacle(Entity):
    """Data-only obstacle. Parsed from .rfg level files.

    Students should implement:
    - draw(): render the obstacle as a colored rectangle
    - Collision detection with player
    """
    
    def __init__(
        self,
        track: int = 0,
        duration_start: int = 0,
        length: int = 0,
        color: tuple[int, int, int] = (255, 255, 255),
        width: int = 5,
        upgrade: bool = True,
        hitbox_h = 0,
        hitbox_w = 0,
        speed: int = 2
    ):
        self.track = track              # Which track (column) the obstacle is on
        self.duration_start = duration_start  # When it appears (in level duration)
        self.length = length            # How long it lasts (in duration units)
        self.color = color              # RGB color tuple
        self.width = width              # Pixel width
        self.upgrade = upgrade          # upgrades for player 
        self.hitbox_h = hitbox_h        # hitbox height obstacles
        self.hitbox_w = hitbox_w        # hitbox width obstacles
        self.speed = speed              # moving speed of obstacle 
            
        # Derived screen coordinates (students compute these from track layout)
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
    
    # get Collider
    def collision(self, rect):
        if self.get_rect().colliderect(rect):
            return True

    # Move down 
    def step(self, speed):
        self.pos.y += speed 

    #obstacles = pygame.Rect(5, 5, 5, 5)

    #if obstacles.update == True:
    #    print ("HEY")
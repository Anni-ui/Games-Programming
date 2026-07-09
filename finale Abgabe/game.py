#game.py 
# Context Klasse, von der alle State Klassen erben 

import pygame
from sounds import  BASE_DIR
import os
from shake import ScreenShake

class Context:
 
    def __init__(self, game):
        self.game = game                                                # Referenz zurück auf Game, für push()/pop()/replace()
 
    def handle_event(self, event):
        pass
 
    def update(self, dt):
        pass
 
    def draw(self, screen):
        pass

class Game:

    def __init__(self,):
        self.stack = []
        self.level_index = 0

        self.screen_shake = ScreenShake()

        pygame.mixer.music.load(os.path.join(BASE_DIR, "assets", "sounds", "musik.wav"))
        pygame.mixer.music.play(loops=-1)


    # -------------------------------------------------------------- #
    #  nächstes Level                                                #
    # -------------------------------------------------------------- # 
    def next_level(self):
        self.level_index += 1
        from playing_context import LEVEL                            # lokal importieren, um zirkuläre Imports zu vermeiden
        if self.level_index >= len(LEVEL):
            self.level_index = 0            
            return False
        return True
    
        #self.points.add_score()
        #self.points.save_highscore(self.points.score)
        #from gameover_context import GameOver
        #self.game.replace(GameOver(self.game, self.points))  
        #current_level = LEVEL[index_nummer]

    # ------------------------------------------------------------------ #
    #  erstes Level                                                      #
    # ------------------------------------------------------------------ # 
    def reset_level(self):
        self.level_index = 0

    # ------------------------------------------------------------------ #
    #  legt neue Ebene oben drauf                                        #
    # ------------------------------------------------------------------ #
    def push(self, ctx): 
        self.stack.append(ctx)

    # ------------------------------------------------------------------ #
    #  entfernt oberste Ebene                                            #
    # ------------------------------------------------------------------ #
    def pop(self):       
        if self.stack:
            self.stack.pop()

    # ------------------------------------------------------------------ #
    #  ersetz oberste Ebene                                              #
    # ------------------------------------------------------------------ #
    def replace(self, ctx):
        if self.stack:
            self.stack.pop()
        self.stack.append(ctx)

    @property
    def current(self):
        return self.stack[-1] if self.stack else None    

    # ------------------------------------------------------------------ #
    #  leitet befehle an oberste Ebene                                   #
    # ------------------------------------------------------------------ #
    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)

    # ------------------------------------------------------------------ #
    #  nur die oberste Ebene wird aktualisiert                           #
    # ------------------------------------------------------------------ #
    def update(self, dt):
        if self.current:
            self.current.update(dt)

        self.screen_shake.update()

    # ------------------------------------------------------------------ #
    #  zeichnet alles von unten nach oben                                #
    # ------------------------------------------------------------------ #
    def draw(self, screen):
        game_surface = pygame.Surface(screen.get_size())

        for ctx in self.stack:                                           # bottom-up
            ctx.draw(game_surface)                                       # shop over game

        dx, dy = self.screen_shake.get_offset()
        screen.fill((0, 0, 0))                                           # Bildschirm leeren
        screen.blit(game_surface, (dx, dy))                              # mit Offset draufkopieren
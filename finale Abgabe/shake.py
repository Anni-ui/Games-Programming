# class for screen shake

import random 

class ScreenShake:
    def __init__(self):
        self.dauer: int = 0      
        self.intens: int = 0

    # ------------------------------------------------------------------ #
    # startet den screen shake                                           #
    # ------------------------------------------------------------------ #
    def start(self, dauer, intens):
        self.dauer = dauer
        self.intens = intens

    # ------------------------------------------------------------------ #
    # verringert die verbleibende dauer                                  #
    # ------------------------------------------------------------------ #
    def update(self):
        if self.dauer > 0:
            self.dauer -= 1

    # ------------------------------------------------------------------ #
    # gibt den Versatz zurück                                            #
    # ------------------------------------------------------------------ #
    def get_offset(self):
        if self.dauer <= 0:
            return (0, 0)
        dx = random.uniform(-self.intens, self.intens)
        dy = random.uniform(-self.intens, self.intens)
        return (dx, dy)
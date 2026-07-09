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
        """Shake auslösen, z.B. bei Treffer oder Explosion."""
        self.dauer = dauer
        self.inten = intens

    # ------------------------------------------------------------------ #
    # verringert die verbleibende dauer                                  #
    # ------------------------------------------------------------------ #
    def update(self):
        """Muss jeden Frame aufgerufen werden, reduziert die verbleibende Dauer."""
        if self.dauer > 0:
            self.dauer -= 1

    # ------------------------------------------------------------------ #
    # gibt den Versatz zurück                                            #
    # ------------------------------------------------------------------ #
    def get_offset(self):
        """Gibt den aktuellen Versatz (dx, dy) zurück."""
        if self.dauer <= 0:
            return (0, 0)
        dx = random.uniform(-self.intens, self.intens)
        dy = random.uniform(-self.intens, self.intens)
        return (dx, dy)
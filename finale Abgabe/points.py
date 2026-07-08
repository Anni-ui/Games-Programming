# Points & Währung (Trümmer)
#Points are stored and compared to set the highscore

import json
from eventBus import EventBus

class Points:
    def __init__(self):
        self.points: int = 0
        self.combo_hit: int = 0
        self.score: int = (self.load_highscore() or 0)
        self.trümmer: int = 0
    
        self.bus = EventBus()
        self.bus.subscribe("enemy_died", self._on_enemy_died)
        self.bus.subscribe("player_hit", self._on_player_hit)

    # -------------------------------------------------------------- #
    #  Combo                                                         #
    # -------------------------------------------------------------- #
    def combo_level(self) -> int:
        return self.combo_hit // 5 + 1                               # Combo Level wird nach 5 treffern erhöt

    # -------------------------------------------------------------- #
    #  Highscore speichern                                           #
    # -------------------------------------------------------------- #   
    def _on_enemy_died(self, enemy=None, points=0, trümmer=0):
        self.points += self.combo_level()                              # Punkte steigen, um das Combo Level 
        self.combo_hit += 1   
        self.trümmer += 1

    # -------------------------------------------------------------- #
    #  Highscore speichern                                           #
    # -------------------------------------------------------------- #   
    def _on_player_hit(self, **kwargs):
        self.combo_hit = 0                                           # Combo wird auf 0 zurückgesetzt 

    # -------------------------------------------------------------- #
    #  Highscore speichern                                           #
    # -------------------------------------------------------------- #    
    def save_highscore(self, score: int) -> None:
        with open("highscore.json", "w") as f:
            json.dump({"highscore": score}, f)

    # -------------------------------------------------------------- #
    #  Highscore laden                                               #
    # -------------------------------------------------------------- #
    def load_highscore(self) -> int:
        try:
            with open("highscore.json", "r") as f:
                data = json.load(f)
            return data.get("highscore", 0)
        except FileNotFoundError:
            return 0

    # -------------------------------------------------------------- #
    #  Vergleich neuer Score und Highscore                           #
    # -------------------------------------------------------------- #        
    def add_score(self):
        if self.score < self.points:                                           # wenn Score kleiner ist als Points
            self.score = self.points                                           # dann wird score zu points, um den neuen Highscore zu setzen 


    #bus.publish("enemy_died", enemy=g, points=10)
    #def add_score(enemy, points): score.add(points)
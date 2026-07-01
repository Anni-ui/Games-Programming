# Points
#Points are stored and compared to set the highscore

import json
from eventBus import EventBus

class Points:
    
    score: int = 0
    points: int = 0

    bus = EventBus()

    bus.subscribe("enemy_died", lambda enemy, points: score.add(points))

    def save_highscore(score: int) -> None:
        with open("highscore.json", "w") as f:
            json.dump({"highscore": score}, f)

    def load_highscore() -> int:
        try:
            with open("highscore.json", "r") as f:
                data = json.load(f)
            return data.get("highscore", 0)
        except FileNotFoundError:
            return 0
        
    def add_score(points, score):
        if score < points:
            score = points 


    #bus.publish("enemy_died", enemy=g, points=10)
    #def add_score(enemy, points): score.add(points)
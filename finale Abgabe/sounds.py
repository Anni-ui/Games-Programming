# Sounds - Sounds werden hier geladen 

import pygame
import os
import random
import numpy as np

pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(BASE_DIR, "assets/sounds/")


def load_sound(name):
        return pygame.mixer.Sound(os.path.join(SOUND_DIR, name))

# ---------------------------------------------------------------------- #
# verändert den pitch des Sounds                                         #
# ---------------------------------------------------------------------- #
def pitch_shift(sound, semitones=None, factor=None):
    if factor is None:
          factor = 2 ** (semitones / 12)

    arr = pygame.sndarray.array(sound)
    old_len = arr.shape[0]
    new_len = int(old_len / factor)

    indices = np.linspace(0, old_len - 1, new_len)
    indices = indices.astype(np.int32)

    if arr.ndim == 1:
        new_arr == arr[indices]
    else:
        new_arr = arr[indices, :]

    new_arr = np.ascontiguousarray(new_arr)
    return pygame.sndarray.make_sound(new_arr)


class Sounds():

    # ------------------------------------------------------------------ #
    # lädt alle Sounds                                                   #
    # ------------------------------------------------------------------ #
    musik = load_sound("musik.wav")
    buy = load_sound("buy.wav")
    decline = load_sound("decline.wav")
    enemy_shot = load_sound("enemy_shot.wav")
    enemy_dead = load_sound("enemy_dead.wav")
    player_shot = load_sound("player_shot.wav")
    player_dead = load_sound("player_dead.wav")
    power_up =load_sound("power_up.wav")
    win = load_sound("win.wav")

    enemy_shot.set_volume(0.5)
    player_shot.set_volume(0.5)

    volume: float = 0.5 

    # ------------------------------------------------------------------ #
    # berechnet eine leicht veränderte variante                          #
    # ------------------------------------------------------------------ #    
    def play_vary(sound, amount=0.1, volume=0.5):     # +/- 10% by default
        factor = random.uniform(1 - amount, 1 + amount)
        vary = pitch_shift(sound, factor=factor)
        vary.set_volume(volume)
        vary.play()
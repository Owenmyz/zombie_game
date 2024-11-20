# zombies/fast_zombie.py

from .zombie import Zombie

class FastZombie(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, size=30, color=(0, 255, 0), health=20, speed=2)
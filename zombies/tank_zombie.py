# zombies/tank_zombie.py

from .zombie import Zombie

class TankZombie(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, size=50, color=(128, 0, 0), health=60, speed=0.5)
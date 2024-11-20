from .zombie import Zombie

class ExplodingZombie(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, size=40, color=(255, 128, 0), health=25, speed=1)

    def take_damage(self, amount):
        super().take_damage(amount)
        if not self.active:
            self.explode()

    def explode(self):
        # Logic for explosion effect
        print("ExplodingZombie exploded!")
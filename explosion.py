import pygame

class Explosion:
    def __init__(self, x, y, radius=50, duration=30):
        self.x = x
        self.y = y
        self.radius = radius
        self.duration = duration  # How long the explosion lasts in frames
        self.active = True

    def update(self):
        # Decrease the duration each frame
        self.duration -= 1
        if self.duration <= 0:
            self.active = False

    def draw(self, surface):
        # Draw the explosion effect (expanding circle)
        if self.active:
            pygame.draw.circle(surface, (255, 100, 0), (self.x, self.y), self.radius)
            pygame.draw.circle(surface, (255, 255, 0), (self.x, self.y), self.radius // 2)

    def check_zombie_in_range(self, zombie):
        # Check if a zombie is within the explosion radius
        distance = ((self.x - zombie.x) ** 2 + (self.y - zombie.y) ** 2) ** 0.5
        if distance < self.radius:
            return True
        return False
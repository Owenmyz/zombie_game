import pygame

class Gun:
    def __init__(self, name, bullet_speed, fire_rate, color=(255, 255, 255), gun_type="normal"):
        self.name = name
        self.bullet_speed = bullet_speed  # Speed of bullets fired by this gun
        self.fire_rate = fire_rate  # Time in milliseconds between shots
        self.color = color
        self.type = gun_type  # Type of gun: 'normal', 'rpg', 'shotgun'
        self.width = 10
        self.height = 10

    def draw(self, surface, x, y):
        pygame.draw.rect(surface, self.color, (x, y, self.width, self.height))
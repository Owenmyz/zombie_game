import pygame

class Zombie:
    def __init__(self, x, y, size=40, color=(0, 128, 0), health=30, speed=1):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.health = health
        self.speed = speed
        self.active = True

    def take_damage(self, amount):
        """Reduces the zombie's health and deactivates if health reaches zero."""
        self.health -= amount
        if self.health <= 0:
            self.active = False

    def move_towards_player(self, player_x, player_y, zombies):
        dx, dy = player_x - self.x, player_y - self.y
        distance = (dx**2 + dy**2) ** 0.5
        if distance != 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

    def check_collision_with_player(self, player_x, player_y, player_size):
        return (
            self.x < player_x + player_size and
            self.x + self.size > player_x and
            self.y < player_y + player_size and
            self.y + self.size > player_y
        )
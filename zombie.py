import pygame
import math

class Zombie:
    def __init__(self, x, y, size=40, speed=2, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color

    def move_towards_player(self, player_x, player_y, other_zombies):
        # Calculate the direction vector towards the player
        direction_x = player_x - self.x
        direction_y = player_y - self.y

        # Normalize the direction vector
        distance = math.hypot(direction_x, direction_y)
        if distance != 0:  # Avoid division by zero
            direction_x /= distance
            direction_y /= distance

        # Move the zombie towards the player
        new_x = self.x + direction_x * self.speed
        new_y = self.y + direction_y * self.speed

        # Check collision with other zombies
        if not self.check_collision_with_zombies(new_x, new_y, other_zombies):
            self.x = new_x
            self.y = new_y

    def check_collision_with_player(self, player_x, player_y, player_size):
        # Check if zombie collides with player
        return (
            self.x < player_x + player_size and
            self.x + self.size > player_x and
            self.y < player_y + player_size and
            self.y + self.size > player_y
        )

    def check_collision_with_zombies(self, new_x, new_y, other_zombies):
        # Check if zombie collides with another zombie
        for zombie in other_zombies:
            if zombie != self:
                if (
                    new_x < zombie.x + zombie.size and
                    new_x + self.size > zombie.x and
                    new_y < zombie.y + zombie.size and
                    new_y + self.size > zombie.y
                ):
                    return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
from .zombie import Zombie
import pygame
import math

class ExplodingZombie(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, size=40, color=(255, 128, 0), health=25, speed=1)
        self.explosion_radius = 50  # Radius of the explosion

    def explode(self, player, zombies):
        """Handle explosion effects on the player and nearby zombies."""
        print("ExplodingZombie exploded!")
        
        # Check for damage to the player
        distance_to_player = math.hypot(self.x - player.x, self.y - player.y)
        if distance_to_player <= self.explosion_radius:
            player.take_damage(20)  # Damage the player

        # Check for damage to nearby zombies
        for zombie in zombies[:]:  # Use a copy of the list to avoid modification during iteration
            if zombie != self:  # Skip the exploding zombie itself
                distance_to_zombie = math.hypot(self.x - zombie.x, self.y - zombie.y)
                if distance_to_zombie <= self.explosion_radius:
                    zombie.take_damage(15)  # Damage other zombies

    def take_damage(self, amount, player=None, zombies=None):
        """Reduces the zombie's health and triggers an explosion when health reaches zero."""
        self.health -= amount
        if self.health <= 0 and self.active:
            self.active = False  # Mark the zombie as inactive
            if player and zombies:
                self.explode(player, zombies)  # Trigger explosion when the zombie dies
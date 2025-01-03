import pygame
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y, speed=10, width=10, height=5, angle=0, color=(255, 255, 0), bullet_type="normal"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.bullet_type = bullet_type  # 'normal' or 'rpg'

        # Calculate direction from player to target
        direction_x = target_x - x
        direction_y = target_y - y
        distance = math.hypot(direction_x, direction_y)

        # Apply angle if any (for shotgun spread)
        angle_radians = math.radians(angle)
        direction_x = direction_x * math.cos(angle_radians) - direction_y * math.sin(angle_radians)
        direction_y = direction_x * math.sin(angle_radians) + direction_y * math.cos(angle_radians)

        if distance != 0:
            self.vel_x = (direction_x / distance) * speed
            self.vel_y = (direction_y / distance) * speed
        else:
            self.vel_x, self.vel_y = 0, 0

        self.active = True

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def check_off_screen(self, screen_width, screen_height):
        if self.x > screen_width or self.x < 0 or self.y > screen_height or self.y < 0:
            self.active = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def check_collision_with_zombie(self, zombie):
        if (
            self.x < zombie.x + zombie.size and
            self.x + self.width > zombie.x and
            self.y < zombie.y + zombie.size and
            self.y + self.height > zombie.y
        ):
            # If this is an RPG, trigger an explosion
            if self.bullet_type == "rpg":
                return "explode"  # Return special flag for RPG bullets
            return True
        return False
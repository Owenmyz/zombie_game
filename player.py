import pygame
from bullet import Bullet

class Player:
    def __init__(self, x, y, size, speed, color=(0, 128, 255)):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.bullets = []  # List to hold bullets fired by the player

    def move(self, keys, screen_width, screen_height, zombies):
        new_player_x = self.x
        new_player_y = self.y

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.y > 0:
            new_player_y -= self.speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.y < screen_height - self.size:
            new_player_y += self.speed
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.x > 0:
            new_player_x -= self.speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.x < screen_width - self.size:
            new_player_x += self.speed

        if not self.check_collision_with_zombies(new_player_x, new_player_y, zombies):
            self.x = new_player_x
            self.y = new_player_y

    def check_collision_with_zombies(self, new_x, new_y, zombies):
        for zombie in zombies:
            if (
                new_x < zombie.x + zombie.size and
                new_x + self.size > zombie.x and
                new_y < zombie.y + zombie.size and
                new_y + self.size > zombie.y
            ):
                return True
        return False

    def shoot(self, mouse_x, mouse_y):
        # Shoot towards the mouse
        bullet = Bullet(self.x + self.size // 2, self.y + self.size // 2, mouse_x, mouse_y)
        self.bullets.append(bullet)

    def update_bullets(self, screen_width, screen_height, zombies):
        for bullet in self.bullets[:]:
            bullet.move()
            bullet.check_off_screen(screen_width, screen_height)
            if not bullet.active:
                self.bullets.remove(bullet)
                continue

            for zombie in zombies:
                if bullet.check_collision_with_zombie(zombie):
                    zombies.remove(zombie)
                    self.bullets.remove(bullet)
                    break

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(surface)
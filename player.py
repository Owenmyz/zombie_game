import pygame
import math
from bullet import Bullet

class Player:
    def __init__(self, x, y, size, speed, gun, color=(0, 128, 255)):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.gun = gun  # This is the gun the player is using
        self.bullets = []  # List to hold bullets fired by the player
        self.last_shot_time = 0  # Time when the last shot was fired

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

    def shoot(self, mouse_x, mouse_y, current_time):
        # Only shoot if enough time has passed since the last shot
        if current_time - self.last_shot_time >= self.gun.fire_rate:
            if self.gun.type == 'shotgun':
                # Shoot 3 bullets in slightly different directions
                angles = [-15, 0, 15]  # Bullet spread
                for angle in angles:
                    self.fire_bullet(mouse_x, mouse_y, angle)
            elif self.gun.type == 'rpg':
                # Fire a single, powerful bullet
                self.fire_bullet(mouse_x, mouse_y, 0, bullet_speed=self.gun.bullet_speed * 0.7, bullet_size=(20, 10))
            else:
                # Normal single bullet
                self.fire_bullet(mouse_x, mouse_y)

            self.last_shot_time = current_time

    def fire_bullet(self, mouse_x, mouse_y, angle=0, bullet_speed=None, bullet_size=(10, 5)):
        # Create a bullet with a given angle, speed, and size
        if bullet_speed is None:
            bullet_speed = self.gun.bullet_speed

        bullet = Bullet(
            self.x + self.size // 2,
            self.y + self.size // 2,
            mouse_x,
            mouse_y,
            bullet_speed,
            width=bullet_size[0],
            height=bullet_size[1],
            angle=angle
        )
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

    def pick_up_gun(self, gun):
        # Replace the current gun with the new gun
        self.gun = gun

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(surface)
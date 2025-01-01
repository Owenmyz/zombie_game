import pygame
import math
from bullet import Bullet
from explosion import Explosion

class Player:
    def __init__(self, x, y, size, speed, gun, color=(0, 128, 255), health=100):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.gun = gun
        self.health = health  # Player's health
        self.bullets = []
        self.explosions = []
        self.last_shot_time = 0

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

        # Check for collisions and take damage if necessary
        if self.check_collision_with_zombies(new_player_x, new_player_y, zombies):
            self.take_damage(10)  # Reduce health if colliding with a zombie
        else:
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

    def take_damage(self, amount):
        """Reduces the player's health."""
        self.health -= amount
        if self.health <= 0:
            print("Game Over! Player has died.")
            self.health = 0  # Ensures health doesn't go negative

    def draw_health(self, surface):
        """Draws the player's health bar."""
        pygame.draw.rect(surface, (255, 0, 0), (10, 10, 100, 10))  # Background bar
        pygame.draw.rect(surface, (0, 255, 0), (10, 10, self.health, 10))  # Health bar

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
        self.draw_health(surface)  # Draw health bar

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(surface)

        # Draw explosions
        for explosion in self.explosions:
            explosion.draw(surface)

    def update_bullets(self, screen_width, screen_height, zombies):
        for bullet in self.bullets[:]:
            bullet.move()
            bullet.check_off_screen(screen_width, screen_height)
            if not bullet.active:
                self.bullets.remove(bullet)
                continue

            for zombie in zombies[:]:
                collision = bullet.check_collision_with_zombie(zombie)
                if collision:
                    if isinstance(zombie, ExplodingZombie):  # Handle exploding zombie
                        zombie.take_damage(15, player=self, zombies=zombies, surface=self.screen)
                    else:
                        zombie.take_damage(15)  # Normal zombie takes damage
                    if not zombie.active:  # Remove zombie if health is zero
                        zombies.remove(zombie)
                    self.bullets.remove(bullet)
                    break

    def update_explosions(self, zombies):
        for explosion in self.explosions[:]:
            explosion.update()
            if not explosion.active:
                self.explosions.remove(explosion)
            else:
                # Damage zombies within the explosion's radius
                for zombie in zombies[:]:
                    if explosion.check_zombie_in_range(zombie):
                        zombies.remove(zombie)

    def pick_up_gun(self, gun):
        """Replace the player's current gun with a new one."""
        self.gun = gun

    def shoot(self, mouse_x, mouse_y, current_time):
        # Only shoot if enough time has passed since the last shot
        if current_time - self.last_shot_time >= self.gun.fire_rate:
            if self.gun.type == 'shotgun':
                # Shoot 3 bullets in slightly different directions
                angles = [-15, 0, 15]  # Bullet spread
                for angle in angles:
                    self.fire_bullet(mouse_x, mouse_y, angle)
            elif self.gun.type == 'rpg':
                # Fire a single RPG bullet
                self.fire_bullet(mouse_x, mouse_y, 0, bullet_speed=self.gun.bullet_speed * 0.7, bullet_size=(20, 10), bullet_type="rpg")
            else:
                # Normal single bullet
                self.fire_bullet(mouse_x, mouse_y)

            self.last_shot_time = current_time

    def fire_bullet(self, mouse_x, mouse_y, angle=0, bullet_speed=None, bullet_size=(10, 5), bullet_type="normal"):
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
            angle=angle,
            bullet_type=bullet_type
        )
        self.bullets.append(bullet)
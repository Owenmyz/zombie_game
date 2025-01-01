import pygame
import sys
import random
from zombies.fast_zombie import FastZombie
from zombies.tank_zombie import TankZombie
from zombies.exploding_zombie import ExplodingZombie
from player import Player
from zombies.zombie import Zombie
from gun import Gun
import time

# Initialize pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player, Zombies, and Guns")

# Define different guns
basic_gun = Gun("Basic Gun", bullet_speed=10, fire_rate=500, color=(255, 255, 0))
fast_gun = Gun("Fast Gun", bullet_speed=15, fire_rate=200, color=(0, 255, 0))

# Function to display the game-over screen
def display_game_over_screen(zombies_killed, time_survived):
    """Display the game-over screen."""
    screen.fill((0, 0, 0))  # Black background

    # Display "Game Over" text
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))

    # Display stats
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Zombies Killed: {zombies_killed}", True, (255, 255, 255))
    time_text = font.render(f"Time Survived: {time_survived:.2f} seconds", True, (255, 255, 255))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 + 40))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 80))

    pygame.display.flip()

    # Wait for the player to restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    return "restart"
                elif event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    sys.exit()

# Main game loop
def game_loop():
    # Initialize game variables
    player = Player(x=WIDTH // 2 - 25, y=HEIGHT // 2 - 25, size=50, speed=5, gun=basic_gun)
    zombies = []
    guns = []
    zombies_killed = 0
    start_time = time.time()
    zombie_spawn_delay = 3000
    last_zombie_spawn_time = pygame.time.get_ticks()
    gun_spawn_delay = 30000
    last_gun_spawn_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((0, 0, 0))  # Fill screen with black

        # Check if the player is dead
        if player.health <= 0:
            time_survived = time.time() - start_time
            return zombies_killed, time_survived  # Exit the game loop and return stats

        # Get the current time
        current_time = pygame.time.get_ticks()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                player.shoot(mouse_x, mouse_y, current_time)

        # Get key input
        keys = pygame.key.get_pressed()
        player.move(keys, WIDTH, HEIGHT, zombies)

        # Update bullets and check for collisions
        player.update_bullets(WIDTH, HEIGHT, zombies)
        player.update_explosions(zombies)

        # Draw player, health bar, and other elements
        player.draw(screen)

        # Spawn a new zombie every few seconds
        if current_time - last_zombie_spawn_time >= zombie_spawn_delay:
            spawn_x, spawn_y = random.choice([(0, 0), (WIDTH - 40, 0), (0, HEIGHT - 40), (WIDTH - 40, HEIGHT - 40)])
            zombie_type = random.choice([Zombie, FastZombie, TankZombie, ExplodingZombie])
            new_zombie = zombie_type(spawn_x, spawn_y)
            zombies.append(new_zombie)
            last_zombie_spawn_time = current_time

        # Spawn a new gun every 30 seconds
        if current_time - last_gun_spawn_time >= gun_spawn_delay:
            gun_types = [
                Gun("Random Gun", bullet_speed=random.randint(10, 20), fire_rate=random.randint(200, 700), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                Gun("Shotgun", bullet_speed=10, fire_rate=800, color=(255, 0, 0), gun_type="shotgun"),
                Gun("RPG", bullet_speed=8, fire_rate=1000, color=(0, 0, 255), gun_type="rpg")
            ]
            random_gun = random.choice(gun_types)
            gun_x = random.randint(50, WIDTH - 50)
            gun_y = random.randint(50, HEIGHT - 50)
            guns.append({"gun": random_gun, "x": gun_x, "y": gun_y})
            last_gun_spawn_time = current_time

# Move and draw zombies
    for zombie in zombies[:]:
        if not zombie.check_collision_with_player(player.x, player.y, player.size):
            zombie.move_towards_player(player.x, player.y, zombies)

        # Draw the zombie
        zombie.draw(screen)

        # If the zombie is inactive, handle explosions for ExplodingZombie
        if isinstance(zombie, ExplodingZombie) and not zombie.active:
            zombie.explode(player, zombies)
            zombies.remove(zombie)  # Remove exploded zombie from the list

    # Check for gun pickups and draw them
    for gun_pickup in guns[:]:
        gun_pickup_obj = gun_pickup["gun"]
        gun_rect = pygame.Rect(gun_pickup["x"], gun_pickup["y"], 20, 10)
        pygame.draw.rect(screen, gun_pickup_obj.color, gun_rect)
        player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
        if player_rect.colliderect(gun_rect):
            player.pick_up_gun(gun_pickup_obj)
            guns.remove(gun_pickup)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Game loop with restart functionality
while True:
    # Run the game and get stats when it ends
    zombies_killed, time_survived = game_loop()

    # Display the game-over screen
    action = display_game_over_screen(zombies_killed, time_survived)

    # Restart or quit based on player's choice
    if action == "restart":
        continue
    else:
        break

# Properly quit Pygame
pygame.quit()
sys.exit()
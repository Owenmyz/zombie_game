import pygame
import sys
import random
from player import Player
from zombie import Zombie
from gun import Gun

# Initialize pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player, Zombies, and Guns")

# Define different guns
basic_gun = Gun("Basic Gun", bullet_speed=10, fire_rate=500, color=(255, 255, 0))
fast_gun = Gun("Fast Gun", bullet_speed=15, fire_rate=200, color=(0, 255, 0))

# Set up the player
player = Player(x=WIDTH // 2 - 25, y=HEIGHT // 2 - 25, size=50, speed=5, gun=basic_gun)

# Initial zombies list
zombies = [
    Zombie(0, 0),  # Top-left corner
    Zombie(WIDTH - 40, 0),  # Top-right corner
    Zombie(0, HEIGHT - 40),  # Bottom-left corner
    Zombie(WIDTH - 40, HEIGHT - 40)  # Bottom-right corner
]

# Gun pickups (start with no guns)
guns = []

# Variables for zombie spawning
zombie_spawn_delay = 3000  # Time between spawns (in milliseconds)
last_zombie_spawn_time = pygame.time.get_ticks()  # Time when the last zombie was spawned

# Variables for gun spawning
gun_spawn_delay = 30000  # Time between gun spawns (30 seconds)
last_gun_spawn_time = pygame.time.get_ticks()  # Time when the last gun was spawned

# Initialize clock for frame rate control
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Fill screen with black

    # Get the current time
    current_time = pygame.time.get_ticks()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # End game loop

        # Handle shooting with mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player.shoot(mouse_x, mouse_y, current_time)

    # Get key input
    keys = pygame.key.get_pressed()

    # Move player
    player.move(keys, WIDTH, HEIGHT, zombies)

    # Update bullets and check for collisions
    player.update_bullets(WIDTH, HEIGHT, zombies)

    # Spawn a new zombie every few seconds
    if current_time - last_zombie_spawn_time >= zombie_spawn_delay:
        # Randomly choose one of the corners to spawn the zombie
        spawn_x, spawn_y = random.choice([(0, 0), (WIDTH - 40, 0), (0, HEIGHT - 40), (WIDTH - 40, HEIGHT - 40)])
        new_zombie = Zombie(spawn_x, spawn_y)
        zombies.append(new_zombie)
        last_zombie_spawn_time = current_time  # Reset the last spawn time

    # In the gun spawn section, add different gun types
    if current_time - last_gun_spawn_time >= gun_spawn_delay:
        gun_types = [
            Gun("Random Gun", bullet_speed=random.randint(10, 20), fire_rate=random.randint(200, 700), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            Gun("Shotgun", bullet_speed=10, fire_rate=800, color=(255, 0, 0), gun_type="shotgun"),
            Gun("RPG", bullet_speed=8, fire_rate=1000, color=(0, 0, 255), gun_type="rpg")
        ]
        random_gun = random.choice(gun_types)

        # Randomly place the gun on the screen
        gun_x = random.randint(50, WIDTH - 50)
        gun_y = random.randint(50, HEIGHT - 50)

        # Add the new gun to the guns list
        guns.append({"gun": random_gun, "x": gun_x, "y": gun_y})

        # Reset the last gun spawn time
        last_gun_spawn_time = current_time

    # Move and draw zombies
    for zombie in zombies:
        if not zombie.check_collision_with_player(player.x, player.y, player.size):
            zombie.move_towards_player(player.x, player.y, zombies)
        zombie.draw(screen)

    # Draw and check gun pickups
    for gun_pickup in guns[:]:
        gun_pickup_obj = gun_pickup["gun"]
        gun_rect = pygame.Rect(gun_pickup["x"], gun_pickup["y"], 20, 10)
        pygame.draw.rect(screen, gun_pickup_obj.color, gun_rect)

        print(f"Drawing gun at ({gun_pickup['x']}, {gun_pickup['y']})")  # Debugging print statement

        # Check if player is picking up the gun
        player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
        if player_rect.colliderect(gun_rect):
            player.pick_up_gun(gun_pickup_obj)
            print(f"Player picked up gun: {gun_pickup_obj.name}")  # Debugging pickup message
            guns.remove(gun_pickup)  # Remove gun from the list once picked up

    # Draw the player and bullets
    player.draw(screen)

    # Update the display
    pygame.display.flip()

    # Frame rate (60 FPS)
    clock.tick(60)

# Properly quit Pygame after the loop ends
pygame.quit()
sys.exit()
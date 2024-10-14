import pygame
import sys
from player import Player
from zombie import Zombie

# Initialize pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player, Zombies, and Shooting")

# Set up the player
player = Player(x=WIDTH // 2 - 25, y=HEIGHT // 2 - 25, size=50, speed=5)

# Spawn zombies at the corners
zombies = [
    Zombie(0, 0),  # Top-left corner
    Zombie(WIDTH - 40, 0),  # Top-right corner
    Zombie(0, HEIGHT - 40),  # Bottom-left corner
    Zombie(WIDTH - 40, HEIGHT - 40)  # Bottom-right corner
]

# Initialize clock for frame rate control
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Fill screen with black

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # End game loop

        # Handle shooting with mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player.shoot(mouse_x, mouse_y)

    # Get key input
    keys = pygame.key.get_pressed()

    # Move player
    player.move(keys, WIDTH, HEIGHT, zombies)

    # Update bullets and check for collisions
    player.update_bullets(WIDTH, HEIGHT, zombies)

    # Move and draw zombies
    for zombie in zombies:
        if not zombie.check_collision_with_player(player.x, player.y, player.size):
            zombie.move_towards_player(player.x, player.y, zombies)
        zombie.draw(screen)

    # Draw the player and bullets
    player.draw(screen)

    # Update the display
    pygame.display.flip()

    # Frame rate (60 FPS)
    clock.tick(60)

# Properly quit Pygame after the loop ends
pygame.quit()
sys.exit()
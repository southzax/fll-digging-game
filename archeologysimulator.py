# Archeology Simulator - Main Game File
# by FLL Team "Ctrl + Alt + Defeat", Team 71061

import pygame

# Initialize pygame FIRST (before importing files that use pygame)
pygame.init()

# Now we can import our other files!
# We split our game into smaller files to stay organized.
# Each file has one job - this makes it easier to find things.
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_SPEED,
    PLAYER_SCALE,
    JUMP_HEIGHT,
    Y_GRAVITY,
    POPUP_DURATION,
)
from player import Man  # Our player character
from ui import (
    draw_bg,
    draw_text_box,
    dig,
    make_dig_hole,
    init_ui,
)  # Drawing and digging

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Archeology Simulator")
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

# Load images now that pygame is ready
init_ui()

# Create the player
player = Man(PLAYER_START_X, PLAYER_START_Y, PLAYER_SCALE, PLAYER_SPEED, screen)

# Game state
run = True
moving_left = False
moving_right = False
jumping = False
Y_VELOCITY = JUMP_HEIGHT
popup_text = None
popup_timer = 0
popup_rarity = "common"  # Track rarity for border color

# Main game loop
while run:
    clock.tick(FPS)
    draw_bg(screen)

    # Handle events (keyboard, quit, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                make_dig_hole(player.rect.centerx, player.rect.bottom)
                artifact, rarity = dig()
                if artifact is not None:
                    popup_text = f"You found a {artifact['name']}!"
                    popup_rarity = rarity
                    popup_timer = pygame.time.get_ticks()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    # Show popup if we found something
    current_time = pygame.time.get_ticks()
    if popup_text:
        if current_time - popup_timer < POPUP_DURATION:
            draw_text_box(
                screen, popup_text, font, SCREEN_WIDTH, SCREEN_HEIGHT, popup_rarity
            )
        else:
            popup_text = None

    # Update player
    player.move(moving_left, moving_right)

    # Handle jumping (not used yet, but ready!)
    if jumping:
        player.rect.y -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT

    player.draw()
    pygame.display.update()

pygame.quit()

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
    DIG_COOLDOWN,
    BLACK,
    WHITE,
    GREEN,
    LIGHT_GREEN,
    STATE_MENU,
    STATE_PLAYING,
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
title_font = pygame.font.SysFont(None, 60)
clock = pygame.time.Clock()

# Load images now that pygame is ready
init_ui()

# Create the player
player = Man(PLAYER_START_X, PLAYER_START_Y, PLAYER_SCALE, PLAYER_SPEED, screen)

# Game state
run = True
game_state = STATE_MENU  # Start on menu screen!
moving_left = False
moving_right = False
jumping = False
Y_VELOCITY = JUMP_HEIGHT
popup_text = None
popup_timer = 0
last_dig_time = 0  # Track when we last dug

# Button settings
button_width = 200
button_height = 60
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = SCREEN_HEIGHT // 2

# Main game loop
while run:
    clock.tick(FPS)

    # Get mouse position for button hover effect
    mouse_pos = pygame.mouse.get_pos()

    # Handle events (keyboard, quit, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                current = pygame.time.get_ticks()
                if current - last_dig_time >= DIG_COOLDOWN:
                    last_dig_time = current

        # Menu screen events
        if game_state == STATE_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if Start button was clicked
                if (
                    button_x <= mouse_pos[0] <= button_x + button_width
                    and button_y <= mouse_pos[1] <= button_y + button_height
                ):
                    game_state = STATE_PLAYING

        # Playing screen events
        elif game_state == STATE_PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_SPACE:
                    make_dig_hole(player.rect.centerx, player.rect.bottom)
                    artifact = dig()
                    if artifact is not None:
                        popup_text = f"You found a {artifact['name']}!"
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
            draw_text_box(screen, popup_text, font, SCREEN_WIDTH, SCREEN_HEIGHT)
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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False

    # Draw based on game state
    if game_state == STATE_MENU:
        # Draw menu screen
        screen.fill(BLACK)

        # Draw title
        title = title_font.render("Archeology Simulator", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title, title_rect)

        # Draw Start button (green, lighter when hovered)
        button_hovered = (
            button_x <= mouse_pos[0] <= button_x + button_width
            and button_y <= mouse_pos[1] <= button_y + button_height
        )
        button_color = LIGHT_GREEN if button_hovered else GREEN
        pygame.draw.rect(
            screen, button_color, (button_x, button_y, button_width, button_height)
        )
        pygame.draw.rect(
            screen, WHITE, (button_x, button_y, button_width, button_height), 3
        )

        # Button text
        start_text = font.render("START", True, WHITE)
        start_rect = start_text.get_rect(
            center=(button_x + button_width // 2, button_y + button_height // 2)
        )
        screen.blit(start_text, start_rect)

    elif game_state == STATE_PLAYING:
        draw_bg(screen)

        # Show popup if we found something
        current_time = pygame.time.get_ticks()
        if popup_text:
            if current_time - popup_timer < POPUP_DURATION:
                draw_text_box(screen, popup_text, font, SCREEN_WIDTH, SCREEN_HEIGHT)
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

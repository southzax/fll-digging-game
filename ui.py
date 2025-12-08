# ui.py - User interface stuff (drawing backgrounds, text boxes, etc.)
# Functions for drawing things on screen that aren't the player.

import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GRAY, DARK_GRAY

# Colors for different rarity levels
GOLD = (255, 215, 0)
BLUE = (100, 149, 237)
BROWN = (139, 90, 43)
from artifacts import Artifacts

# These get set up by init_ui() after pygame is ready
BGT = None
ground_layer = None


def init_ui():
    """Call this after pygame.init() to load images."""
    global BGT, ground_layer
    BG = pygame.image.load("img/background.png")
    BGT = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ground_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)


def draw_bg(screen):
    """Draw the background and any dig holes."""
    screen.blit(BGT, (0, 0))
    screen.blit(ground_layer, (0, 0))


def draw_text_box(screen, text, font, width, height, rarity="common"):
    """Draw a popup box with text in it. Border color shows rarity!"""
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(100)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # Pick border color based on rarity
    if rarity == "legendary":
        border_color = GOLD
    elif rarity == "rare":
        border_color = BLUE
    else:
        border_color = BROWN

    box_width = 350
    box_height = 150
    box_x = (width - box_width) // 2
    box_y = (height - box_height) // 2
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, border_color, (box_x, box_y, box_width, box_height), 6)

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)


def dig():
    """Try to dig up an artifact! Returns (artifact, rarity) or (None, None) if you just got a rock."""
    find = random.random()
    if find < 0.01:
        print("legendary!")
        rarity = "legendary"
    elif find < 0.05:
        print("rare!")
        rarity = "rare"
    elif find < 0.20:
        print("common")
        rarity = "common"
    else:
        print("I got a rock")
        return None, None

    return random.choice(Artifacts[rarity]), rarity


def make_dig_hole(x, y):
    """Draw a dig hole at the given position."""
    pygame.draw.circle(ground_layer, (0, 0, 0, 200), (x, y), 20)

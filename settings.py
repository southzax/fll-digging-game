# settings.py - All the numbers and settings for our game live here!
# Change these to tweak how the game feels.

import pygame

pygame.init()

# Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# How fast the game runs (frames per second)
FPS = 60

# Player settings
PLAYER_START_X = 200
PLAYER_START_Y = 400
PLAYER_SPEED = 5
PLAYER_SCALE = 1

# Jump physics (not used yet, but ready for later!)
Y_GRAVITY = 1
JUMP_HEIGHT = 20

# How long popups stay on screen (in milliseconds)
# 1000 milliseconds = 1 second
POPUP_DURATION = 2000

# Colors (Red, Green, Blue) - values from 0 to 255
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

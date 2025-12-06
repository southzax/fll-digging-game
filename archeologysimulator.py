import pygame
import random

pygame.init()

#Position of player
Y_position = 400
X_position = 200

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Archeology Simulator")

font = pygame.font.SysFont(None, 40)

clock = pygame.time.Clock()
FPS = 60

moving_left = False
moving_right = False

BG = pygame.image.load("img/background.png")
BGT = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
ground_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

def draw_bg():
    screen.blit(BGT, (0,0))
    screen.blit(ground_layer,(0,0))

jumping = False

Y_GRAVITY = 1
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT

Artifacts = {
    "legendary": [
        {
            "name": "Artifacts L1",
            "description": "Here is text about Legendary Artifact L1",
            "image": "Image Goes HERE!"
        },
        {
            "name": "Artifacts L2",
            "description": "Here is text about Legendary Artifact L2",
            "image": "Image Goes HERE!"
        },
        {
            "name": "Artifacts L3",
            "description": "Here is text about Legendary Artifact L3",
            "image": "Image Goes HERE!"
        },
        {
            "name": "Artifacts L4",
            "description": "Here is text about Legendary Artifact L4",
            "image": "Image Goes HERE!"
        },
    ],
    "rare": [
        {
            "name": "Artifacts R1",
            "description": "Here is text about Rares Artifact R1",
            "image": "Image Goes HERE!"
        },
        {
            "name": "Artifacts R2",
            "description": "Here is text about Rare Artifact R2",
            "image": "Image Goes HERE!"
        },
        {
            "name": "Artifacts R3",
            "description": "Here is text about Rare Artifact R3",
            "image": "Image Goes HERE!"
        },
        {
            "name": "Artifacts R4",
            "description": "Here is text about Rare Artifact R4",
            "image": "Image Goes HERE!"
        },
    ],
    "common": [
        {
            "name": "Artifacts C1",
            "description": "Here is text about Common Artifact C1",
            "image": "Image Goes HERE!"
        },
        {
            "name": "Artifacts C2",
            "description": "Here is text about Common Artifact C2",
            "image": "Image Goes HERE!"
        },
        {
            "name": "Artifacts C3",
            "description": "Here is text about Common Artifact C3",
            "image": "Image Goes HERE!"
        },
        {
            "name": "Artifacts C4",
            "description": "Here is text about Common Artifact C4",
            "image": "Image Goes HERE!"
        },
    ]
}


class Man(pygame.sprite.Sprite):

    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.flip = False
        img = pygame.image.load('img/player/MAN.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.speed
            #self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            #self.flip = False
            self.direction = 1

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



player = Man(X_position, Y_position, 1, 5)

run = True

def dig():
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
        return None

    return random.choice(Artifacts[rarity])

def draw_text_box(screen, text, font, width, height):
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(100)
    overlay.fill((0, 0, 0,))
    screen.blit(overlay, (0, 0))

    box_width = 300
    box_height = 150
    box_x = (width - box_width) // 2
    box_y = (height - box_height) // 2
    pygame.draw.rect(screen, (200, 200, 200), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, (50,50,50), (box_x, box_y, box_width, box_height), 4)

    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center = (width//2, height//2))
    screen.blit(text_surface, text_rect)

popup_text = None
popup_timer = 0


while run:

    clock.tick(FPS)
    draw_bg()

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

        #kebord press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False
            #if event.key == pygame.K_w and not jumping:
                #jumping = True
            if event.key == pygame.K_SPACE:
                dig_position = (player.rect.centerx, player.rect.bottom)
                pygame.draw.circle(ground_layer, (0, 0, 0, 200), dig_position, 20)
                artifact = dig()
                if artifact is not None:
                    popup_text = f"You found a {artifact['name']}\n{artifact['description']}!"
                    popup_timer = pygame.time.get_ticks()

        #keyboard reless
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    current_time = pygame.time.get_ticks()
    if popup_text:
        if current_time - popup_timer < 2000:
            draw_text_box(screen, popup_text, font, 300, 150)
        else:
            popup_text = None


    player.move(moving_left, moving_right)

    if jumping:
        player.rect.y -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT

    player.draw()

    pygame.display.update()

pygame.quit()

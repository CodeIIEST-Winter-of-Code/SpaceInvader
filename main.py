import random
import math
import pygame
from pygame import mixer

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))
# background sounds
mixer.music.load('sounds/background.wav')
mixer.music.play(-1)

# background image
background = pygame.image.load("img/background.png")
# set title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('img/gameicon.png')
pygame.display.set_icon(icon)

# enemy icon
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('img/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(100, 150))
    enemyX_change.append(1)
    enemyY_change.append(30)

# player (craft) icon and initial position
playerImg = pygame.image.load('img/player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# ready- you can't see bullet on the screen, if fired, state is fire

bulletImg = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7.5
bullet_state = "ready"

# blit(...) used to draw am item on the screen

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# collision logic
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    if distance < 27:
        return True
    else:
        return False

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

running = True
while running:
    # while is necessary so that the window keeps running otherwise it will stop abruptly after initial load
    screen.fill((128, 128, 128))  # filling screen with color in (R, G, B)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # pygame.QUIT is pressing the cross at the top-right
        if event.type == pygame.QUIT:
            running = False
            #  print("Quitting......")

        # checks if key has been pressed
        if event.type == pygame.KEYDOWN:
            # checks if key pressed is right or left
            if event.key == pygame.K_LEFT:
                playerX_change = -2.5  # reduction of x-axis value if left key pressed
            if event.key == pygame.K_RIGHT:
                playerX_change = 2.5  # increase of x-axis value if right key pressed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('sounds/laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # checks if key has been released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change

    # prevents craft from going off screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # prevents enemy from going off screen
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            break
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
            # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(100, 150)
            explosion_Sound = mixer.Sound('sounds/explosion.wav')
            explosion_Sound.play()
        enemyX[i] += enemyX_change[i]
        enemy(enemyX[i], enemyY[i], i)

        # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()  # compulsory for display to update

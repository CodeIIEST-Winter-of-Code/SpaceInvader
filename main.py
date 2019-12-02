import pygame

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# set title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('gameicon.png')
pygame.display.set_icon(icon)

# player (craft) icon and initial position
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# blit(...) used to draw am item on the screen


def player(x, y):
    screen.blit(playerImg, (x, y))


running = True
while running:
    # while is necessary so that the window keeps running otherwise it will stop abruptly after initial load
    screen.fill((128, 128, 128))  # filling screen with color in (R, G, B)

    for event in pygame.event.get():
        # pygame.QUIT is pressing the cross at the top-right
        if event.type == pygame.QUIT:
            running = False
            #  print("Quitting......")

        # checks if key has been pressed
        if event.type == pygame.KEYDOWN:
            # checks if key pressed is right or left
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3  # reduction of x-axis value if left key pressed
                print("Left arrow is pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3  # increase of x-axis value if right key pressed
                print("Right arrow is pressed")
        # checks if key has been released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print("Keystroke released")
    playerX += playerX_change

    # prevents craft from going off screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    player(playerX, playerY)
    pygame.display.update()  # compulsory for display to update

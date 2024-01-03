import math
import random

import pygame
from pygame import mixer

pygame.init()

#GameScreen
screen = pygame.display.set_mode((800, 600))

#SpaceBackground
background = pygame.image.load('background.png')

#GameName
pygame.display.set_caption("Alien Invasion")

#Spaceship
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

#Alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(50, 150))
    alienX_change.append(2)
    alienY_change.append(10)

#Laserbeam

beamImg = pygame.image.load('beam.png')
beamX = 0
beamY = 480
beamX_change = 0
beamY_change = 10
beam_state = "ready"

#Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

#GameOver
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_beam(x, y):
    global beam_state
    beam_state = "fire"
    screen.blit(beamImg, (x + 16, y + 10))


def isCollision(alienX, alienY, beamX, beamY):
    distance = math.sqrt(math.pow(alienX - beamX, 2) + (math.pow(alienY - beamY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if beam_state is "ready":
                    beamX = playerX
                    fire_beam(beamX, beamY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

#AlienMovement
    for i in range(num_of_enemies):

        # Game Over
        if alienY[i] > 440:
            for j in range(num_of_enemies):
                alienY[j] = 2000
            game_over_text()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 4
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -4
            alienY[i] += alienY_change[i]

        # Collisions
        collision = isCollision(alienX[i], alienY[i], beamX, beamY)
        if collision:
            beamY = 480
            beam_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 736)
            alienY[i] = random.randint(50, 150)

        alien(alienX[i], alienY[i], i)

#BeamMovement
    if beamY <= 0:
        beamY = 480
        beam_state = "ready"

    if beam_state is "fire":
        fire_beam(beamX, beamY)
        beamY -= beamY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()

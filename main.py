import pygame as p
import random as r
import math as m
from pygame import mixer

# initialize pygame by init method
p.init()

# create the game window or screen
screen = p.display.set_mode((800, 600))

# background

background = p.image.load('background.png')

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon

p.display.set_caption("Space Invaders")

icon = p.image.load("ufo.png")
p.display.set_icon(icon)

# Player
playerimg = p.image.load("player.png")
playerimgX = 370
playerimgY = 480
playerimgX_chg = 0

# Enemy
enemyimg = []
enemyimgX = []
enemyimgY = []
enemyimgX_chg = []
enemyimgY_chg = []
noe = 6
for i in range(noe):
    enemyimg.append(p.image.load("enemy.png"))
    enemyimgX.append(r.randint(0, 736))
    enemyimgY.append(r.randint(50, 150))
    enemyimgX_chg.append(2)
    enemyimgY_chg.append(40)

# Bullet   Ready state means bullet is not on the screen and fire state means it's moving
bulletimg = p.image.load("bullet.png")
bulletimgX = 0
bulletimgY = 480
bulletimgX_chg = 0
bulletimgY_chg = 10
bullet_state = "ready"


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def isCollision(enemyimgX, enemyimgY, bulletimgX, bulletimgY):
    distance = m.sqrt(m.pow(enemyimgX - bulletimgX, 2) + m.pow(enemyimgY - bulletimgY, 2))
    if distance < 27:
        return True
    else:
        return False


score_value = 0
font = p.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# game over
game = p.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over():
    game_text = game.render("GAME OVER", True, (0, 0, 0))
    screen.blit(game_text, (200, 250))


# game loop
running = True

while running:

    screen.fill((0, 15, 90))
    # background image
    screen.blit(background, (0, 0))
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

        # check whether keystroke is pressed or not KEYDOWN IS USED WHEN WE PRESS CERTAIN KEY ON KEYBOARD
        if event.type == p.KEYDOWN:
            # print("Keystroke is pressed")
            if event.key == p.K_LEFT:
                playerimgX_chg = -0.6
            if event.key == p.K_RIGHT:
                playerimgX_chg = 0.6

            if event.key == p.K_SPACE:
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                if bullet_state is "ready":
                    bulletimgX = playerimgX
                    fire_bullet(bulletimgX, bulletimgY)
        # KEYUP IS USED WHEN WE RELEASE A KEYSTROKES
        if event.type == p.KEYUP:
            if event.key == p.K_LEFT or event.key == p.K_RIGHT:
                playerimgX_chg = 0

    # checking for boundaries of spaceships
    playerimgX += playerimgX_chg

    if playerimgX <= 0:
        playerimgX = 0

    elif playerimgX >= 736:
        playerimgX = 736

    # checking for enemy boundaries
    for i in range(noe):
        # game over part
        if enemyimgY[i] > 440:
            for j in range(noe):
                enemyimgY[j] = 2000
            game_over()
            break
        enemyimgX[i] += enemyimgX_chg[i]

        if enemyimgX[i] <= 0:
            enemyimgX_chg[i] = 2
            enemyimgY[i] += enemyimgY_chg[i]

        elif enemyimgX[i] >= 736:
            enemyimgX_chg[i] = -2
            enemyimgY[i] += enemyimgY_chg[i]

        collision = isCollision(enemyimgX[i], enemyimgY[i], bulletimgX, bulletimgY)
        if collision:
            exp_sound = mixer.Sound("explosion.wav")
            exp_sound.play()
            bulletimgY = 480
            bullet_state = "ready"
            score_value += 1
            # print(score)
            enemyimgX[i] = r.randint(0, 736)
            enemyimgY[i] = r.randint(50, 150)
        enemy(enemyimgX[i], enemyimgY[i], i)
    # bullet movement

    if bulletimgY <= 0:
        bulletimgY = 480
        bullet_state = "ready"

    if bullet_state is "Fire":
        fire_bullet(bulletimgX, bulletimgY)
        bulletimgY -= bulletimgY_chg

    player(playerimgX, playerimgY)
    show_score(textX, textY)

    p.display.update()

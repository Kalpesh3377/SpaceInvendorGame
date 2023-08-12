import pygame
import random
import math
from pygame import mixer
# initialize the pygame
pygame.init()

# create the screen
screen=pygame.display.set_mode((800,600))

# title and icon
pygame.display.set_caption("Space Invader")
icon=pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
# score
score=0
font=pygame.font.Font('Coffee Extra.ttf',32)
textX=10
textY=10
# game over text
over_font=pygame.font.Font('Coffee Extra.ttf',64)
def showscore(x,y):
    score_show=font.render("Score :"+str(score),True,(255,255,255))
    screen.blit(score_show,(x,y))
def game_over_text():
    over=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over,(200,250))


# background
backImg=pygame.image.load("img.png")
# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)
# player
playerImg=pygame.image.load("arcade-game.png")
playerX=370
playerY=480
playerx_change=0
# enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyx_change=[]
enemyy_change=[]
number_of_enemy=5
for i in range(number_of_enemy):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyx_change.append(0.3)
    enemyy_change.append(40)
# bullet
bulletImg=pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletx_change=0
bullety_change=1
bullet_state="ready"

def player(x,y):
    screen.blit(playerImg,(x,y))
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))
def bulletfire(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance<27:
        return True
    else:
        return False
# game loop
running=True
while running:
    # background colour change
    screen.fill((0,0,0))
    screen.blit(backImg,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        # moving object if keystroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerx_change=-0.3
            if event.key==pygame.K_RIGHT:
                playerx_change = 0.3
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    bulletfire(bulletX,bulletY)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerx_change = 0

    playerX+=playerx_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
    # movement of enemys
    for i in range(number_of_enemy):
        # game over
        if enemyY[i]>440:
            for j in range(number_of_enemy):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i]+=enemyx_change[i]
        if enemyX[i]<=0:
            enemyx_change[i] = 0.3
            enemyY[i]+=enemyy_change[i]
        elif enemyX[i]>=736:
            enemyx_change[i]=-0.3
            enemyY[i]+=enemyy_change[i]

            # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i],i)

    # bullet movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"
    if bullet_state=="fire":
        bulletfire(bulletX,bulletY)
        bulletY-=bullety_change

    player(playerX,playerY)
    showscore(textX,textY)
    pygame.display.update()
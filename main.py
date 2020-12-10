import pygame
import random
import math

#Start pygame loop
pygame.init()

#Create Screen
screen = pygame.display.set_mode((800,600))
score = 0
score_font = pygame.font.Font('freesansbold.ttf',20)
scoreX = 0
scoreY = 10

def ShowScore(x,y):
    score_text = score_font.render("Score :" + str(score),True,(255,255,255))
    screen.blit(score_text,(x,y))

#Background
background = pygame.image.load('space.jpg')
background = pygame.transform.scale(background,(800,600))

#You Win Screen
youwin = pygame.image.load('1.jpg')
youwin = pygame.transform.scale(youwin,(800,600))

#Game Over Screen
gameover = pygame.image.load('gameover.jpg')
gameover = pygame.transform.scale(gameover,(800,600))


#Title
pygame.display.set_caption("Invader")
icon = pygame.image.load('space-invaders.png')

pygame.display.set_icon(icon)

#Player
playerImage = pygame.image.load('space-invaders.png')
playerX = 368
playerY = 520
playerX_change = 0
player_freeze = True

def player(Img,x,y):
    playerImg = pygame.transform.scale(Img,(50,50))
    screen.blit(playerImg,(x,y))

#Enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []

def createEnemy(enemyImage,enemyX,enemyY,enemyX_change,enemyNum):
    for i in range(enemyNum):
        enemyImage.append(pygame.image.load('planet.png'))
        enemyX.append(random.randint(10,74)*random.randint(1,10))
        enemyY.append(10)
        enemyX_change.append(2.5)

createEnemy(enemyImage,enemyX,enemyY,enemyX_change,random.randint(1,6))

def enemy(Img,x,y):
    enemyImg = pygame.transform.scale(Img,(50,50))
    screen.blit(enemyImg,(x,y))

#Bullet
bulletImage = pygame.image.load('fire.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = False

def bullet(Img,x,y):
    global bullet_state
    bullet_state = True
    bulletImg = pygame.transform.scale(Img,(15,50))
    screen.blit(bulletImg,(x + 17,y + 8))

def Collision(x1,y1,x2,y2,d):
    distance = math.sqrt(math.pow(x1-x2,2)+ math.pow(y1-y2,2))
    if distance<d:
        return True
    else:
        return False
#Game loop
running = True
while running:

    #Background
    screen.blit(background,(0,0))
    for event in pygame.event.get():
#Screen quiting
        if event.type == pygame.QUIT:
            running = False
#Keyboard Input
        if  event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 4
            elif event.key == pygame.K_RIGHT:
                playerX_change += 4
            if event.key == pygame.K_SPACE and bullet_state == False:
                bulletX = playerX
                bullet(bulletImage,bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change += 4
            elif event.key == pygame.K_RIGHT:
                playerX_change -=4

    if player_freeze:
        playerX += playerX_change
    if playerX > 740:
        playerX = 740
    elif playerX < 10:
        playerX = 10

    for i in range(len(enemyX)):
        collision_over = Collision(enemyX[i],enemyY[i],playerX,playerY,50)
        if collision_over:
            player_freeze = False
            screen.blit(gameover, (0, 0))
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] > 740:
            enemyX_change[i] = -2.5
            enemyY[i] += 40
            if i == len(enemyX)-1 and len(enemyX)<20 and score <= 1000:
                createEnemy(enemyImage,enemyX,enemyY,enemyX_change,random.randint(1,6))
                break
        elif enemyX[i] < 10:
            enemyX_change[i] = 2.5
            enemyY[i] += 40
        collision = Collision(enemyX[i],enemyY[i],bulletX,bulletY,27)
        if collision and bullet_state:
            bullet_state = False
            bulletY = 480
            score += 10
            print(score)
            del enemyX[i]
            del enemyY[i]
            del enemyImage[i]
            del enemyX_change[i]
            break
        enemy(enemyImage[i], enemyX[i], enemyY[i])


    if bullet_state:
        bullet(bulletImage,bulletX,bulletY)
        bulletY -= 8
        if bulletY <= 10:
            bullet_state = False
            bulletY = 480

    if len(enemyX) == 0 and score>=1000:
        screen.blit(youwin, (0, 0))
    if player_freeze:
        player(playerImage,playerX,playerY)
        ShowScore(scoreX,scoreY)
    pygame.display.update()

import pygame 
import random
import math
# initiate the pygame
pygame.init()

# create a window
window = pygame.display.set_mode((800,600))

# icon and title
pygame.display.set_caption('Space Invador')
icon = pygame.image.load('ufo-2.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('background.png')

# define player
playerimg = pygame.image.load('space-invaders.png')
playerx = 380
playery = 520
change = 0
def player():
    window.blit(playerimg,(playerx,playery))

# enemy
class enemy():
    enemyimg = pygame.image.load('space-ship.png')
    was_hit = False
    def __init__(self,x,y):
        self.enemyx = x
        self.enemyy = y
    def enemy_draw(self):
        window.blit(self.enemyimg,(self.enemyx,self.enemyy))

enemies =[]
temp =[]
change_enemy = 10 
rows, cols = (4, 8) 
y=0
for row in range(rows):
    x=64
    temp = []
    for col in range(cols):
        temp.append(enemy(x,y))
        x += 64
    y += 64
    enemies.append(temp)
    
# bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
y = 500
bullet_state = False
score = 0
def bullet(x):
    window.blit(bulletimg,(x+15,y))

# is collision
def isCollision(x,y,enemyx,enemyy):
    if math.sqrt(math.pow(x-enemyx,2)+math.pow(y-enemyy,2)) < 32:
        return True
    else:
        return False


def move_enemy():
    global change_enemy
    global rows,cols,enemies
    for row in range(rows):
        for col in range(cols):
            enemies[row][col].enemy_draw()
            if enemies[row][col].enemyx >= 0 and enemies[row][col].enemyx <= 736:
                enemies[row][col].enemyx += change_enemy

def move_enemies_down():
    global enemies,rows,cols
    for row in range(rows):
        for col in range(cols):
            enemies[row][col].enemyy += 10
# game loop
running = True
while running:
    window.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change = -10
            if event.key == pygame.K_RIGHT:
                change = 10
            if event.key == pygame.K_SPACE and  not bullet_state:
                x = playerx
                bullet_state = True
                bullet(x)
        if event.type == pygame.KEYUP:
            change = 0
    if playerx >= 0 and playerx <= 736:
        playerx += change
    elif playerx > 700:
        playerx = 736
    else:
        playerx = 0

    if enemies[0][0].enemyx-10 <= 0 or enemies[0][cols-1].enemyx+10 >= 736 :
        change_enemy = -change_enemy
        move_enemies_down()
    move_enemy()

    if y > 0 and bullet_state:
        y-=20
        bullet(x)
    else:
        bullet_state = False  
        y = 500


    # detect collision
    for row in range(rows):
        for col in range(cols):
            if not enemies[row][col].was_hit and isCollision(x,y,enemies[row][col].enemyx,enemies[row][col].enemyy):
                score += 1
                enemies[row][col].was_hit = True
                print(score)
                bullet_state = False  
                y = 500
                enemies[row][col].enemyimg=pygame.Surface((64,64), pygame.SRCALPHA)
                # enemies[row][col].enemyimg.fill((255,255,255,128))
    player()

    pygame.display.update()
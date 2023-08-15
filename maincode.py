import pygame
import random
import math
from pygame import mixer
 
pygame.init()                                 # initilizing

#.................DISPLAY............................................
screen = pygame.display.set_mode((800,600))   # window size

pygame.display.set_caption('SPACE INVADERS')  # main title
icon = pygame.image.load('spaceship.png')     #  icon or game logo
pygame.display.set_icon(icon)

background = pygame.image.load('background.jpg') # for backgound
background = pygame.transform.scale(background, (800, 600))
mixer.music.load("background_music.mp3")
mixer.music.play(-1)



#.................... player...........................................
playerImage=pygame.image.load('spaceship.png')# image loading

playerX=370                                   # player default position
playerY=480       

playerXchange=0                               # player changing position


def player(x,y):                              # player function for showing on screen
    screen.blit(playerImage,(x,y))

#......................enemy.........................................
enemyImage = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(0.3)
    enemyYchange.append(40)

def enemy(x,y,i):                        # enemy function for showing on screen
    screen.blit(enemyImage[i],(x,y))

#....................BULLET....................................................

bulletImage = pygame.image.load('bullet.png')
bulletX=0                                   # player default position
bulletY=480# or playerY

bulletXchange=0                               # player changing position
bulletYchange= 3
bullet_state="ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImage,(x+16,y+10))

def isCollision(enemyX,enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
#game over
over_font = pygame.font.Font('Rubber-Duck.ttf', 64)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
#...........................MAIN LOOOP........................................
running = True
while running:
    screen.fill((0, 0, 0))                           # background colour
    screen.blit(background, (0, 0))                  # background image ko dikhane ke liye

    for event in pygame.event.get():                 # close button ka use karne ke liye
        if event.type == pygame.QUIT:
            running=False
        
        if event.type == pygame.KEYDOWN:             # kebowrd ke button ka use karne ke liye
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerXchange = -0.5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerXchange = +0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX=playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerXchange = 0
    


    
    playerX += playerXchange                  # player ki boundary ko lock karne ke liye
    
    player(playerX,playerY)
    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736
    
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyXchange[i]

        enemy(enemyX[i],enemyY[i],i)
        if enemyX[i] <= 0:
            enemyXchange[i] = +0.6
            enemyY[i] += enemyYchange[i]
        elif enemyX[i] >=736:
            enemyXchange[i] = -0.6
            enemyY[i] += enemyYchange[i]
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY=480
            bullet_state='ready'
            score_value += 1
            enemyX[i]=random.randint(0,736)                             # enemy default position
            enemyY[i]=random.randint(50,150)
        
        
    
    if bulletY <=0:
        bulletY= 480
        bullet_state='ready'

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletYchange

    show_score(textX, testY)
    
    pygame.display.update()

import pygame
import sys
pygame.init()

SCREEN = pygame.display.set_mode((800,800)) # Größe des BIldschirms wird Eingestellt
CLOCK = pygame.time.Clock() # Die Variable Clock wird für die FPS definiert
pygame.display.set_caption("Cat run ")# Der Name des Spiels wird zu Cat run eingestellt
X_POSITION, Y_POSITION = 400, 660 # Die X Position wird auf 400 eingestellt und die Y auf 600

jumping = False # die Variable jumping wird am anfang auf false gestellt

Y_GRAVITY = 1
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT

STANDING_SURFACE = pygame.transform.scale(pygame.image.load("cat idle.png"), (48,74))
JUMPING_SURFACE = pygame.transform.scale(pygame.image.load("cat_jump.gif"), (68,94))
BACKGROUND = pygame.transform.scale(pygame.image.load("background.png"), (800,800))

cat_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_SPACE]:
        jumping = True              
    SCREEN.blit(BACKGROUND, (0, 0))
 
    if jumping:
        Y_POSITION -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
       
        cat_rect = JUMPING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(JUMPING_SURFACE, cat_rect)
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT
           
           
    else:
        cat_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(STANDING_SURFACE, cat_rect)


    pygame.display.update()
    CLOCK.tick(60)
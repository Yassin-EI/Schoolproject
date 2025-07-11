import pygame 

import math 

pygame.init() 

 

clock = pygame.time.Clock() 

FPS = 60 

 

SCREEN_WIDTH = 1500 

SCREEN_HEIGHT = 600 

WIDTH = 100 

HEIGHT = 100 

boden_height = 50 

 

 

#variablen 

obstacles = [] 

obstacle_timer = 0 

obstacle_interval = 1000 

speedineeedthis = 10 

# Player 

player = pygame.Rect(100, 300, 40, 40) 

gravity = 0 

on_ground = True 

 

 

#farben 

RED = (255, 0, 0) 

 

# Obstacles 

obstacles = [] 

SPAWN_TIMER = pygame.USEREVENT + 1 

pygame.time.set_timer(SPAWN_TIMER, 1500) 

 

#öffnen 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

pygame.display.set_caption("Infinite Scroll") 

 

#bild laden 

bg = pygame.transform.scale(pygame.image.load("Background.png"), (900, 600)) 

bg_width = bg.get_width() 

 

#definiere variable calculating... 

scroll = 0 

tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1 

 

 

#schleife 

run = True 

while run: 

 

    clock.tick(FPS) 

 

    # Obstacles movement 

    for ob in obstacles: 

        ob["rect"].x -= ob["speed"] 

    obstacles = [o for o in obstacles if o["rect"].x > -50] 

 

    # Collision 

    for ob in obstacles: 

        if player.colliderect(ob["rect"]): 

            print("Game Over") 

            run = False 

    

    #draw obstacle 

    for ob in obstacles: 

        pygame.draw.rect(screen, RED, ob["rect"]) 

 

    #scrolling background 

    for i in range(0, tiles): 

        screen.blit(bg, (i * bg_width + scroll,0)) 

 

    #scroll background 

    scroll -= 5 

 

    #reset scroll 

    if abs(scroll) > bg_width: 

        scroll = 0 

    #event run 

    for event in pygame.event.get(): 

        if event.type == pygame.QUIT: 

            run = False 

 

    pygame.display.update() 

 

pygame.quit() 
 
import pygame 

import random 

from obstacles import * 

from config import * 

 

# Initialize 

 

background = pygame.image.load("Background.png").convert() 

 

 

 

pygame.init() 

WIDTH, HEIGHT = 800, 400 

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 

pygame.display.set_caption("Jump & Run") 

clock = pygame.time.Clock() 

score = 0 

font = pygame.font.SysFont(None, 40)  # Default font, size 40 

game_over = False 

 

def _init_(self): 

    pygame.init 

    self.font = pygame.font.Font('arial.tts', 32) 

# Colors 

WHITE = (255, 255, 255) 

RED = (255, 0, 0) 

BLACK = (0, 0, 0) 

 

# Player 

player = pygame.Rect(100, 300, 40, 40) 

gravity = 0 

on_ground = True 

 

# Obstacles 

obstacles = [] 

SPAWN_TIMER = pygame.USEREVENT + 1 

pygame.time.set_timer(SPAWN_TIMER, 1500) 

 

Game_Over = False 

 

def draw_text(text, font, text_col, x, y): 

    img = font.render(text, True, text_col) 

    screen.blit(img, (x, y)) 

 

 

# Game loop 

running = True 

while running: 

    clock.tick(60) 

    screen.fill('Background.png') 

    score += 1 

 

 

    # Events 

    for event in pygame.event.get(): 

        if event.type == pygame.QUIT: 

            running = False 

 

        if event.type == SPAWN_TIMER: 

            speed = random.randint(5, 40)  # random speed 

            new_obstacle = {"rect": pygame.Rect(WIDTH, 320, 40, 40), "speed": speed} 

            obstacles.append(new_obstacle) 

 

    # Jump 

    keys = pygame.key.get_pressed() 

    if keys[pygame.K_SPACE] and on_ground: 

        gravity = -15 

        on_ground = False 

 

    # Gravity 

    gravity += 1 

    player.y += gravity 

    if player.y >= 300: 

        player.y = 300 

        gravity = 0 

        on_ground = True 

 

    # Obstacles movement 

    for obs in obstacles: 

        obs["rect"].x -= obs["speed"] 

    obstacles = [o for o in obstacles if o["rect"].x > -50] 

 

    # Collision 

    for obs in obstacles: 

        if player.colliderect(obs["rect"]): 

            print("Game Over") 

 

    # Draw 

    pygame.draw.rect(screen, WHITE, player) 

    for obs in obstacles: 

        pygame.draw.rect(screen, RED, obs["rect"]) 

 

    score_text = font.render(f"Score: {score}", True, WHITE) 

    screen.blit(score_text, (10, 10)) 

    pygame.display.flip() 

 

pygame.quit() 
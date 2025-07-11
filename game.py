import pygame 

import sqlite3 

import random 

 

# --------------call database-------------------------------------------------------------- 

 

score_place_names = ["First place", "second place", "third place", "fourth", "fifth"] 

 

def init_db(): 

    conn = sqlite3.connect("highscore.db") 

    c = conn.cursor() 

    c.execute(''' 

        CREATE TABLE IF NOT EXISTS highscores ( 

            player_name TEXT PRIMARY KEY, 

            score INTEGER NOT NULL 

        ) 

    ''') 

    for name in score_place_names: 

        c.execute('SELECT player_name FROM highscores WHERE player_name = ?', (name,)) 

        if not c.fetchone(): 

            c.execute('INSERT INTO highscores (player_name, score) VALUES (?, ?)', (name, 0)) 

    conn.commit() 

    return conn, c 

 

def get_all_scores(c): 

    c.execute('SELECT player_name, score FROM highscores') 

    results = c.fetchall() 

    sorted_results = sorted(results, key=lambda x: x[1], reverse=True) 

    while len(sorted_results) < 5: 

        sorted_results.append(("ScoreX", 0)) 

    return sorted_results[:5] 

 

def save_score_insert(conn, c, new_score): 

    scores = get_all_scores(c) 

    if new_score <= scores[-1][1]: 

        return 

    inserted = False 

    new_scores = [] 

    for pname, pscore in scores: 

        if not inserted and new_score > pscore: 

            new_scores.append(("Score1", new_score)) 

            inserted = True 

        if len(new_scores) < 5: 

            new_scores.append((pname, pscore)) 

    new_scores = new_scores[:5] 

    for i, (_, score_val) in enumerate(new_scores): 

        fixed_name = score_place_names[i] 

        c.execute('UPDATE highscores SET score = ? WHERE player_name = ?', (score_val, fixed_name)) 

    conn.commit() 

 

 

# -----------------time for the game baby-------------------------------------------------- 

 

# Initialize and variables on which my life depends on. Ily variables 

pygame.init() 

WIDTH, HEIGHT = 800, 400 

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 

pygame.display.set_caption("Jump & Run") 

clock = pygame.time.Clock() 

score = 0 

game_over = False 

show_gmover = False 

showing_highscores = False   

font = pygame.font.SysFont(None, 40) 

 

# load them pics 

background = pygame.transform.scale(pygame.image.load("background.png"), (800, 400)) 

STANDING_SURFACE = pygame.transform.scale(pygame.image.load("cat idle.png"), (53, 77)) 

JUMPING_SURFACE = pygame.transform.scale(pygame.image.load("cat_jump.gif"), (71, 97)) 

 

# Colors 

WHITE = (255, 255, 255) 

RED = (255, 0, 0) 

BLACK = (0, 0, 0) 

Green = (0, 255, 0) 

 

# cute cat logic and variables 

player = pygame.Rect(100, 300, 40, 40) 

gravity = 0 

on_ground = True 

jumping = False 

 

# evil red tomato-cubed Obstacles 

obstacles = [] 

SPAWN_TIMER = pygame.USEREVENT + 1 

pygame.time.set_timer(SPAWN_TIMER, 1500) 

 

def draw_text(text, font, text_col, x, y): 

    img = font.render(text, True, text_col) 

    screen.blit(img, (x, y)) 

 

# Game loop will go on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on 

running = True 

while running: 

    clock.tick(60) 

    screen.blit(background, (0, 0)) 

 

    # events that will happen (fun fact, this made me have a crashout) 

    for event in pygame.event.get(): 

        if event.type == pygame.QUIT: 

            running = False 

 

 

            # evil tomato spawner 

        if event.type == SPAWN_TIMER and not game_over: 

            speed = random.randint(5, 40) 

            new_obstacle = {"rect": pygame.Rect(WIDTH, 320, 40, 40), "speed": speed} 

            obstacles.append(new_obstacle) 

 

    keys = pygame.key.get_pressed() 

 

    # prepare to crown the winner 

    if keys[pygame.K_h] and game_over: 

        showing_highscores = True 

    else: 

        showing_highscores = False 

 

    # crown the first place, burn the second place and delete the third place (joke) 

    if showing_highscores: 

        screen.fill(WHITE) 

        draw_text("Highscores", font, BLACK, WIDTH // 2 - 80, 30) 

        show_gmover = False 

 

        conn, c = init_db() 

        highscores = get_all_scores(c) 

        conn.close() 

 

        for i, (name, score_val) in enumerate(highscores): 

            text = f"{i + 1}. {name}: {score_val}" 

            draw_text(text, font, BLACK, WIDTH // 2 - 100, 80 + i * 40) 

 

    # the logics and laws of this wonderful game 

    if not showing_highscores: 

        # hop and hop cute kitten 

        if keys[pygame.K_SPACE] and on_ground: 

            gravity = -15 

            on_ground = False 

            jumping = True 

 

        # Isaac Newton's laws of gravity modified by a divine being (me) 

        gravity += 1 

        player.y += gravity 

        if player.y >= 300: 

            player.y = 300 

            gravity = 0 

            on_ground = True 

            jumping = False 

 

        # evil tomatoes shall move 

        for obs in obstacles: 

            obs["rect"].x -= obs["speed"] 

        obstacles = [o for o in obstacles if o["rect"].x > -50] 

 

        # Cute kitten is struck by the evil tomatoe 

        for obs in obstacles: 

            if player.colliderect(obs["rect"]): 

                print("Game Over") 

                conn, c = init_db() 

                save_score_insert(conn, c, score) 

                conn.close() 

                game_over = True 

                show_gmover = True 

 

        # cute kitten did not succumb 

        if keys[pygame.K_e] and game_over: 

            game_over = False 

            score = 0 

            obstacles.clear() 

 

        # cute kitten succumbed 

        if game_over and show_gmover: 

            game_overtext = font.render("Game Over! press E to restart. Hold H to see highscore", True, Green) 

            screen.blit(game_overtext, (WIDTH // 2 - game_overtext.get_width() // 2, HEIGHT // 2)) 

        elif not game_over: 

            score += 1 

            SPAWN_TIMER = pygame.USEREVENT + 1 

 

        # create the cute kitten 

        if jumping: 

            cat_rect = JUMPING_SURFACE.get_rect(midbottom=(player.centerx, player.bottom)) 

            screen.blit(JUMPING_SURFACE, cat_rect) 

        else: 

            cat_rect = STANDING_SURFACE.get_rect(midbottom=(player.centerx, player.bottom)) 

            screen.blit(STANDING_SURFACE, cat_rect) 

 

        # create the evil tomatoes 

        for obs in obstacles: 

            pygame.draw.rect(screen, RED, obs["rect"]) 

 

    # show us the kitten's score 

    score_text = font.render(f"Score: {score}", True, WHITE) 

    screen.blit(score_text, (10, 10)) 

 

    pygame.display.flip() 

 

 

# the end 

pygame.quit() 
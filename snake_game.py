# importing libraries
import pygame
import time
import random

snake_speed = 15
action = False
# Window size
window_x = 720
window_y = 480

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Michael Snake')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# displaying Score function
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# Reset game variables
def reset_game():
    global snake_position, snake_body, fruit_position, fruit_spawn, direction, change_to, score
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                      random.randrange(1, (window_y//10)) * 10]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

# Game over function
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2, window_y/4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)

def show_menu(action):
    while True:
        game_window.fill(black)
        menu_font = pygame.font.SysFont('times new roman', 50)

        # Render menu options
        title_surface = menu_font.render('Snake Game', True, green)
        start_surface = menu_font.render('Press S to Start', True, white)
        quit_surface = menu_font.render('Press Q to Quit', True, white)

        # Set positions for the menu options
        title_rect = title_surface.get_rect(center=(window_x/2, window_y/4))
        start_rect = start_surface.get_rect(center=(window_x/2, window_y/2))
        quit_rect = quit_surface.get_rect(center=(window_x/2, window_y/2 + 50))

        # Blit the menu options onto the screen
        game_window.blit(title_surface, title_rect)
        game_window.blit(start_surface, start_rect)
        game_window.blit(quit_surface, quit_rect)

        # Adding a "Continue" section if the game is paused
        if action:
            ongoing_surface = menu_font.render('Press C to Continue', True, white)
            ongoing_rect = ongoing_surface.get_rect(center=(window_x/2, window_y/3 + 30))
            game_window.blit(ongoing_surface, ongoing_rect)

        pygame.display.flip()

        # Handle menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c and action:
                    return True

# Main Function
while True:
    if not action:
        action = show_menu(action)
        reset_game()

    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_SPACE:
                action = show_menu(action)

    # If two keys pressed simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                          random.randrange(1, (window_y//10)) * 10]
        
    fruit_spawn = True
    game_window.fill(black)
    
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
        action = False
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()
        action = False

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
            action = False
            
    # displaying score continuously
    show_score(1, white, 'times new roman', 20)

    pygame.display.update()

    fps.tick(snake_speed)

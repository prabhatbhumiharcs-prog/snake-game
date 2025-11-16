import pygame
import time
import random
from pygame.locals import *

pygame.init()

# Define colors
red = (255, 0, 0)
blue = (51, 153, 255)
# grey = (192, 192, 192)
black=(0,0,0)
green = (51, 102, 0)
yellow = (0, 255, 255)
dark_pink = (255, 105, 180)  # Darker pink for the head

win_width = 600
win_height = 400
window = pygame.display.set_mode((win_width, win_height))

snake_block = 10  # Size of each block (rectangular segment)
snake_speed = 15  # Speed of the snake

clock = pygame.time.Clock()

font_style = pygame.font.SysFont("calibri", 26)
score_font = pygame.font.SysFont("comicsansms", 30)

def user_score(score):
    number = score_font.render("Score: " + str(score), True, red)
    window.blit(number, [0, 0])

def game_snake(snake_block, snake_length_list):
   
    for segment in snake_length_list[:-1]:  # All segments except the head
        pygame.draw.rect(window, red, [segment[0], segment[1], snake_block, snake_block])
    
    
    head = snake_length_list[-1]  # Get the position of the head (last element)
    pygame.draw.circle(window, dark_pink, [head[0] + snake_block // 2, head[1] + snake_block // 2], snake_block // 2)

def message(msg):
    msg = font_style.render(msg, True, red)
    window.blit(msg, [win_width / 16, win_height / 3])

def game_loop():
    gameOver = False
    gameClose = False
    paused = False  # Variable to track pause state

    x1 = win_width / 2
    y1 = win_height / 2

    x1_change = 0
    y1_change = 0

    snake_length_list = []
    snake_length = 1

    foodx = round(random.randrange(0, win_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, win_height - snake_block) / 10.0) * 10.0

    while not gameOver:

        while gameClose:
            window.fill(black)
            message("You lost!! Press P to play again or Q to quit the game")
            user_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = True
                        gameClose = False
                    if event.key == pygame.K_p:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == K_DOWN:
                    x1_change = 0
                    y1_change = snake_block
                elif event.key == K_SPACE:  # Toggle pause when space is pressed
                    paused = not paused

        if paused:
            message("Game Paused! Press SPACE to continue")
            pygame.display.update()
            continue  # Skip the rest of the game loop to keep the game paused

        # Check for boundaries collision
        if x1 >= win_width or x1 < 0 or y1 >= win_height or y1 < 0:
            gameClose = True

        x1 += x1_change
        y1 += y1_change

        window.fill(black)

        # Draw the food as a circle
        pygame.draw.circle(window, yellow, [foodx + snake_block // 2, foody + snake_block // 2], snake_block // 2)

        snake_size = []
        snake_size.append(x1)
        snake_size.append(y1)
        snake_length_list.append(snake_size)
        if len(snake_length_list) > snake_length:
            del snake_length_list[0]

        # Check if the snake bites itself
        for segment in snake_length_list[:-1]:  # Exclude the head (last segment)
            if segment == snake_size:
                gameClose = True

        game_snake(snake_block, snake_length_list)
        user_score(snake_length - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, win_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, win_height - snake_block) / 10.0) * 10.0
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()

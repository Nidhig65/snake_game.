import pygame
import time
import random

snake_speed = 15

# Window size
window_x = 720
window_y = 480

# Defining colors
light_green = pygame.Color(144, 238, 144)  # Light green for the background
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)  # Snake color
dark_blue = pygame.Color(0, 0, 139)  # Dark blue for the food

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# Defining snake default position
snake_position = [100, 50]

# Defining first 4 blocks of snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

# Fruit positions
fruit_positions = [[random.randrange(1, (window_x // 10)) * 10,
                    random.randrange(1, (window_y // 10)) * 10] for _ in range(5)]
fruit_spawn = True

# Setting default snake direction towards right
direction = 'RIGHT'
change_to = direction

# Initial score
score = 0

# Displaying Score function
def show_score(choice, color, font, size):
    # Creating font object score_font
    score_font = pygame.font.SysFont(font, size)
    
    # Create the display surface object score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)
    
    # Create a rectangular object for the text surface object
    score_rect = score_surface.get_rect()
    
    # Displaying text
    game_window.blit(score_surface, score_rect)

# Game over function
def game_over():
    # Creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)
    
    # Creating a text surface on which text will be drawn
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    
    # Create a rectangular object for the text surface object
    game_over_rect = game_over_surface.get_rect()
    
    # Setting position of the text
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    
    # Blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    # After 2 seconds we will quit the program
    time.sleep(2)
    
    # Deactivating pygame library
    pygame.quit()
    
    # Quit the program
    quit()

# Main Function
while True:
    # Handling key events
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

    # If two keys pressed simultaneously we don't want the snake to move into two directions simultaneously
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

    # Snake body growing mechanism if fruits and snakes collide then scores will be incremented by 10
    snake_body.insert(0, list(snake_position))
    
    # Check for collision with any fruit
    for fruit_position in fruit_positions:
        if (snake_position[0] in range(fruit_position[0], fruit_position[0] + 40) and
            snake_position[1] in range(fruit_position[1], fruit_position[1] + 40)):
            score += 10
            fruit_positions.remove(fruit_position)
            # Spawn new fruit
            fruit_positions.append([random.randrange(1, (window_x // 10)) * 10,
                                    random.randrange(1, (window_y // 10)) * 10])
            break
    else:
        snake_body.pop()

    game_window.fill(light_green)  # Change background color

    # Draw the snake as circles
    for pos in snake_body:
        pygame.draw.circle(game_window, red, (pos[0] + 5, pos[1] + 5), 5)  # Radius of 5 for the circles
        
    # Draw each fruit in dark blue
    for fruit_position in fruit_positions:
        pygame.draw.rect(game_window, dark_blue, pygame.Rect(fruit_position[0], fruit_position[1], 15, 15))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # Displaying score continuously
    show_score(1, white, 'times new roman', 30)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second / Refresh Rate
    fps.tick(snake_speed)

import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Set up display dimensions
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))

# Set up title and icon
pygame.display.set_caption('Snake Game')
icon = pygame.image.load('snake_icon.jpg')
pygame.display.set_icon(icon)

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Set up fonts
font = pygame.font.SysFont(None, 35)

# Define clock for controlling game speed
clock = pygame.time.Clock()

# Function to display score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, [10, 10])

# Function to display game over message
def game_over_message(score):
    screen.fill(black)
    game_over_text = font.render(f"Game Over! Your Score: {score}", True, red)
    replay_text = font.render("Press R to play again or Q to quit", True, white)
    screen.blit(game_over_text, [display_width // 4, display_height // 3])
    screen.blit(replay_text, [display_width // 4, display_height // 2])
    pygame.display.flip()

# Function to generate a random apple position
def random_apple():
    return (random.randrange(0, display_width // 20) * 20, random.randrange(0, display_height // 20) * 20)

# Main game loop
def game_loop():
    # Initialize game variables
    snake = [(200, 200), (220, 200), (240, 200)]  # initial snake position
    apple_pos = random_apple()  # random initial apple position
    direction = 'right'  # initial direction
    score = 0
    game_over = False
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'down':
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction != 'up':
                    direction = 'down'
                elif event.key == pygame.K_LEFT and direction != 'right':
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    direction = 'right'

        # Update snake position based on direction
        head_x, head_y = snake[-1]
        if direction == 'up':
            new_head = (head_x, head_y - 20)
        elif direction == 'down':
            new_head = (head_x, head_y + 20)
        elif direction == 'left':
            new_head = (head_x - 20, head_y)
        elif direction == 'right':
            new_head = (head_x + 20, head_y)

        # Check for self-collision or wall collision
        if (new_head in snake or
            new_head[0] < 0 or new_head[0] >= display_width or
            new_head[1] < 0 or new_head[1] >= display_height):
            game_over_message(score)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game_loop()  # Restart the game
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
        
        # Check for collisions with apple
        if new_head == apple_pos:
            snake.append(new_head)
            apple_pos = random_apple()
            score += 1  # Increment score
        else:
            snake.append(new_head)
            snake.pop(0)

        # Draw everything
        screen.fill(black)
        for pos in snake:
            pygame.draw.rect(screen, white, (pos[0], pos[1], 20, 20))
        pygame.draw.rect(screen, red, (apple_pos[0], apple_pos[1], 20, 20))

        # Display the score
        display_score(score)

        # Update display
        pygame.display.flip()

        # Control game speed (lower time means faster speed)
        clock.tick(10)

# Start the game loop
game_loop()

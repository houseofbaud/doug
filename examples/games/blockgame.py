import pygame
import random

pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the width and height of the screen
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500
BLOCK_SIZE = 20
MARGIN = 5

# Create the screen
screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

# Set the title of the window
pygame.display.set_caption("Tetris")

# Create the grid
grid = []
for row in range(20):
    grid.append([])
    for column in range(10):
        grid[row].append(0)

# Define the shapes
shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6],
     [6, 6]]
]

# Define the colors
colors = [
    WHITE,
    RED,
    GREEN,
    BLUE,
    (255, 255, 0),
    (255, 0, 255)
]

# Define the current shape and its position
current_shape = random.choice(shapes)
current_shape_color = random.choice(colors)
current_shape_row = 0
current_shape_column = 3

# Define the clock
clock = pygame.time.Clock()

# Define the score
score = 0

# Define the font
font = pygame.font.SysFont(None, 25)

# Define the game over flag
game_over = False

# Define the function to draw the grid
def draw_grid():
    for row in range(20):
        for column in range(10):
            color = BLACK
            if grid[row][column] != 0:
                color = colors[grid[row][column] - 1]
            pygame.draw.rect(screen, color, [(MARGIN + BLOCK_SIZE) * column + MARGIN, (MARGIN + BLOCK_SIZE) * row + MARGIN, BLOCK_SIZE, BLOCK_SIZE])

# Define the function to draw the current shape
def draw_current_shape():
    for row in range(len(current_shape)):
        for column in range(len(current_shape[0])):
            if current_shape[row][column] != 0:
                pygame.draw.rect(screen, current_shape_color, [(MARGIN + BLOCK_SIZE) * (current_shape_column + column) + MARGIN, (MARGIN + BLOCK_SIZE) * (current_shape_row + row) + MARGIN, BLOCK_SIZE, BLOCK_SIZE])

# Define the function to move the current shape down
def move_down():
    global current_shape_row
    if can_move(current_shape, current_shape_row + 1, current_shape_column):
        current_shape_row += 1
    else:
        add_shape_to_grid()
        remove_completed_rows()
        new_shape()

# Define the function to move the current shape left
def move_left():
    global current_shape_column
    if can_move(current_shape, current_shape_row, current_shape_column - 1):
        current_shape_column -= 1

# Define the function to move the current shape right
def move_right():
    global current_shape_column
    if can_move(current_shape, current_shape_row, current_shape_column + 1):
        current_shape_column += 1

# Define the function to rotate the current shape
def rotate():
    global current_shape
    new_shape = []
    for column in range(len(current_shape[0])):
        new_row = []
        for row in range(len(current_shape) - 1, -1, -1):
            new_row.append(current_shape[row][column])
        new_shape.append(new_row)
    if can_move(new_shape, current_shape_row, current_shape_column):
        current_shape = new_shape

# Define the function to check if the current shape can move to the given position
def can_move(shape, row, column):
    for shape_row in range(len(shape)):
        for shape_column in range(len(shape[0])):
            if shape[shape_row][shape_column] != 0:
                if row + shape_row < 0 or row + shape_row >= 20 or column + shape_column < 0 or column + shape_column >= 10 or grid[row + shape_row][column + shape_column] != 0:
                    return False
    return True

# Define the function to add the current shape to the grid
def add_shape_to_grid():
    global grid, current_shape, current_shape_color, current_shape_row, current_shape_column, game_over
    for shape_row in range(len(current_shape)):
        for shape_column in range(len(current_shape[0])):
            if current_shape[shape_row][shape_column] != 0:
                if current_shape_row + shape_row < 0:
                    game_over = True
                else:
                    grid[current_shape_row + shape_row][current_shape_column + shape_column] = colors.index(current_shape_color) + 1
    current_shape = None

# Define the function to remove completed rows
def remove_completed_rows():
    global grid, score
    new_grid = []
    completed_rows = 0
    for row in range(len(grid)):
        if 0 not in grid[row]:
            completed_rows += 1
        else:
            new_grid.append(grid[row])
    score += completed_rows ** 2
    for i in range(completed_rows):
        new_grid.insert(0, [0] * 10)
    grid = new_grid

# Define the function to generate a new shape
def new_shape():
    global current_shape, current_shape_color, current_shape_row, current_shape_column
    current_shape = random.choice(shapes)
    current_shape_color = random.choice(colors)
    current_shape_row = 0
    current_shape_column = 3

# Main game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left()
            elif event.key == pygame.K_RIGHT:
                move_right()
            elif event.key == pygame.K_DOWN:
                move_down()
            elif event.key == pygame.K_UP:
                rotate()

    # Move the current shape down
    move_down()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the grid and the current shape
    draw_grid()
    if current_shape is not None:
        draw_current_shape()

    # Draw the score
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, [10, 10])

    # Update the screen
    pygame.display.update()

    # Set the frame rate
    clock.tick(10)

# Clean up
pygame.quit()

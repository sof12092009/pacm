import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 20
WHITE, BLACK, YELLOW, RED, BLUE, GREEN, ORANGE, GRAY = (255, 255, 255), (0, 0, 0), (255, 255, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 165, 0), (128, 128, 128)
COLORS = [WHITE, YELLOW, RED, BLUE, GREEN, ORANGE, GRAY]
WIDTH, HEIGHT = 400, 600

# Maze
maze = [
    "############################",
    "#oooooooooooooooooooooooooo#",
    "#o####o#####o########o####o#",
    "#o####o#####o##o#####o####o#",
    "#o####o#####o##o#####o####o#",
    "#oooooooooooooooooooooooooo#",
    "#o####o##o######o##o####ooo#",
    "#o####o##o######o##o####o###",
    "#oooooo##oooo##ooooo#oooooo#",
    "######o#####o##o#####o######",
    "######o#####o##o#####o######",
    "######o##oooooooo#oooooo####",
    "######o##o########o##o######",
    "######o##o########o##o######",
    "#oooooooooooo##oooooooooooo#",
    "#o####o#####o##o#####o####o#",
    "#o####o#####o##o#####o####o#",
    "#o####o##oooooooo#oooo##ooo#",
    "#o####o##o########o#########",
    "#oooooo##oooooooooo#########",
    "############################",
    "############################",
    "############################",
    "############################"
]
# Positions
pacman_pos = [1, 1]
ghosts = [
    {"pos": [12, 11], "color": RED, "direction": random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])},
    {"pos": [12, 12], "color": GREEN, "direction": random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])},
    {"pos": [11, 12], "color": ORANGE, "direction": random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])}
]
dot_positions = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == 'o']

# Directions
direction = [0, 0]

# Clock
clock = pygame.time.Clock()

# Score
score = 0

# Font
font = pygame.font.Font(None, 36)

# Screen dimensions
SCREEN_WIDTH = len(maze[0]) * GRID_SIZE
SCREEN_HEIGHT = len(maze) * GRID_SIZE + 100

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pacman')

# Pacman image
pacman_image = pygame.image.load('pacmen.png')
pacman_image = pygame.transform.scale(pacman_image, (GRID_SIZE, GRID_SIZE))

# Function to draw maze
def draw_maze():
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "#":
                pygame.draw.rect(screen, BLUE, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif cell == "o" and (x, y) in dot_positions:
                pygame.draw.circle(screen, WHITE, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), 3)

# Function to draw score
def draw_score(score):
    score_surface = font.render(f'Score: {score}', True, GRAY)
    score_rect = score_surface.get_rect()
    score_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

    background_rect = pygame.Rect(score_rect.left - 10, score_rect.top - 5, score_rect.width + 20, score_rect.height + 10)
    pygame.draw.rect(screen, YELLOW, background_rect)
    pygame.draw.rect(screen, BLACK, background_rect, 3)

    screen.blit(score_surface, score_rect)

# Function to move
def move(pos, direction):
    new_pos = [pos[0] + direction[0], pos[1] + direction[1]]
    if 0 <= new_pos[0] < len(maze[0]) and 0 <= new_pos[1] < len(maze) and maze[new_pos[1]][new_pos[0]] != "#":
        return new_pos
    return pos

# Function to check win
def check_win():
    return len(dot_positions) == 0

# Function to draw gradient background
def draw_gradient_background():
    for y in range(SCREEN_HEIGHT):
        r = int(255 * (1 - y / SCREEN_HEIGHT))  # Red (gradient up)
        g = int(255 * (y / SCREEN_HEIGHT))  # Green (gradient down)
        b = int(255 * (1 - abs(y / SCREEN_HEIGHT - 0.5) * 2))  # Blue (gradient towards middle)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

# Start screen
def start_screen():
    screen.fill(BLACK)

    circles = []
    for _ in range(100):
        radius = random.randint(5, 20)
        color = random.choice(COLORS)
        pos = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
        circles.append([pos, radius, color])

    title_text = font.render('PACMAN', True, YELLOW)
    start_text = font.render('Press SPACE to Start', True, WHITE)
    instruction_text = font.render('Press SPACE to Start', True, WHITE)

    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2 - 40))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 - instruction_text.get_height() // 2 + 40))

    while not pygame.key.get_pressed()[pygame.K_SPACE]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(BLACK)
        for circle in circles:
            pos, radius, color = circle
            pygame.draw.circle(screen, color, pos, radius)
            pos[0] += random.randint(-2, 2)
            pos[1] += random.randint(-2, 2)
            if pos[0] < 0 or pos[0] > SCREEN_WIDTH or pos[1] < 0 or pos[1] > SCREEN_HEIGHT:
                circles.remove(circle)

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2 - 40))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 - instruction_text.get_height() // 2 + 40))

        pygame.display.flip()
        clock.tick(30)

# Game over screen
def game_over_screen(message, score):
    draw_gradient_background()

    game_over_text = font.render(message, True, WHITE)
    score_text = font.render(f'Score: {score}', True, WHITE)
    restart_text = font.render('Press R to Restart', True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 20))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + 20))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 - restart_text.get_height() // 2 + 60))
    pygame.display.flip()


# Main game loop
def game():
    global pacman_pos, ghosts, direction, score, dot_positions
    pacman_pos = [1, 1]
    ghosts = [
        {"pos": [12, 11], "color": RED, "direction": random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])},
        {"pos": [12, 12], "color": GREEN, "direction": random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])},
        {"pos": [11, 12], "color": ORANGE, "direction": random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])}
    ]
    direction = [0, 0]
    score = 0
    dot_positions = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == 'o']

    game_over = False
    paused = False

    while not game_over:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = [-1, 0]
                if event.key == pygame.K_RIGHT:
                    direction = [1, 0]
                if event.key == pygame.K_UP:
                    direction = [0, -1]
                if event.key == pygame.K_DOWN:
                    direction = [0, 1]
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_s:
                    paused = not paused

        if not paused:
            pacman_pos = move(pacman_pos, direction)

        if (pacman_pos[0], pacman_pos[1]) in dot_positions:
            dot_positions.remove((pacman_pos[0], pacman_pos[1]))
            score += 10

        if check_win():
            game_over = True
            game_over_screen("Success!", score)
            return

        if not paused:
            for ghost in ghosts:
                ghost['pos'] = move(ghost['pos'], ghost['direction'])
                if random.random() < 0.2:
                    ghost['direction'] = random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])

        for ghost in ghosts:
            if ghost['pos'] == pacman_pos:
                game_over = True

        draw_maze()

        # Draw Pacman
        screen.blit(pacman_image, (pacman_pos[0] * GRID_SIZE, pacman_pos[1] * GRID_SIZE))

        # Draw ghosts
        for ghost in ghosts:
            pygame.draw.rect(screen, ghost['color'], pygame.Rect(ghost['pos'][0] * GRID_SIZE, ghost['pos'][1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        draw_score(score)

        pygame.display.flip()
        clock.tick(10)

# Main loop
running = True
while running:
    start_screen()
    start = False
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True

    if running:
        game()
        game_over_screen("Game Over", score)
        restart = False
        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    restart = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart = True

pygame.quit()


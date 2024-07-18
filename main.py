import pygame  # Импортируем библиотеку Pygame для создания игры
import random # Импортируем библиотеку random для генерации случайных чисел

# Initialize Pygame  # Инициализируем Pygame
pygame.init()

# Constants #Константы
GRID_SIZE = 35
WHITE, BLACK, YELLOW, RED, BLUE, GREEN, ORANGE, GRAY = (255, 255, 255), (0, 0, 0), (255, 255, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 165, 0), (128, 128, 128)
COLORS = [WHITE, YELLOW, RED, BLUE, GREEN, ORANGE, GRAY]
WIDTH, HEIGHT = 400, 600

# Maze лабиринт
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
pacman_pos = [1, 1] # Начальная позиция Пакмана в сетке (координаты x, y)
ghosts = [
    {"pos": [12, 11], "color": RED, "direction": random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])}, # Призрак 1: начальная позиция, цвет и случайное направление
    {"pos": [12, 12], "color": GREEN, "direction": random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])}, # Призрак 2: начальная позиция, цвет и случайное направление
    {"pos": [11, 12], "color": ORANGE, "direction": random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])} # Призрак 3: начальная позиция, цвет и случайное направление
]
# Генерация списка позиций точек (dot_positions) на основе лабиринта (maze)
dot_positions = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == 'o']
# Проходим по каждой строке (row) и каждому символу (cell) в строке лабиринта (maze)
# Если символ равен 'o' (точка), добавляем координаты (x, y) в список dot_positions


# Directions
direction = [0, 0]  # Начальное направление движения Пакмана (x, y). [0, 0] означает, что Пакман стоит на месте.

# Clock
clock = pygame.time.Clock()  # Создаем объект Clock для управления частотой обновления экрана.

# Score
score = 0  # Начальный счет игры.

# Font
font = pygame.font.Font(None, 36) # Создаем объект шрифта с размером 36. None означает использование шрифта по умолчанию.

# Screen dimensions
SCREEN_WIDTH = len(maze[0]) * GRID_SIZE  #Ширина экрана рассчитывается как количество столбцов в лабиринте, умноженное на размер клетки.
SCREEN_HEIGHT = len(maze) * GRID_SIZE + 100 # Высота экрана рассчитывается как количество строк в лабиринте, умноженное на размер клетки, плюс 100 пикселей для дополнительного пространства (например, для отображения счета).

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Создаем окно игры с заданными размерами.
pygame.display.set_caption('Pacman')  # Устанавливаем заголовок окна игры.

# Pacman image
pacman_image = pygame.image.load('pacmen.png')  # Загружаем изображение Пакмана из файла 'pacmen.png'.
pacman_image = pygame.transform.scale(pacman_image, (GRID_SIZE, GRID_SIZE))  # Масштабируем изображение Пакмана до размера клетки сетки.

# Ghost images
ghost_images = {
    RED: pygame.image.load('red_ghost.png'),  # Загружаем изображение красного призрака из файла 'red_ghost.png'.
    GREEN: pygame.image.load('green_ghost.png'),  # Загружаем изображение зеленого призрака из файла 'green_ghost.png'.
    ORANGE: pygame.image.load('orange_ghost.png')  # Загружаем изображение оранжевого призрака из файла 'orange_ghost.png'.
}
for color, image in ghost_images.items(): # Масштабируем каждое изображение призрака до размера клетки сетки.
    ghost_images[color] = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))  # Масштабируем изображение призрака до размера клетки сетки.

# Function to draw maze
def draw_maze():
    # Проходим по каждой строке (row) и каждому символу (cell) в строке лабиринта (maze)
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "#":
                # Если символ равен "#", рисуем прямоугольник (стену) синего цвета (BLUE)
                pygame.draw.rect(screen, BLUE, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif cell == "o" and (x, y) in dot_positions:
                # Если символ равен "o" и координаты (x, y) находятся в списке dot_positions, рисуем точку (dot)
                pygame.draw.circle(screen, WHITE, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), 3)
            # Рисуем белый круг (точку) в центре клетки сетки

# Function to draw score
def draw_score(score):

    # Создаем поверхность с текстом "Score: {score}" серого цвета (GRAY)
    score_surface = font.render(f'Score: {score}', True, GRAY)

    # Получаем прямоугольник (rect) для поверхности с текстом
    score_rect = score_surface.get_rect()

    # Устанавливаем позицию прямоугольника: центр по горизонтали и 30 пикселей от нижней границы экрана
    score_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

    # Создаем прямоугольник для фона текста, немного больше самого текста
    background_rect = pygame.Rect(score_rect.left - 10, score_rect.top - 5, score_rect.width + 20, score_rect.height + 10)

    # Рисуем желтый (YELLOW) прямоугольник для фона текста
    pygame.draw.rect(screen, YELLOW, background_rect)

    # Рисуем черную (BLACK) рамку вокруг желтого прямоугольника
    pygame.draw.rect(screen, BLACK, background_rect, 3)

    # Отображаем поверхность с текстом на экране в заданной позиции
    screen.blit(score_surface, score_rect)

# Function to move
def move(pos, direction):
    # Вычисляем новую позицию, добавляя направление к текущей позиции
    new_pos = [pos[0] + direction[0], pos[1] + direction[1]]

    # Проверяем, находится ли новая позиция внутри границ лабиринта и не является ли она стеной
    if 0 <= new_pos[0] < len(maze[0]) and 0 <= new_pos[1] < len(maze) and maze[new_pos[1]][new_pos[0]] != "#":

        # Если все условия выполнены, возвращаем новую позицию
        return new_pos

    # Если новая позиция невалидна (вне границ или стена), возвращаем текущую позицию
    return pos

# Function to check win
def check_win():
    return len(dot_positions) == 0 # Проверяем, пуст ли список dot_positions (все точки собраны)

# Function to draw gradient background
def draw_gradient_background():
    for y in range(SCREEN_HEIGHT):  # Проходим по каждой строке экрана по вертикали
        r = int(255 * (1 - y / SCREEN_HEIGHT))  # Red (gradient up) # Вычисляем значение красного цвета, уменьшающегося от 255 до 0 по мере движения вниз
        g = int(255 * (y / SCREEN_HEIGHT))  # Green (gradient down)   # Вычисляем значение зеленого цвета, увеличивающегося от 0 до 255 по мере движения вниз
        b = int(255 * (1 - abs(y / SCREEN_HEIGHT - 0.5) * 2))  # Blue (gradient towards middle)  # Вычисляем значение синего цвета, которое достигает максимума в середине экрана и уменьшается к краям
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))   # Рисуем горизонтальную линию с текущим цветом на экране

# Start screen
def start_screen():
    # Заполняем экран черным цветом
    screen.fill(BLACK)

    # Создаем пустой список для хранения кругов
    circles = []

    # Генерируем 100 кругов
    for _ in range(100):
        # Случайным образом выбираем радиус круга от 5 до 20 пикселей
        radius = random.randint(5, 20)

        # Случайным образом выбираем цвет круга из списка COLORS
        color = random.choice(COLORS)

        # Случайным образом выбираем позицию круга на экран
        pos = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]

        # Добавляем круг в список circles в виде [позиция, радиус, цвет]
        circles.append([pos, radius, color])

    # Рендерим текст "PACMAN" с использованием шрифта, делая его желтым
    title_text = font.render('PACMAN', True, YELLOW)

    # Рендерим текст "Press SPACE to Start" с использованием шрифта, делая его белым
    start_text = font.render('Press SPACE to Start', True, WHITE)

    # Рендерим текст "Press SPACE to Start" с использованием шрифта, делая его белым (дублируется для инструкций)
    instruction_text = font.render('Press SPACE to Start', True, WHITE)

    # Отображаем текст "PACMAN" на экране, центрируя его по горизонтали и немного выше центра по вертикали
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2 - 40))

    # Отображаем текст "Press SPACE to Start" на экране, центрируя его по горизонтали и по вертикали
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))

    # Отображаем текст "Press SPACE to Start" на экране, центрируя его по горизонтали и немного ниже центра по вертикали
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 - instruction_text.get_height() // 2 + 40))

    while not pygame.key.get_pressed()[pygame.K_SPACE]: # Пока не нажата клавиша пробела
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == pygame.QUIT:  # Если событие - выход из игры
                pygame.quit()  # Завершаем работу Pygame и выходим из функции
                return

        screen.fill(BLACK)  #Заполняем экран черным цветом
        for circle in circles:  # Проходим по каждому кругу в списке circles
            pos, radius, color = circle # Извлекаем позицию, радиус и цвет круга
            pygame.draw.circle(screen, color, pos, radius)   # Рисуем круг на экране

            # Случайным образом изменяем позицию круга по горизонтали и вертикали
            pos[0] += random.randint(-2, 2)
            pos[1] += random.randint(-2, 2)

            if pos[0] < 0 or pos[0] > SCREEN_WIDTH or pos[1] < 0 or pos[1] > SCREEN_HEIGHT: # Если круг выходит за границы экрана, удаляем его из списка circles
                circles.remove(circle)

        # Отображаем текст "PACMAN" на экране, центрируя его по горизонтали и немного выше центра по вертикали
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2 - 40))
        # Отображаем текст "Press SPACE to Start" на экране, центрируя его по горизонтали и по вертикали
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
        # Отображаем текст "Press SPACE to Start" на экране, центрируя его по горизонтали и немного ниже центра по вертикали
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 - instruction_text.get_height() // 2 + 40))

        pygame.display.flip() # Обновляем экран, чтобы отобразить все изменения
        clock.tick(30) # Ограничиваем частоту кадров до 30 кадров в секунду

# Game over screen
def game_over_screen(message, score): # Функция для отображения экрана окончания игры
    draw_gradient_background()  # Рисуем градиентный фон

    # Рендерим текст сообщения об окончании игры с использованием шрифта, делая его белым
    game_over_text = font.render(message, True, WHITE)
    # Рендерим текст с текущим счетом с использованием шрифта, делая его белым
    score_text = font.render(f'Score: {score}', True, WHITE)
    # Рендерим текст с инструкцией по перезапуску игры с использованием шрифта, делая его белым
    restart_text = font.render('Press R to Restart', True, WHITE)
    # Отображаем текст сообщения об окончании игры на экране, центрируя его по горизонтали и немного выше центра по вертикали
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 20))
    # Отображаем текст с текущим счетом на экране, центрируя его по горизонтали и немного ниже центра по вертикали
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + 20))
    # Отображаем текст с инструкцией по перезапуску игры на экране, центрируя его по горизонтали и еще ниже центра по вертикали
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 - restart_text.get_height() // 2 + 60))
    # Обновляем экран, чтобы отобразить все изменения
    pygame.display.flip()

# You win screen
def you_win_screen(score): # Функция для отображения экрана победы
    draw_gradient_background()   # Рисуем градиентный фон

    # Рендерим текст сообщения о победе с использованием шрифта, делая его белым
    win_text = font.render('You Win!', True, WHITE)
    # Рендерим текст с текущим счетом с использованием шрифта, делая его белым
    score_text = font.render(f'Score: {score}', True, WHITE)
    # Рендерим текст с инструкцией по перезапуску игры с использованием шрифта, делая его белым
    restart_text = font.render('Press R to Restart', True, WHITE)
    # Отображаем текст сообщения о победе на экране, центрируя его по горизонтали и немного выше центра по вертикали
    screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height() // 2 - 20))
    # Отображаем текст с текущим счетом на экране, центрируя его по горизонтали и немного ниже центра по вертикали
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + 20))
    # Отображаем текст с инструкцией по перезапуску игры на экране, центрируя его по горизонтали и еще ниже центра по вертикали
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 - restart_text.get_height() // 2 + 60))
    # Обновляем экран, чтобы отобразить все изменения
    pygame.display.flip()

# Main game loop
def game(): # Главный игровой цикл
    # Объявляем глобальные переменные, которые будут использоваться в функции
    global pacman_pos, ghosts, direction, score, dot_positions
    # Устанавливаем начальную позицию Пакмана
    pacman_pos = [1, 1]
    # Инициализируем список призраков с их начальными позициями, цветами и случайными направлениями
    ghosts = [
        {"pos": [12, 11], "color": RED, "direction": random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])},
        {"pos": [12, 12], "color": GREEN, "direction": random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])},
        {"pos": [11, 12], "color": ORANGE, "direction": random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])}
    ]
    # Устанавливаем начальное направление движения Пакмана (стоит на месте)
    direction = [0, 0]
    # Устанавливаем начальный счет игры
    score = 0
    # Создаем список позиций точек (еды) в лабиринте
    # Перебираем каждую строку и каждую ячейку в лабиринте
    # Если ячейка содержит 'o' (точку), добавляем ее координаты в список dot_positions
    dot_positions = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == 'o']

    # Устанавливаем флаг окончания игры в False (игра не окончена)
    game_over = False
    # Устанавливаем флаг паузы в False (игра не на паузе)
    paused = False


    while not game_over: # Главный игровой цикл, который продолжается, пока игра не окончена
        screen.fill(BLACK)  # Заполняем экран черным цветом

        for event in pygame.event.get():  # Обрабатываем все события, которые произошли
            if event.type == pygame.QUIT:    # Если событие - закрытие окна, завершаем игру
                game_over = True
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN: # Если событие - нажатие клавиши
                if event.key == pygame.K_LEFT: # Если нажата клавиша влево, устанавливаем направление движения влево
                    direction = [-1, 0]
                if event.key == pygame.K_RIGHT: # Если нажата клавиша вправо, устанавливаем направление движения вправо
                    direction = [1, 0]
                if event.key == pygame.K_UP:  # Если нажата клавиша вверх, устанавливаем направление движения вверх
                    direction = [0, -1]
                if event.key == pygame.K_DOWN: # Если нажата клавиша вниз, устанавливаем направление движения вниз
                    direction = [0, 1]
                if event.key == pygame.K_SPACE:  # Если нажата клавиша пробела, выходим из функции (пауза)
                    return
                if event.key == pygame.K_s: # Если нажата клавиша 's', переключаем состояние паузы
                    paused = not paused

        if not paused:  # Если игра не на паузе
            pacman_pos = move(pacman_pos, direction)  # Двигаем Пакмана в текущем направлении

        if (pacman_pos[0], pacman_pos[1]) in dot_positions:  # Если Пакман находится на позиции точки (еды)
            dot_positions.remove((pacman_pos[0], pacman_pos[1])) # Удаляем точку с этой позиции
            score += 10 # Увеличиваем счет на 10

        if check_win():  # Проверяем, выиграл ли игрок
            game_over = True # Если выиграл, завершаем игру
            you_win_screen(score)  # Отображаем экран победы с текущим счетом
            return

        if not paused:  # Если игра не на паузе
            for ghost in ghosts: # Двигаем каждого призрака
                ghost['pos'] = move(ghost['pos'], ghost['direction'])  # Двигаем призрака в текущем направлении
                if random.random() < 0.2:  # С вероятностью 20% меняем направление движения призрака на случайное
                    ghost['direction'] = random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])

        for ghost in ghosts: # Проверяем столкновение Пакмана с каждым призраком
            if ghost['pos'] == pacman_pos:   # Если позиция призрака совпадает с позицией Пакмана
                game_over = True # Завершаем игру
                game_over_screen("Game Over", score)   # Отображаем экран окончания игры с сообщением "Game Over" и текущим счетом
                return

        draw_maze()   # Отрисовываем лабиринт

        # Draw Pacman
        #Рисуем изображение Пакмана на экране на позиции, указанной в переменной pacman_pos
        screen.blit(pacman_image, (pacman_pos[0] * GRID_SIZE, pacman_pos[1] * GRID_SIZE))

        # Draw ghosts
        #Рисуем призраков на экране на их соответствующих позициях, цвет призрака определяется из словаря ghost_images
        for ghost in ghosts:
            screen.blit(ghost_images[ghost['color']], (ghost['pos'][0] * GRID_SIZE, ghost['pos'][1] * GRID_SIZE))

#Рисуем счет игрока на экране, передавая переменную score в функцию draw_score
        draw_score(score)

#После отрисовки всех элементов, обновляем экран
        pygame.display.flip()
        clock.tick(10) # Ограничиваем частоту обновления экрана, чтобы игра не происходила слишком быстро

# Main loop
running = True #Инициализируем переменную running как True, чтобы запустить главный игровой цикл
while running: #Главный игровой цикл
    start_screen() # Показываем стартовый экран
    start = False
    # Цикл проверки событий
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True # Начинаем игру после нажатия клавиши пробел

# проверяем значение переменной running
    if running: # если игра запущена, вызываем функцию game()
        game()  # устанавливаем переменную restart в значение
        restart = False # цикл продолжается, пока переменная restart равна False
        while not restart: # перебираем все события в очереди
            for event in pygame.event.get(): # если тип события - выход из игры, устанавливаем running в False и restart в True
                if event.type == pygame.QUIT:  # если тип события - нажатие клавиши
                    running = False
                    restart = True
                if event.type == pygame.KEYDOWN:  # если нажата клавиша "r", устанавливаем restart в True
                    if event.key == pygame.K_r:
                        restart = True

pygame.quit() #завершаем работу Pygame
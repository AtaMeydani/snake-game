from random import randrange
import pygame

from cube import GridCube
from snake import Snake
from algorithms import a_start, bfs
from dataset import Dataset

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 550

GRID_WIDTH = SCREEN_WIDTH
GRID_HEIGHT = 500

COLUMNS = 20
ROWS = 20

CUBE_WIDTH = GRID_WIDTH // COLUMNS
CUBE_HEIGHT = GRID_HEIGHT // ROWS

snake_start_position = (0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.font.init()
FONT = pygame.font.SysFont('arial', 20)
DELAY = 200

RUNNING = True
GRID = [[GridCube((x, y)) for y in range(ROWS)] for x in range(COLUMNS)]
CLOCK = pygame.time.Clock()  # creating our frame regulator
dataset = Dataset()


def random_snack_cube(snake):
    while True:
        x = randrange(0, COLUMNS)
        y = randrange(0, ROWS)
        snack = GRID[x][y]
        if snack in snake.body:
            continue
        break

    return snack


def draw_grid(window):
    x = 0
    y = 0

    for _ in range(COLUMNS):
        x = x + CUBE_WIDTH
        pygame.draw.line(window, (255, 255, 255), (x, 0), (x, GRID_HEIGHT))  # vertical lines

    for _ in range(ROWS):
        y = y + CUBE_HEIGHT
        pygame.draw.line(window, WHITE, (0, y), (GRID_WIDTH, y))  # horizontal lines


def redraw_window(window, snake, snack, direction):
    window.fill((0, 0, 0))
    draw_grid(window)
    snake.draw(window, CUBE_WIDTH, CUBE_HEIGHT)
    snack.draw(window, CUBE_WIDTH, CUBE_HEIGHT, color=GREEN)
    snake_score = FONT.render(f'Score: {len(snake.body)}', True, (255, 255, 255))
    snake_direction = FONT.render(f'Direction: {direction}', True, (255, 255, 255))
    window.blit(snake_score, (SCREEN_WIDTH * 1 // 10, GRID_HEIGHT + (SCREEN_HEIGHT - GRID_HEIGHT) // 2))
    window.blit(snake_direction, (SCREEN_WIDTH * 3 // 10, GRID_HEIGHT + (SCREEN_HEIGHT - GRID_HEIGHT) // 2))
    pygame.display.update()


def restart_game(window):
    restart_button_text = FONT.render("Play Again", True, WHITE)
    text_rect = restart_button_text.get_rect(
        center=(SCREEN_WIDTH * 8 // 10, GRID_HEIGHT + (SCREEN_HEIGHT - GRID_HEIGHT) // 2))
    pygame.draw.rect(window, BLACK, text_rect)
    window.blit(restart_button_text, text_rect)
    pygame.display.update()
    button_clicked = False
    global RUNNING

    while RUNNING and not button_clicked:
        pygame.time.delay(DELAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                RUNNING = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    button_clicked = True
                    break


def end_game(snake):
    for neighbor in snake.head.neighbors:
        if neighbor in snake.body or neighbor.obstacle:
            continue
        return False
    return True


def get_path(snack, snake):
    bfs_res = bfs(snack, snake)
    a_start_res = a_start(snack, snake)
    dataset.add(a_start_res.get('elapsed_time'), a_start_res.get('num_of_expanded_cubes'),
                bfs_res.get('elapsed_time'), bfs_res.get('num_of_expanded_cubes'))
    dataset.plot()

    # current_cube = bfs_res.get('leaf')
    current_cube = a_start_res.get('leaf')
    reached_the_snack = current_cube == snack
    path = []
    while current_cube.came_from:
        current_cube_x_equal_to_parent_x = current_cube.pos[0] == current_cube.came_from.pos[0]
        current_cube_y_equal_to_parent_y = current_cube.pos[1] == current_cube.came_from.pos[1]
        current_cube_x_less_than_parent_x = current_cube.pos[0] < current_cube.came_from.pos[0]
        current_cube_x_greater_than_parent_x = current_cube.pos[0] > current_cube.came_from.pos[0]
        current_cube_y_less_than_parent_y = current_cube.pos[1] < current_cube.came_from.pos[1]
        current_cube_y_greater_than_parent_y = current_cube.pos[1] > current_cube.came_from.pos[1]

        if current_cube_x_equal_to_parent_x and current_cube_y_less_than_parent_y:
            path.append('UP')
        elif current_cube_x_equal_to_parent_x and current_cube_y_greater_than_parent_y:
            path.append('DOWN')
        elif current_cube_x_less_than_parent_x and current_cube_y_equal_to_parent_y:
            path.append('LEFT')
        elif current_cube_x_greater_than_parent_x and current_cube_y_equal_to_parent_y:
            path.append('RIGHT')

        current_cube = current_cube.came_from

    for row in GRID:
        for cube in row:
            cube.reset()

    if reached_the_snack:
        return path
    return [path[-1]]


def main():
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Smart Snake!')

    for x in range(COLUMNS):
        for y in range(ROWS):
            GRID[x][y].add_neighbors(grid=GRID, rows=ROWS, columns=COLUMNS)

    snake = Snake(grid=GRID, color=RED, start_position=snake_start_position,
                  direction_x=1, direction_y=0, rows=ROWS, columns=COLUMNS)
    snack = random_snack_cube(snake)
    redraw_window(window, snake, snack, 'Starting ...')

    path = get_path(snack, snake)

    global RUNNING
    restart = False
    while RUNNING:
        pygame.time.delay(DELAY)
        CLOCK.tick(30)  # program will never run at more than 30 frames per second.

        if restart:
            restart_game(window)
            snake.reset(direction_x=1, direction_y=0)
            restart = False
            continue

        if snake.head.pos == snack.pos:
            snake.add_cube()
            snack = random_snack_cube(snake)
            redraw_window(window, snake, snack, 'Yummy!')
            if end_game(snake):
                restart = True
                continue
            path = get_path(snack, snake)

        if not path:
            if end_game(snake):
                restart = True
                continue
            path = get_path(snack, snake)

        direction = path.pop()
        if snake.move(direction=direction):
            redraw_window(window, snake, snack, direction)
        else:
            restart = True
            continue

        for snake_cube in snake.body:
            if snake_cube in snake.body[snake.body.index(snake_cube) + 1:]:
                restart = True
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                RUNNING = False
                break


if __name__ == '__main__':
    main()

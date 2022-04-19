from math import sqrt
from time import time


def a_start(snack, snake):
    start = time()
    open_list = [snake.head]
    closed_list = []
    last_cube = None

    while True:
        if not open_list:
            current_cube = last_cube
            break

        current_cube = min(open_list, key=lambda cube: cube.f)
        last_cube = current_cube
        open_list.remove(current_cube)
        closed_list.append(current_cube)

        if current_cube.pos == snack.pos:
            break

        for neighbor in current_cube.neighbors:
            if neighbor not in closed_list and not neighbor.obstacle and neighbor not in snake.body[
                                                                                         :-(current_cube.g + 1)]:
                temp_g = current_cube.g + 1
                if neighbor in open_list:
                    if temp_g < neighbor.g:
                        neighbor.g = temp_g
                        neighbor.came_from = current_cube
                else:
                    neighbor.g = temp_g
                    neighbor.came_from = current_cube
                    open_list.append(neighbor)
                neighbor.h = sqrt((neighbor.pos[0] - snack.pos[0]) ** 2 + (neighbor.pos[1] - snack.pos[1]) ** 2)
                #  neighbor.h = abs(neighbor.pos[0] - snack.pos[0]) + abs(neighbor.pos[1] - snack.pos[1])
                neighbor.f = neighbor.g + neighbor.h

    return {'leaf': current_cube,
            'elapsed_time': time() - start,
            'num_of_expanded_cubes': len(closed_list)}


def bfs(snack, snake):
    start = time()
    open_list = [snake.head]
    closed_list = []
    last_cube = None

    while True:
        if not open_list:
            current_cube = last_cube
            break

        current_cube = min(open_list, key=lambda cube: cube.f)
        last_cube = current_cube
        open_list.remove(current_cube)
        closed_list.append(current_cube)

        if current_cube.pos == snack.pos:
            break

        for neighbor in current_cube.neighbors:
            if neighbor not in closed_list and not neighbor.obstacle and neighbor not in snake.body[
                                                                                         :-(current_cube.f + 1)]:
                temp_f = current_cube.f + 1
                if neighbor in open_list:
                    if temp_f < neighbor.f:
                        neighbor.f = temp_f
                        neighbor.came_from = current_cube
                else:
                    neighbor.f = temp_f
                    open_list.append(neighbor)
                    neighbor.came_from = current_cube

    return {'leaf': current_cube,
            'elapsed_time': time() - start,
            'num_of_expanded_cubes': len(closed_list)}

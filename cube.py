import pygame


class GridCube:
    def __init__(self, pos, direction_x=None, direction_y=None):
        self.pos = pos
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.came_from = None
        self.obstacle = False

        #  for snake cube
        self.direction_x = direction_x
        self.direction_y = direction_y

    def draw(self, surface, cube_width, cube_height, color=(0, 0, 0), eyes=False):
        x = self.pos[0]
        y = self.pos[1]

        pygame.draw.rect(surface, color, (x * cube_width, y * cube_height, cube_width * 0.9, cube_height * 0.9))
        if eyes:
            center = cube_width // 2
            radius = min(cube_width, cube_height) * 0.1
            circle_middle_1 = (x * cube_width + center - radius, y * cube_height + 8)
            circle_middle_2 = (x * cube_width + cube_width - radius * 2, y * cube_height + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle_1, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle_2, radius)

    def add_neighbors(self, grid, rows, columns):
        x, y = self.pos
        if x > 0:
            self.neighbors.append(grid[x - 1][y])
        if y > 0:
            self.neighbors.append(grid[x][y - 1])
        if x < columns - 1:
            self.neighbors.append(grid[x + 1][y])
        if y < rows - 1:
            self.neighbors.append(grid[x][y + 1])

    def reset(self):
        self.f = 0
        self.g = 0
        self.h = 0
        self.came_from = None

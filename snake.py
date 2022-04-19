class Snake:
    def __init__(self, grid, color, start_position, direction_x, direction_y, rows, columns):
        self.grid = grid
        self.color = color
        self.start_position = start_position
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.rows = rows
        self.columns = columns

        self.head = self.grid[self.start_position[0]][self.start_position[1]]
        self.head.direction_x = self.direction_x
        self.head.direction_y = self.direction_y

        self.body = [self.head]
        self.turns = {}

    def move_cube_of_snake_body(self, snake_cube_index, direction_x, direction_y):
        old_snake_cube = self.body[snake_cube_index]
        new_snake_cube = self.grid[old_snake_cube.pos[0] + direction_x][old_snake_cube.pos[1] + direction_y]
        new_snake_cube.direction_x = direction_x
        new_snake_cube.direction_y = direction_y
        self.body[snake_cube_index] = new_snake_cube

    def opposite_directio(self, direction_x, direction_y):
        if direction_x + self.head.direction_x == 0 and direction_y + self.head.direction_y == 0:
            self.body.reverse()
            self.head = self.body[0]
            for snake_cube in self.body:
                snake_cube.direction_x *= -1
                snake_cube.direction_y *= -1

    def move(self, direction):
        def set_direction(x, y):
            self.opposite_directio(x, y)
            self.direction_x = x
            self.direction_y = y
            self.turns[self.head.pos[:]] = (self.direction_x, self.direction_y)

        match direction:
            case 'UP':
                set_direction(0, -1)
            case 'DOWN':
                set_direction(0, 1)
            case 'LEFT':
                set_direction(-1, 0)
            case 'RIGHT':
                set_direction(1, 0)

        new_x = self.head.pos[0] + self.direction_x
        new_y = self.head.pos[1] + self.direction_y
        if not (self.columns > new_x >= 0 and self.rows > new_y >= 0):
            return False

        new_tail = None
        if self.grid[new_x][new_y] == self.body[-1] and len(self.body) > 1:
            old_tail = self.body[-1]
            old_tail_pos = (old_tail.pos[0], old_tail.pos[1])
            if old_tail_pos in self.turns:
                direction_x, direction_y = self.turns[old_tail_pos]
            else:
                direction_x, direction_y = old_tail.direction_x, old_tail.direction_y

            new_tail = {'new_tail_x': old_tail.pos[0] + direction_x,
                        'new_tail_y': old_tail.pos[1] + direction_y,
                        'new_tail_direction': (direction_x, direction_y)}

        for snake_cube_index in range(len(self.body)):
            if (snake_cube_index == len(self.body) - 1) and new_tail:
                snake_cube = self.grid[new_tail.get('new_tail_x')][new_tail.get('new_tail_y')]
                snake_cube.direction_x, snake_cube.direction_y = new_tail.get('new_tail_direction')
                self.body[snake_cube_index] = snake_cube
                break

            snake_cube = self.body[snake_cube_index]
            snake_cube_position = snake_cube.pos
            if snake_cube_position in self.turns:
                direction_x, direction_y = self.turns[snake_cube_position]
                self.move_cube_of_snake_body(snake_cube_index, direction_x, direction_y, )
                if snake_cube_index == len(self.body) - 1:
                    del self.turns[snake_cube_position]
            else:
                self.move_cube_of_snake_body(snake_cube_index, snake_cube.direction_x, snake_cube.direction_y)

        self.head = self.body[0]
        return True

    def reset(self, direction_x, direction_y):
        self.head = self.grid[self.start_position[0]][self.start_position[1]]
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.head.direction_x = self.direction_x
        self.head.direction_y = self.direction_y

        self.body = [self.head]
        self.turns = {}

    def add_cube(self):
        tail = self.body[-1]
        direction_x, direction_y = tail.direction_x, tail.direction_y
        x, y = tail.pos[0] - direction_x, tail.pos[1] - direction_y

        new_tail = None

        if self.columns > x >= 0 and self.rows > y >= 0 and self.grid[x][y] not in self.body:
            new_tail = self.grid[x][y]
        else:
            for neighbor in tail.neighbors:
                if neighbor not in self.body:
                    new_tail = neighbor
                    new_direction_x = tail.pos[0] - new_tail.pos[0]
                    new_direction_y = tail.pos[1] - new_tail.pos[1]
                    new_tail.direction_x = new_direction_x
                    new_tail.direction_y = new_direction_y
                    self.turns[new_tail.pos[:]] = (new_direction_x, new_direction_y)
                    break

        if new_tail:
            new_tail.color = self.color
            self.body.append(new_tail)
            self.body[-1].direction_x = direction_x
            self.body[-1].direction_y = direction_y
        else:
            print('Error adding new cube to snake')

    def draw(self, surface, cube_width, cube_height):
        for index, cube in enumerate(self.body):
            if index == 0:
                cube.draw(surface, cube_width, cube_height, color=self.color, eyes=True)
            else:
                cube.draw(surface, cube_width, cube_height, color=self.color)

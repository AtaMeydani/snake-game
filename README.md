# snake-game

### Graphic structure of the program:
The pygame library has been used to design the program, and it is possible for us to run the game in different dimensions and at the same time observe the score and the direction of the snake.

### Snake features:
In this game, the snake has only one head and according to it, it can move in all directions except the cases where it cuts itself, which is checked during the execution of the algorithm. Our snake also has the ability to move behind its tail. For example, consider the case where our snake has a length of 4 and this snake is located in a space of 2 * 2, it is possible for the snake to rotate around itself without making a mistake about cutting itself.

### Snack features:
The snack is placed randomly in an empty house that, if eaten by a snake, will add one unit to the snake's length.

### Algorithms:
In this game, two algorithms **A \*** and **BFS** are used. In order for the snake to reach the snack, the algorithm is executed only once, except in cases where the snake's body prevents the creation of a path, in which case we run the algorithm with each movement to open a path if possible by moving the snake's body and gathering it. Because we run the algorithm once until we reach the snack, so when expanding the node, we must not consider the body of the snake as much as the depth of the node (from the tail) so that the snake can cross the place where it was before. Each time we execute the get_path function, both algorithms are executed using the A * algorithm to move.

### Comparison of algorithms:
In the previous section, it was said that both routing algorithms run, the reason for this is to compare algorithms under the same conditions. For better comparison, the number of expanded nodes and the execution time of each algorithm are stored in an Excel file and then the associated diagrams are drawn for ease of comparison.
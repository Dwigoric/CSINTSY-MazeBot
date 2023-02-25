from queue import Queue


def disp_maze(maze):
    for row in maze:
        for col in row:
            print(col, end="\t")
        print('\n')


def read_maze(filename):
    with open(filename) as f:
        size = f.readline()
        maze = [[*line] for line in f]
        
    return size, maze


def flood_fill(txt_maze, goal):
    # Implement breadth-first search
    # to convert the maze to a distance map
    # from the goal
    q = Queue()
    q.put(goal)
    visited = set()
    visited.add(goal)

    distances = [[-1 for _ in range(len(txt_maze[0]))] for _ in range(len(txt_maze))]
    curr_distance = 0
    distances[goal[0]][goal[1]] = curr_distance

    while not q.empty():
        curr = q.get()
        curr_distance = distances[curr[0]][curr[1]]

        for neighbor in get_neighbors(curr, txt_maze):
            if neighbor not in visited:
                visited.add(neighbor)
                q.put(neighbor)
                distances[neighbor[0]][neighbor[1]] = curr_distance + 1

    return distances


def get_neighbors(node, maze):
    neighbors = []
    row, col = node
    if row > 0 and maze[row - 1][col] != '#':
        neighbors.append((row - 1, col))
    if row < len(maze) - 1 and maze[row + 1][col] != '#':
        neighbors.append((row + 1, col))
    if col > 0 and maze[row][col - 1] != '#':
        neighbors.append((row, col - 1))
    if col < len(maze[0]) - 1 and maze[row][col + 1] != '#':
        neighbors.append((row, col + 1))

    return neighbors


def find_start_goal(maze):
    start, goal = None, None
    for row_idx, row in enumerate(maze):
        for col_idx, col in enumerate(row):
            if col == 'S':
                start = (row_idx, col_idx)
            elif col == 'G':
                goal = (row_idx, col_idx)

            if start and goal:
                return start, goal

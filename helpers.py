from queue import Queue


def read_maze(filename):
    '''
    Reads a maze from a text file

    Inputs:
    - filename: the name of the file to read

    Returns:
    - size: an integer representing the width and height of the maze
    - txtMaze: a 2D list of characters representing the maze
    '''

    with open(filename) as f:
        size = f.readline()
        txtMaze = [line.rstrip('\n') for line in f]

    return int(size), txtMaze


def find_path(distances, start, goal):
    """
    Finds the shortest path from start to goal in the maze using greedy best-first search

    Inputs:
    - distances: a 2D list of integers representing the distance from the goal
    - start: a tuple representing the start location
    - goal: a tuple representing the goal location

    Returns:
    - path_list: a list of tuples representing the path from start to goal
    """

    path_list = []
    curr = start

    while curr != goal:
        path_list.append(curr)

        next_states = get_next_states(distances, curr)
        if len(next_states) == 0:
            return None

        curr = min(next_states, key=lambda x: distances[x[0]][x[1]])

    path_list.append(goal)

    return path_list


def get_next_states(distances, current):
    """
    Finds the next states from the current state

    Inputs:
    - distances: a 2D list of integers representing the distance from the goal
    - current: a tuple representing the current state

    Returns:
    - next_states: a list of tuples representing the next states
    """

    next_states = []
    row, col = current

    if row > 0 and distances[row - 1][col] >= 0:
        next_states.append((row - 1, col))

    if row < len(distances) - 1 and distances[row + 1][col] >= 0:
        next_states.append((row + 1, col))

    if col > 0 and distances[row][col - 1] >= 0:
        next_states.append((row, col - 1))

    if col < len(distances[0]) - 1 and distances[row][col + 1] >= 0:
        next_states.append((row, col + 1))

    return next_states


def flood_fill(txt_maze, goal, distances):
    '''
    Implements breadth-first search to convert the maze to a distance map from the goal

    Inputs: 
    - txt_maze: a 2D list of characters representing the maze
    - goal: a tuple representing the goal location
    - distances: a 2D list of integers representing the initial distance from the goal

    Returns:
    - distances: a 2D list of integers representing the flood-fill distance from the goal
    '''

    q = Queue()
    q.put(goal)

    visited = set()
    visited.add(goal)

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
    '''
    Gets the neighbors of a node in the maze

    Inputs:
    - node: a tuple representing the node
    - maze: a 2D list of characters representing the maze

    Returns:
    - neighbors: a list of tuples representing the neighbors of the node
    '''

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


def start_goal_distances(maze):
    '''
    Finds the start and goal locations in the maze

    Inputs:
    - maze: a 2D list of characters representing the maze

    Returns:
    - start: a tuple representing the start location
    - goal: a tuple representing the goal location
    - distances: a 2D list of integers representing the distance from the goal
    '''

    distances = [[-1 for _ in range(len(maze[0]))] for _ in range(len(maze))]
    start, goal = None, None

    for row_idx, row in enumerate(maze):
        for col_idx, col in enumerate(row):
            if col == 'S':
                start = (row_idx, col_idx)
                distances[row_idx][col_idx] = -1
            elif col == 'G':
                goal = (row_idx, col_idx)
                distances[row_idx][col_idx] = 0
            elif col == '#':
                distances[row_idx][col_idx] = -2
            else:
                distances[row_idx][col_idx] = -1

            # if start and goal:
                # return start, goal, distances

    # Placed outside of the loop to avoid prematurely returning            
    return start, goal, distances

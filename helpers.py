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
        txtMaze = [[*line] for line in f]
        
    return int(size), txtMaze


def find_path(maze, start, goal):
    """
    Finds the shortest path from start to goal in the maze

    Inputs:
    - maze: a 2D list of characters representing the maze
    - start: a tuple representing the start location
    - goal: a tuple representing the goal location

    Returns:
    - path_list: a list of tuples representing the path from start to goal
    """
    
    q = Queue()
    q.put(start)

    visited = set()
    visited.add(start)

    path = {}
    path[start] = None

    while not q.empty():
        curr = q.get()

        if curr == goal:
            break
        
        for neighbor in get_neighbors(curr, maze):
            if neighbor not in visited:
                q.put(neighbor)
                visited.add(neighbor)
                path[neighbor] = curr

    curr = goal
    path_list = [curr]

    while curr != start:
        curr = path[curr]
        path_list.append(curr)

    path_list.reverse()

    return path_list

def flood_fill(txt_maze, goal):
    '''
    Implements breadth-first search to convert the maze to a distance map from the goal

    Inputs: 
    - txt_maze: a 2D list of characters representing the maze
    - start: a tuple representing the start location
    - goal: a tuple representing the goal location

    Returns:
    - distances: a 2D list of integers representing the distance from the goal
    '''

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


def find_start_goal(maze):
    '''
    Finds the start and goal locations in the maze

    Inputs:
    - maze: a 2D list of characters representing the maze

    Returns:
    - start: a tuple representing the start location
    - goal: a tuple representing the goal location
    '''

    start, goal = None, None
    for row_idx, row in enumerate(maze):
        for col_idx, col in enumerate(row):
            if col == 'S':
                start = (row_idx, col_idx)
            elif col == 'G':
                goal = (row_idx, col_idx)

            if start and goal:
                return start, goal

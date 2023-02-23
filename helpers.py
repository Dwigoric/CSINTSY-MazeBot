import copy
import math 

def disp_maze(maze):
    for row in maze:
        for col in row:
            print(col, end=" ")
        print('\n')

def read_maze(filename):
    with open(filename) as f:
        size = f.readline()
        maze = [[*line] for line in f]
        
    return size, maze

'''
    NOTE TO JOSHUA/RALPH:

    Converting the text file into numerical values for the maze. Right now: 

    > 0: empty (.), start (S), or goal (G), 
    > -1: wall (#), 

    Feel free to change this to whatever is best for the algorithm!
'''
def convert_maze(txt_maze):
    start, goal = None, None
    converted = copy.deepcopy(txt_maze)
    
    for row_idx, row in enumerate(txt_maze):
        for col_idx, col in enumerate(row):

            if col == 'S':
                start = [row_idx, col_idx]
                converted[row_idx][col_idx] = 0
            elif col == 'G':
                goal = [row_idx, col_idx]
                converted[row_idx][col_idx] = 0

            elif col == '#':
                converted[row_idx][col_idx] = -1
            elif col == '.':
                converted[row_idx][col_idx] = 0

    return start, goal, converted

def get_euclidean_distances(maze, goal):
    distances = copy.deepcopy(maze)

    for row_idx, row in enumerate(maze):
        for col_idx, col in enumerate(row):
            if col == -1:
                distances[row_idx][col_idx] = -1
            else:
                distances[row_idx][col_idx] = round(math.dist([row_idx, col_idx], goal), 4)

    return distances
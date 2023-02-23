from helpers import *

size, txt_maze = read_maze('maze.txt')
start, goal, converted_maze = convert_maze(txt_maze)
distances = get_euclidean_distances(converted_maze, start, goal)

disp_maze(distances)
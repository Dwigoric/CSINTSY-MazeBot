from helpers import *

size, txt_maze = read_maze('maze.txt')
start, goal, distances= start_goal_distances(txt_maze)
converted_maze = flood_fill(txt_maze, goal)

from helpers import *

size, txt_maze = read_maze('maze.txt')
start, goal = find_start_goal(txt_maze)
converted_maze = flood_fill(txt_maze, goal)

disp_maze(converted_maze)

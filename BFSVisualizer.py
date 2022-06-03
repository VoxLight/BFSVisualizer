# Python 3.8.0+
# Tested on Windows 10

# version 0.1.0


# built-ins
import re
import os
import sys
import glob
import time
import math
import shutil
import pygame
import argparse
from PIL import Image

"""
Exit Codes used from: https://tldp.org/LDP/abs/html/exitcodes.html

 
Underscores at the start is a naming convention I use to denote 'private' objects.
Python has no implementation of private/public, but this makes it harder for linters
to reccomend these objects.

Two underscores are akin to an object not used by my own code.

similarly, an underscore at the end is used to represent an object that wants a similar
name to an already decalred object or keyword.
"""
class Interactive:


    scale = 10
    offset_position = (0, 0)
    start_tracking_pos = (0, 0)

    follow = False
    follow_offset_position = (0, 0)
    follow_start_tracking_pos = (0, 0)

    @classmethod
    def restoreDefaults(cls):
        cls.scale = 10
        cls.offset_position = (0, 0)
        cls.start_tracking_pos = (0, 0)
        cls.follow_offset_position = (0, 0)
        cls.follow_start_tracking_pos = (0, 0)


    @classmethod
    def growScale(cls, val):
        cls.scale += val*cls.scale*0.1

    @classmethod
    def setOffset(cls):
        print("Offset Position: ", cls.offset_position)
        print("Start Pos: ", cls.start_tracking_pos)
        print()
        if cls.follow:
            cls.follow_offset_position = _add_vect_2D(_negate_vect_2D(pygame.mouse.get_pos()),  cls.follow_start_tracking_pos)
        else:
            cls.offset_position = _add_vect_2D(_negate_vect_2D(pygame.mouse.get_pos()),  cls.start_tracking_pos)

    @classmethod
    def startTrackingPosition(cls):
        if cls.follow:
            cls.follow_offset_position = (0, 0)
            cls.follow_start_tracking_pos = pygame.mouse.get_pos()
        else:
            cls.start_tracking_pos = _add_vect_2D(pygame.mouse.get_pos(), cls.offset_position)
        

    @classmethod
    def followToggle(cls):
        cls.follow = not cls.follow






# privates
def _map(value, istart, istop, ostart, ostop):
    return round(ostart + (ostop - ostart) * ((value - istart) / (istop - istart)))

def _get_dims(matrix):
    # x , y
    return len(matrix[0]), len(matrix)
    
def _add_vect_2D(vect1, vect2):
    """Adds two indexible reprs. of 2D vects

    Args:
        vect1 (tuple): Tuple of ints Y & X.
        vect2 (tuple): Tuple of ints Y & X.

    Returns:
        tuple: vect1 offset by vect2
    """
    return (vect1[0]+vect2[0], vect1[1]+vect2[1])

def _negate_vect_2D(vect):
    """Negates a 2D vect

    Args:
        vect (tuple): Tuple of ints Y & X.

    Returns:
        tuple: -vect
    """
    return (-vect[0], -vect[1])
    
def _depack_image_data(matrix):
    w, h = _get_dims(matrix)
    
    goals = []
    closed = []
    start, end = None, None
    
    for x in range(w):
        for y in range(h):
            case = matrix[x][y]
            if case == SYMBOLS["CLOSE"]: closed.append((x, y))
            elif case == SYMBOLS["COIN"]: goals.append((x, y))
            elif case == SYMBOLS["START"]: start = (x, y)
            elif case == SYMBOLS["END"]: end = (x, y)
            
    return start, end, closed, goals
      
def _in_grid(pos, grid):
    w, h = _get_dims(grid)
    x, y = pos
    return  not ((x < 0) or
            (y < 0) or
            (x > w-1) or
            (y > h-1))      

def _establish_cli():
    """Establishes the cli for this program

    Returns:
        argparse.Namespace: Object with formatted cli args. 
    """
    # Defaults
    fps = 60
    size = 800
    
    
    # Establish the cli 
    parser = argparse.ArgumentParser(description="Get the maze file path, configs, and flags.")
    parser.add_argument(
        '-fps', type=float, nargs='?', default=fps, dest="fps",
        help="framerate of the loop. (defaul is 60)"
    )
    
    parser.add_argument(
        '-size', type=int, nargs='?', default=size, dest="size",
        help="height of the pygame surface (aspect ration 1:1). (defaul is 800)"
    )
    
    parser.add_argument(
        '-scr', type=str, nargs='?', default=None, dest="scr",
        help="filepath to save a screenshot of the completed path. will not save if not provided."
    )
    
    parser.add_argument(
        '-gif', type=str, nargs='?', default=None, dest="gif",
        help="filepath to save frames in a subdir and then compile them into a gif."
    )
    
    parser.add_argument(
        'maze_fp', type=str, nargs='?', default=None,
        help="filepath of the maze to generate a path for."
    )
    
    # get the args
    return parser.parse_args()

def _at_pos(grid, pos):
    return grid[pos[0]][pos[1]]

def _scale_position(node, small_dim, big_dim):
    return (
        _map(node[0], 0, small_dim[0], 0, big_dim[0]),
        _map(node[1], 0, small_dim[1], 0, big_dim[1])
    )
    
def _make_rects(nodes, dims, color, offsets):

    size, maze_res, res = dims
    output = []
    for node in nodes:
        scaled_node = _scale_position(node, maze_res, res)
        node_offset = (scaled_node[0] + offsets[0], scaled_node[1] + offsets[1])

        rect = (pygame.Rect(
            node_offset,
            size
        ), color)
        output.append(rect)
    return output
   
def _handle_events():
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT: sys.exit(0)
        if event.type == pygame.MOUSEWHEEL:
                Interactive.growScale(event.y)
                print("Scale Increased!")

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                Interactive.setOffset()

            elif pygame.mouse.get_rel()[0]:
                Interactive.startTrackingPosition()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                Interactive.followToggle()
            elif event.key == pygame.K_k:
                Interactive.restoreDefaults()

                


def _draw(surface, packed, matrix2D, save_frame_, reset_pos=False, follow=False):

    RES = WIDTH, HEIGHT = surface.get_size()
    MAZE_RES = MAZE_W, MAZE_H = _get_dims(matrix2D)
    
    path, start, end, closed, goals = packed

    if follow:
        RECT_SIZE = (1*Interactive.scale, 1*Interactive.scale)#((WIDTH/MAZE_W)+1), (HEIGHT/MAZE_H)+1
        SCALED_RES = (MAZE_RES[0]*Interactive.scale)+1, MAZE_RES[1]*Interactive.scale
        DIMS = RECT_SIZE,MAZE_RES,SCALED_RES#SCALED_RES#RES
        offsets = (WIDTH/2) - ((path[-1][0]*Interactive.scale) + Interactive.follow_offset_position[0]), (HEIGHT/2) - ((path[-1][1]*Interactive.scale) + Interactive.follow_offset_position[1])
    elif not reset_pos:
        RECT_SIZE = (1*Interactive.scale, 1*Interactive.scale)#((WIDTH/MAZE_W)+1), (HEIGHT/MAZE_H)+1
        SCALED_RES = (MAZE_RES[0]*Interactive.scale)+1, MAZE_RES[1]*Interactive.scale
        DIMS = RECT_SIZE,MAZE_RES,SCALED_RES#SCALED_RES#RES
        offsets = (WIDTH/2) - Interactive.offset_position[0], (HEIGHT/2) - Interactive.offset_position[1]
    else:
        RECT_SIZE = (WIDTH/MAZE_W)+1, (HEIGHT/MAZE_H)+1
        DIMS = RECT_SIZE,MAZE_RES,RES#SCALED_RES#RES
        offsets = 0, 0

    if RECT_SIZE[0] < 1:
        RECT_SIZE = (1, 1)

    

    
    to_draw = _make_rects(path, DIMS, COLORS["WHITE"], offsets) +\
            _make_rects([start], DIMS, COLORS["BLUE"], offsets) +\
            _make_rects([end], DIMS, COLORS["GREEN"], offsets) +\
            _make_rects(closed, DIMS, COLORS["RED"], offsets) +\
            _make_rects(goals, DIMS, COLORS["YELLOW"], offsets) 
    
    surface.fill(COLORS["BLACK"])
    
    for rect in to_draw:
        pygame.draw.rect(surface, rect[1], rect[0])
        
    pygame.display.flip()
    
    if save_frame_:
        _save_frame(surface, save_frame_)
    
    _handle_events()
    
def _scrnsht(surface, fp):
    pygame.image.save(surface, fp)
    
def _save_frame(surface, fp):
    name = fp.split("/")[-1]
    frame = len([name for name in os.listdir(fp)])
    pygame.image.save(surface, fp+"/"+name+str(frame)+".png")

def _make_gif(fp, fps):
    fp_in = fp
    name = fp_in+"/"+fp_in.split("/")[-1]+"*.png"
    fp_out = fp_in+".gif"
    print("Generating Gif")
    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(name), key=lambda x: int("".join(re.findall("[0-9]", x))))]
    print("Saving Gif")
    img.save(fp=fp_out, format='GIF', append_images=imgs,
            save_all=True, fps=fps, duration=40, optimize=False, loop=1, palettesize=len(list(COLORS.values())), subrectangles=True)
    
    print("Cleaning up.")
    shutil.rmtree(fp_in)

# publics
COLORS = {
    "WHITE":(255, 255, 255),
    "BLACK":(0, 0, 0),
    "RED":(255,0,0),
    "GREEN":(0,255,0),
    "BLUE":(0,0,255),
    "YELLOW":(255,255,0)
}

SYMBOLS = {
    "OPEN": COLORS["BLACK"],
    "CLOSE": COLORS["RED"],
    "END": COLORS["GREEN"],
    "START": COLORS["BLUE"],
    "COIN": COLORS["YELLOW"]
}

DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

def img_to_matrix(fp):
    """Takes in a filepath of a png image and returns a 2D matrix of RGB color values.

    Args:
        fp (str): path to the image

    Returns:
        list: 2D array of RGB tuples
    """
    img = Image.open(fp)
    
    # create a 2d matrix of (R, G, B) values from the image.
    return [
        [img.getpixel((x, y))[:3] for y in range(img.height) 
            ] for x in range(img.width)
    ]

def matrix_to_adj(matrix):
    w, h = _get_dims(matrix)
    nodes = {}

    for x in range(w):
        for y in range(h):
            cur = (x, y)
            
            
            
            if _at_pos(matrix, cur) is SYMBOLS["CLOSE"]: continue
            
            up = _add_vect_2D(cur, DIRECTIONS["UP"])
            down = _add_vect_2D(cur, DIRECTIONS["DOWN"])
            left = _add_vect_2D(cur, DIRECTIONS["LEFT"])
            right = _add_vect_2D(cur, DIRECTIONS["RIGHT"])
            
            neighbors = [up, down, left, right]
            
            
            
            # purge nodes outside of the grid
            neighbors = list(filter(lambda x: _in_grid(x, matrix), neighbors))
            
            
            # purge nodes that can't be traveled on
            neighbors = list(filter(lambda x: not (_at_pos(matrix, x) == SYMBOLS["CLOSE"]), neighbors))
            
            nodes[str(cur)] = neighbors
            
    return nodes

def is_solvable(matrix):
    adj = matrix_to_adj(matrix)
    start, end, _, goals = _depack_image_data(matrix)
    
    queue = []
    visited = []
    
    queue = [start] # enqueue
    
    while queue:
        cur = queue.pop(0) # dequeue
        if goals: 
            if cur in goals: goals.pop( goals.index(cur) )
        elif cur == end: return True

        for neighbor in adj[str(cur)]:
            if neighbor in visited: continue
            queue.append(neighbor)
            visited.append(neighbor)

    return False

# secrets


def __main():
    args = _establish_cli()
    
    # consts
    MAZE_FP = args.maze_fp
    MATRIX = img_to_matrix(MAZE_FP)
    FPS = args.fps

    RES = args.size, args.size
    
    if args.gif:
        saveframe = args.gif
        if not os.path.isdir(saveframe):
            os.mkdir(saveframe)
    else:
        saveframe = False
    
    pygame.init()
    SCREEN = pygame.display.set_mode(RES)
    
    
    adj = matrix_to_adj(MATRIX)
    start, end, closed, goals = _depack_image_data(MATRIX) # _ unused "closed" variable
    
    queue = [ [start] ]
    visited = [ start ]
    found_goals = []
    
    
    while queue:
        path = queue.pop(0)
        node = path[-1]
        packed = path, start, end, closed, goals + found_goals
        
        
        
        _draw(SCREEN, packed, MATRIX, saveframe, reset_pos=False, follow=Interactive.follow)
        
        if goals:
            if node in goals: 
                found_goals.append( goals.pop( goals.index(node)))
                visited = [node]
                queue = [path]
        elif node == end:
            if args.scr:
                _draw(SCREEN, packed, MATRIX, saveframe, reset_pos=True)
                _scrnsht(SCREEN, args.scr)
            if args.gif:
                _make_gif(saveframe, FPS)

            print("End Found!")
            break
        
        for neighbor in adj[str(node)]:
            next_path = list(path)
            
            if neighbor in visited: continue
            
            next_path.append(neighbor) 
            queue.append(next_path)
            visited.append(neighbor)
            
        time.sleep(1/FPS)

    # end screen
    while True:
        _draw(SCREEN, packed, MATRIX, saveframe, reset_pos=False, follow=Interactive.follow)
        _handle_events()
        time.sleep(1/FPS)
       
if __name__ == "__main__":
    __main()
    
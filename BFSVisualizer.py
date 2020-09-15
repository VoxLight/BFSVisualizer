# built-ins
import argparse
import pygame
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


# privates
_scrnsht = lambda: None
_frame = lambda: None

def _get_dims(matrix):
    # x , y
    return len(matrix[0]), len(matrix)

def _img_to_matrix(fp):
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
        '-fps', type=int, nargs=1, default=fps, dest="fps",
        help="framerate of the loop. (defaul is 60)"
    )
    
    parser.add_argument(
        '-size', type=int, nargs=1, default=size, dest="size",
        help="height of the pygame surface (aspect ration 1:1). (defaul is 800)"
    )
    
    parser.add_argument(
        '-scr', type=int, nargs=1, default=None, dest="scr",
        help="filepath to save a screenshot of the completed path. will not save if not provided."
    )
    
    parser.add_argument(
        '-gif', type=int, nargs=1, default=None, dest="gif",
        help="filepath to save frames in a subdir and then compile them into a gif."
    )
    
    parser.add_argument(
        'maze_fp', type=str, nargs=1, default=None,
        help="filepath of the maze to generate a path for."
    )
    
    # get the args
    return parser.parse_args()


# publics
COLORS = {
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




# secrets

def __main():
    args = _establish_cli()
        
    if args.scr:
        _scrnsht = lambda surface: pygame.image.save(surface, args.scr)
        
    if args.gif:
        _frame = lambda surface: pygame.image.save(surface, args.gif)
    
    # consts
    MAZE_FP = args.maze_fp
    MATRIX = _img_to_matrix(MAZE_FP)
    MAZE_W, MAZE_H = _get_dims(MATRIX)
    FPS = args.fps

    RES = WIDTH, HEIGHT = args.size, args.size
    
    # this allows our rects to scale
    RECT_W, RECT_H = round(WIDTH/MAZE_W)+1, round(HEIGHT/MAZE_H)+1



    
    
    
    
    
    

if __name__ == "__main__":
    __main()
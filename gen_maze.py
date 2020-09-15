# CLI for generating mazes for the BFSVisualizer

# dependancies
from PIL import Image, ImageDraw

# locals
import math
import argparse
from random import  shuffle, randrange, choice, seed
seed(randrange(100000000))

PRIM_DIRECTIONS = {
    "UP": (0, -2),
    "DOWN": (0, 2),
    "LEFT": (-2, 0),
    "RIGHT": (2, 0)
}

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

def grid_maze(size):
    width, height = size
    walls = list(set([
        (x, y) for y in range(0, height, 2) for x in range(width) # every other row
    ] + [
        (x, y) for y in range(height) for x in range(0, width, 2) # every other column
    ]
    
    ))
    
    cells = [
        (x, y) for x in range(width) for y in range(height) if (x, y) not in walls
    ]
    
    walls = [wall for wall in walls if _good_node(wall, (width, height))]
    
    temp = Image.new('RGB', (width, height), SYMBOLS["OPEN"])
    
    draw = ImageDraw.Draw(temp)
    
    for wall in walls:
        draw.point(wall, SYMBOLS["CLOSE"])
    
    return temp, walls, cells

def filled_maze(size):
    return Image.new('RGB', size, SYMBOLS["CLOSE"])

def empty_maze(size):
    return Image.new('RGB', size, SYMBOLS["OPEN"])

"""
def prim(img):
    # empty maze
    pygame.init()
    
    screen = pygame.display.set_mode(img.size)
    
    w, h = img.size
    w, h = w-1, h-1
    draw = ImageDraw.Draw(img)
    
    
    start = (randrange(1, w), randrange(1, h))
    
    draw.point(start, SYMBOLS["START"])
    
    maze = [start]
    
    frontier = _cell_neighbors(start)
    
    
    
    while frontier:
        node = frontier.pop( frontier.index( choice(frontier) ) ) 
        maze.append(node)
        
        for neighbor in _cell_neighbors(node):
            if not _good_node(neighbor, img.size): continue
            if neighbor in frontier: continue
            if _exits(neighbor, img) >= 1: continue
            if neighbor in maze:
                draw.line(node+neighbor, SYMBOLS["CLOSE"], 1)
                gimg = pygame.image.frombuffer(img.tobytes(), img.size, "RGB")
                screen.blit(gimg, (0, 0))
                pygame.display.update()
            
            frontier.append(neighbor)
            
        
            
    draw.point(maze[-1], SYMBOLS["END"])
    draw.point(start, SYMBOLS["START"])
"""
    
def prim_no_vis(img):
    # empty maze  
    w, h = img.size
    w, h = w-1, h-1
    draw = ImageDraw.Draw(img)
    
    
    start = (randrange(1, w), randrange(1, h))
    
    draw.point(start, SYMBOLS["START"])
    
    maze = [start]
    
    frontier = _cell_neighbors(start)
    
    
    
    while frontier:
        node = frontier.pop( frontier.index( choice(frontier) ) ) 
        maze.append(node)
        
        for neighbor in _cell_neighbors(node):
            if not _good_node(neighbor, img.size): continue
            if neighbor in frontier: continue
            if _exits(neighbor, img) >= 1: continue
            if neighbor in maze:
                draw.line(node+neighbor, SYMBOLS["CLOSE"], 1)
            
            frontier.append(neighbor)
            
        
            
    draw.point(maze[-1], SYMBOLS["END"])
    draw.point(start, SYMBOLS["START"])   

def _establish_cli():
    """Establishes the cli for this program

    Returns:
        argparse.Namespace: Object with formatted cli args. 
    """
    parser = argparse.ArgumentParser(description="Get arguments for generating mazes.")
    
    # Defaults
    width = 10
    height = 10
    
    # Establish the cli 
    parser.add_argument(
        '-width', type=int, nargs='?', default=width, dest="width",
        help="width of the resulting maze. maintains a 1:1 aspect ratio. (width x width) (defaults to 10)"
    )
    
    parser.add_argument(
        '-eight', type=int, nargs='?', default=height, dest="height",
        help="height of the resulting maze. (defaults to 10)"
    )
    
    # get the args
    return parser.parse_args()

def _add_vect_2D(vect1, vect2):
    """Adds two indexible reprs. of 2D vects

    Args:
        vect1 (tuple): Tuple of ints Y & X.
        vect2 (tuple): Tuple of ints Y & X.

    Returns:
        tuple: vect1 offset by vect2
    """
    return (vect1[0]+vect2[0], vect1[1]+vect2[1])

def _neighbors(pos):
    return [ _add_vect_2D(pos, dir_ ) for dir_ in list(DIRECTIONS.values())]

def _cell_neighbors(pos):
    return [ _add_vect_2D(pos, dir_ ) for dir_ in list(PRIM_DIRECTIONS.values())]
    
def _exits(node, image):
    exits = 0
    for n in _neighbors(node):
        try:
            if image.getpixel(n) == SYMBOLS["CLOSE"]: exits += 1
        except IndexError:
            continue
    return exits

def _good_node(pos, size):
    h, w = size
    x, y = pos
    return  not ((x < 0) or
        (y < 0) or
        (x > w) or
        (y > h))

def __main():
    args = _establish_cli()
    
    img = empty_maze( (args.width, args.height) )
    
    prim_no_vis(img)
    
    img.save("./maze.png")
    
    
    
    

if __name__ == "__main__":
    __main()
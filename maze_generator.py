# https://github.com/johnsliao/python-maze-generator/blob/master/maze.py


import random

from PIL import Image, ImageDraw

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


class Cell:
    def __init__(self):
        self.north = True
        self.south = True
        self.east = True
        self.west = True
        self.visited = False


class Maze:
    def __init__(self, width=20, height=20, cell_width=20):
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cells = [[Cell() for _ in range(height)] for _ in range(width)]
        self.visited_cells = []

    def generate(self):
        x, y = random.choice(range(self.width)), random.choice(range(self.height))
        self.visited_cells.append( self.cells[x][y] )
        path = [(x, y)]

        while not all(all(c for c in cell) for cell in self.cells):
            x, y = path[len(path) - 1][0], path[len(path) - 1][1]

            good_adj_cells = []
            if self.exists(x, y - 1) and not self.cells[x][y - 1].visited:
                good_adj_cells.append('north')
            if self.exists(x, y + 1) and not self.cells[x][y + 1].visited:
                good_adj_cells.append('south')
            if self.exists(x + 1, y) and not self.cells[x + 1][y].visited:
                good_adj_cells.append('east')
            if self.exists(x - 1, y) and not self.cells[x - 1][y].visited:
                good_adj_cells.append('west')

            if good_adj_cells:
                go = random.choice(good_adj_cells)
                if go == 'north':
                    self.cells[x][y].north = False
                    self.cells[x][y - 1].south = False
                    self.visited_cells.append( (x, y - 1) )
                    path.append((x, y - 1))
                if go == 'south':
                    self.cells[x][y].south = False
                    self.cells[x][y + 1].north = False
                    self.visited_cells.append( (x, y + 1) )
                    path.append((x, y + 1))
                if go == 'east':
                    self.cells[x][y].east = False
                    self.cells[x + 1][y].west = False
                    self.visited_cells.append( (x + 1, y) )
                    path.append((x + 1, y))
                if go == 'west':
                    self.cells[x][y].west = False
                    self.visited_cells.append( (x - 1, y) )
                    self.cells[x - 1][y].visited = True
                    path.append((x - 1, y))
            else:
                path.pop()

    def exists(self, x, y):
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return False
        return True

    def get_direction(self, direction, x, y):
        if direction == 'north':
            return x, y - 1
        if direction == 'south':
            return x, y + 1
        if direction == 'east':
            return x + 1, y
        if direction == 'west':
            return x - 1, y

    def draw(self):
        canvas_width, canvas_height = self.cell_width * self.width, self.cell_width * self.height
        im = Image.new('RGB', (canvas_width, canvas_height))
        draw = ImageDraw.Draw(im)
        
        draw.point(self.visited_cells[0], fill=SYMBOLS["START"])
        
        draw.point(self.visited_cells[-1], fill=SYMBOLS["END"])

        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y].north:
                    draw.line(
                        (x * self.cell_width, 
                        y * self.cell_width, 
                        (x + 1) * self.cell_width, 
                        y * self.cell_width),
                        fill=SYMBOLS["CLOSE"])
                if self.cells[x][y].south:
                    draw.line((x * self.cell_width, 
                            (y + 1) * self.cell_width, 
                            (x + 1) * self.cell_width,
                            (y + 1) * self.cell_width), 
                            fill=SYMBOLS["CLOSE"])
                if self.cells[x][y].east:
                    draw.line(((x + 1) * self.cell_width, 
                               y * self.cell_width, 
                               (x + 1) * self.cell_width,
                               (y + 1) * self.cell_width), 
                              fill=SYMBOLS["CLOSE"])
                if self.cells[x][y].west:
                    draw.line(
                        (x * self.cell_width, 
                        y * self.cell_width, 
                        x * self.cell_width, 
                        (y + 1) * self.cell_width),
                        fill=SYMBOLS["CLOSE"])

        im.show()


if __name__ == '__main__':
    maze = Maze()
    maze.generate()
    maze.draw()
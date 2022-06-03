# Search
![Gif of a path being generated, slowly finding its way to several coins, and then finally an end node](https://github.com/VoxLight/BFSVisualizer/blob/master/gifs/rotate.gif?raw=true)
![Image of the completed shortest path](https://github.com/VoxLight/BFSVisualizer/blob/master/screenshots/rotate.png?raw=true)

## About
This is a tool used to visualize the process of BFS path finding.
This tool takes in PNG images.

Color Codes:
* BLACK (0, 0, 0): Open spaces that can be traversed.
* RED (255, 0, 0): Closed spaces that cannot be traversed.
* GREEN (0, 255, 0): Goal/End; the final node the path needs to travel to.
* BLUE (0, 0, 255): Start; the first node the path travels from.
* YELLOW (255, 255, 0) "Coins"; goal nodes that first need to be reached before trabveling to the End node. (optional).


Any image editor that allows you to create pixel art and precisly set color values will work when creating images for 
this tool. A web tool I reccomend is [this](https://www.pixilart.com/).

Images MUST have an aspect ratio of 1:1 or there will be stretching! You can create larger images and then block off sections to re-create a wonky aspect ratio.

Examples can be found in the `mazes` directory.

## Installation

This is a CLI. Clone/download the repo and move to the directory inside of your terminal.

```
py -m pip install -r requirements.txt
```


## Usage

for help
```
py BFSVisualizer.py -h
>>>>usage: BFSVisualizer.py [-h] [-fps [FPS]] [-size [SIZE]] [-scr [SCR]] [-gif [GIF]] [maze_fp]

Get the maze file path, configs, and flags.

positional arguments:
  maze_fp       filepath of the maze to generate a path for.

optional arguments:
  -h, --help    show this help message and exit
  -fps [FPS]    framerate of the loop. (defaul is 60)
  -size [SIZE]  height of the pygame surface (aspect ration 1:1). (defaul is 800)
  -scr [SCR]    filepath to save a screenshot of the completed path. will not save if not provided.
  -gif [GIF]    filepath to save frames in a subdir and then compile them into a gif.


```

```
py BFSVisualizer.py -fps 60 -size 1000 "./mazes/small.png"
```

`fps` is the allowed speed of the main loop.
`size` is the resolution of the pygame surface ( sizexsize ). An aspect ration of 1:1 is required.
The filepath is the path to your maze image.

Here is the command I used to generate the media above.

gifs/rotate.gif
```
py BFSVisualizer.py "./mazes/rotate.png" -fps 27.4 -gif "./gifs/rotate"
```

and screenshots/rotate.png

```
py BFSVisualizer.py "./mazes/rotate.png" -fps 27.4 -scr "./screenshots/rotate.png"
```

# Search

## About
This is a tool used to visualize the process of BFS path finding.
This tool takes in PNG images.

Color Codes:
    - BLACK (0, 0, 0): Open spaces that can be traversed.
    - RED (255, 0, 0): Closed spaces that cannot be traversed.
    - GREEN (0, 255, 0): Goal/End; the final node the path needs to travel to.
    - BLUE (0, 0, 255): Start; the first node the path travels from.
    - YELLOW (255, 255, 0) "Coins"; goal nodes that first need to be reached before trabveling to the End node. (optional).


Any image editor that allows you to create pixel art and precisly set color values will work when creating images for 
this tool. A web tool I reccomend is [this](https://www.pixilart.com/).

Images MUST have an aspect ratio of 1:1 or there will be stretching! You can create larger images and then block off sections to re-create a wonky aspect ratio.

Examples can be found in the `mazes` directory.


## Usage

```
py BFSVisualizer.py -fps 60 -size 1000 "./mazes/small.png"
```

`fps` is the allowed speed of the main loop.
`size` is the resolution of the pygame surface ( sizexsize ). An aspect ration of 1:1 is required.
The filepath is the path to your maze image.
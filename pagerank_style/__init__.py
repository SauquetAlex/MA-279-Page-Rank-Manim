"""Shared look for every PageRank animation.

Use it at the top of your scene file:

    from manim import *
    from pagerank_style import *

Change colors HERE (not in your own scene) so all our videos match.
"""

from manim import config

BLACK = "#000000"  # black
WHITE = "#FFFFFF"  # white
LIGHT_GRAY = "#BBBBBB"  # light grey
BLUE = "#58C4DD"  # 3b1b blue
YELLOW = "#FFFF00"  # 3b1b yellow
RED = "#FC6255"  # 3b1b red
GREEN = "#83C167"  # 3b1b green


BACKGROUND = BLACK
TEXT_COLOR = WHITE
ACCENT = BLUE
HIGHLIGHT = YELLOW

# Graph drawing (used by pagerank_style.graph)
PAGE_COLORS = [BLUE, YELLOW, RED, GREEN]
NODE_RADIUS = 0.45
NODE_STROKE_WIDTH = 6
EDGE_COLOR = "#BBBBBB"  # light grey
EDGE_STROKE_WIDTH = 3
EDGE_BOLD_STROKE_WIDTH = 7
EDGE_LABEL_FONT_SIZE = 24
EDGE_LABEL_BOLD_STROKE_WIDTH = 1.2

config.background_color = BACKGROUND

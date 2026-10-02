"""Shared look for every PageRank animation.

Use it at the top of your scene file:

    from manim import *
    from pagerank_style import *

Change colors HERE (not in your own scene) so all our videos match.
"""

from pathlib import Path

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

# Random surfer (used by pagerank_style.surfer)
SURFER_COLOR = WHITE
SURFER_RADIUS = 0.12
SURFER_STEP_TIME = 1.2  # seconds per click

# Google search page (used by pagerank_style.search), Google's dark-mode look
LOGOS = Path(__file__).resolve().parents[1] / "assets" / "logos"
SEARCH_FONT = "Arial"
SEARCH_BAR_FILL = "#303134"  # search bar, cards, letter icons
LINK_BLUE = "#8AB4F8"  # result titles
URL_GRAY = "#BDC1C6"  # urls, magnifier, arrows
SNIPPET_GRAY = "#9AA0A6"  # result descriptions
SEARCH_WIDTH = 8.5  # width of the search bar / results column
SEARCH_PAGE_HEIGHT = 6.4  # whole page (logo to last result) is scaled to this

config.background_color = BACKGROUND

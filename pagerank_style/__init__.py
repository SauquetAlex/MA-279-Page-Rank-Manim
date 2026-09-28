"""Shared look for every PageRank animation.

Use it at the top of your scene file:

    from manim import *
    from pagerank_style import *

Change colors HERE (not in your own scene) so all our videos match.
"""

from manim import config

BACKGROUND = "#000000"  # black
TEXT_COLOR = "#FFFFFF"  # white
ACCENT = "#58C4DD"      # 3b1b blue
HIGHLIGHT = "#FFFF00"   # 3b1b yellow

config.background_color = BACKGROUND

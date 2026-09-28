"""Abbas's starter scene.

Render:  uv run manim -pql scenes/abbas/hello.py Hello
"""

from manim import *
from pagerank_style import *


class Hello(Scene):
    def construct(self):
        title = Text("Hello World", color=TEXT_COLOR)
        self.play(Write(title))
        self.wait(1)

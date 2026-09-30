"""Random surfer explanation of PageRank.

Render:  uv run manim -pql scenes/alex/random_surfer.py RandomSurfer
"""

from manim import *

from pagerank_style import *
from pagerank_style.graph import PageGraph

# TRANSITIONS[u][v] = probability the surfer clicks from page u to page v.
TRANSITIONS = {
    "A": {"A": 0.10, "B": 0.50, "C": 0.25, "D": 0.15},
    "B": {"A": 0.30, "C": 0.70},
    "C": {"A": 0.80, "D": 0.20},
    "D": {"B": 0.50, "C": 0.50},
}

POSITIONS = {
    "A": 2 * LEFT + 1.8 * UP,
    "B": 2 * RIGHT + 1.8 * UP,
    "C": 2 * RIGHT + 1.8 * DOWN,
    "D": 2 * LEFT + 1.8 * DOWN,
}


class RandomSurfer(Scene):
    def construct(self):
        graph = PageGraph(TRANSITIONS, POSITIONS)

        self.play(
            LaggedStart(
                *[GrowFromCenter(n) for n in graph.nodes.values()], lag_ratio=0.2
            )
        )
        self.play(*[Create(e) for e in graph.edges.values()])
        self.wait(3)

        self.play(graph.bold_outgoing("A"))
        self.wait(4)
        self.play(graph.unbold_all())
        self.wait(1)

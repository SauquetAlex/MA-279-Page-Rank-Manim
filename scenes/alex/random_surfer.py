"""Random surfer explanation of PageRank.

Render:  uv run manim -pql scenes/alex/random_surfer.py RandomSurfer
"""

from manim import *
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    LaggedStart,
    Scene,
)

from pagerank_style import *
from pagerank_style.graph import PageGraph
from pagerank_style.surfer import Surfers

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

NUM_SURFERS = 3


class RandomSurfer(Scene):
    def construct(self):
        graph = PageGraph(TRANSITIONS, POSITIONS)

        self.play(
            LaggedStart(
                *[GrowFromCenter(n) for n in graph.nodes.values()], lag_ratio=0.2
            )
        )
        self.play(*[e.draw() for e in graph.edges.values()])
        self.wait(3)

        self.play(graph.bold_outgoing("A"))
        self.wait(4)
        self.play(graph.unbold_all())
        self.wait(1)

        # "Animation with clicks following pages"
        letters = VGroup(*[node.letter for node in graph.nodes.values()])

        # One surfer, starting on A
        surfer = Surfers(graph, ["A"], seed=0)
        self.play(FadeIn(surfer, scale=0.5), letters.animate.set_opacity(0.5))
        for _ in range(10):
            self.play(surfer.step())
        self.wait()
        self.play(FadeOut(surfer))
        self.wait()

        # 3 surfers start on every page
        surfers = Surfers(
            graph, [page for page in POSITIONS for _ in range(NUM_SURFERS)], seed=1
        )
        self.play(FadeIn(surfers, scale=0.5))
        for _ in range(20):
            self.play(surfers.step())
        self.wait()
        self.play(FadeOut(surfers), letters.animate.set_opacity(1))

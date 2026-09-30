"""A random surfer: a dot that clicks links on a PageGraph.

    from pagerank_style.surfer import Surfer

    surfer = Surfer(graph, "A", seed=0)
    self.play(FadeIn(surfer))
    self.play(surfer.walk_to("B"))   # follow the A -> B link
    self.play(surfer.step())         # pick a random link from the current page
"""

import random

from manim import *

from pagerank_style import BACKGROUND, SURFER_COLOR, SURFER_RADIUS, SURFER_STEP_TIME


class Surfer(Dot):
    """Rests on the edge of its current page's circle, at `angle`."""

    def __init__(self, graph, page, angle=PI / 4, seed=None, **kwargs):
        super().__init__(
            radius=SURFER_RADIUS,
            color=SURFER_COLOR,
            stroke_color=BACKGROUND,  # thin dark ring so it stands out on arrows
            stroke_width=2,
            **kwargs,
        )
        self.graph = graph
        self.page = page
        self.angle = angle
        self.rng = random.Random(seed)
        self.move_to(self.rest_point(page))

    def rest_point(self, page):
        node = self.graph.nodes[page]
        return node.get_center() + node.radius * rotate_vector(RIGHT, self.angle)

    def choose_next(self):
        """Pick the next page with the link probabilities of the current page."""
        row = self.graph.transitions[self.page]
        return self.rng.choices(list(row), weights=list(row.values()))[0]

    def walk_to(self, page, run_time=SURFER_STEP_TIME, **kwargs):
        """Animation: follow the link from the current page to `page`."""
        arrow = self.graph.edges[self.page, page].arrow
        start, end = self.rest_point(self.page), self.rest_point(page)
        path = VMobject()
        path.set_points_as_corners([start, arrow.points[0]])
        path.append_points(arrow.points)  # the arrow's curve, without its tip
        path.append_points(Line(arrow.points[-1], end).points)
        self.page = page
        return MoveAlongPath(self, path, run_time=run_time, **kwargs)

    def step(self, **kwargs):
        """Animation: click a random link from the current page."""
        return self.walk_to(self.choose_next(), **kwargs)

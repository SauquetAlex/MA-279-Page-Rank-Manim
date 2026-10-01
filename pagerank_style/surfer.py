"""Random surfers: dots that click links on a PageGraph, all at the same time.

    from pagerank_style.surfer import Surfers

    surfers = Surfers(graph, ["A", "B", "C"], seed=0)   # one dot per start page
    self.play(FadeIn(surfers))
    self.play(surfers.step())   # every surfer clicks a random link

Surfers on the same page sit inside its circle: 1 in the middle, 2 side by
side, 3 in a triangle, and so on.
"""

import random

from manim import *

from pagerank_style import BACKGROUND, SURFER_COLOR, SURFER_RADIUS, SURFER_STEP_TIME


class Surfer(Dot):
    def __init__(self, page, **kwargs):
        super().__init__(
            radius=SURFER_RADIUS,
            color=SURFER_COLOR,
            stroke_color=BACKGROUND,  # thin dark ring so touching dots stay apart
            stroke_width=2,
            **kwargs,
        )
        self.page = page
        self.set_z_index(2)  # above the nodes (z_index 1) it sits in


class Surfers(VGroup):
    def __init__(self, graph, pages, seed=None, **kwargs):
        super().__init__(*[Surfer(page) for page in pages], **kwargs)
        self.graph = graph
        self.rng = random.Random(seed)
        for surfer, point in zip(self, self.spots(pages)):
            surfer.move_to(point)

    def spots(self, pages):
        """Where each surfer sits when the surfers are on `pages`."""
        points = []
        for i, page in enumerate(pages):
            k = pages.count(page)  # surfers sharing this page
            j = pages[:i].count(page)  # this surfer's place among them
            ring = 0 if k == 1 else max(0.15, 0.045 * k)  # wide enough not to overlap
            offset = rotate_vector(
                UP, TAU * j / k
            )  # first at the top: triangle points up
            points.append(self.graph.nodes[page].get_center() + ring * offset)
        return points

    def choose_next(self, page):
        """Pick the next page with the link probabilities of `page`."""
        row = self.graph.transitions[page]
        return self.rng.choices(list(row), weights=list(row.values()))[0]

    def walk_to(self, pages, run_time=SURFER_STEP_TIME, **kwargs):
        """Animation: surfer i follows the link to pages[i]."""
        moves = []
        for surfer, page, end in zip(self, pages, self.spots(pages)):
            arrow = self.graph.edges[surfer.page, page].arrow
            path = VMobject()
            path.set_points_as_corners([surfer.get_center(), arrow.points[0]])
            path.append_points(arrow.points)  # the arrow's curve, without its tip
            path.append_points(Line(arrow.points[-1], end).points)
            surfer.page = page
            moves.append(MoveAlongPath(surfer, path))
        return AnimationGroup(*moves, run_time=run_time, **kwargs)

    def step(self, **kwargs):
        """Animation: every surfer clicks a random link from its page."""
        return self.walk_to([self.choose_next(s.page) for s in self], **kwargs)

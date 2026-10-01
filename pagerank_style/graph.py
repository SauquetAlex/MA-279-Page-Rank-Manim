"""Shared pieces for drawing a web graph: pages (nodes) and links (edges).

    from pagerank_style.graph import *

    graph = PageGraph(transitions, positions)   # your own data, see below
    self.play(*[edge.draw() for edge in graph.edges.values()])
    graph.nodes["A"]                             # a PageNode
    graph.edges["A", "B"]                        # a LinkEdge (arrow + "50%")
    self.play(graph.bold_outgoing("A"))          # emphasize A's links
    self.play(graph.unbold_all())

transitions[u][v] is the probability of clicking from page u to page v
(u == v draws a self-loop). positions[u] is where page u goes on screen.
"""

from manim import *

from pagerank_style import (
    EDGE_BOLD_STROKE_WIDTH,
    EDGE_COLOR,
    EDGE_LABEL_BOLD_STROKE_WIDTH,
    EDGE_LABEL_FONT_SIZE,
    EDGE_STROKE_WIDTH,
    NODE_RADIUS,
    NODE_STROKE_WIDTH,
    PAGE_COLORS,
    TEXT_COLOR,
)

PAIR_OFFSET = 0.15  # sideways shift so A->B and B->A don't overlap
LABEL_ALONG = 0.35  # label position along the edge (off-center so crossing diagonals don't collide)


def draw_arrow(arrow, **kwargs):
    """Animation: draw an arrow (straight or curved) with its tip riding along.

    Create(arrow) draws the shaft first and the tip after it, so the tip
    pops in late at the very end of the animation.
    """
    shaft = arrow.copy()
    tip = shaft.tip
    shaft.remove(tip)  # not pop_tips(): that stretches the shaft over the tip

    def update(mob, alpha):
        mob.pointwise_become_partial(shaft, 0, alpha)
        mob.tip.become(tip)
        end, handle = mob.points[-1], mob.points[-2]
        if alpha > 0 and not np.allclose(end, handle):
            mob.tip.rotate(
                angle_of_vector(end - handle) - tip.tip_angle, about_point=tip.base
            )
        mob.tip.shift(end - tip.base)
        mob.tip.scale(min(1, 5 * alpha), about_point=end)  # grow in at the start

    return UpdateFromAlphaFunc(arrow, update, rate_func=smooth, **kwargs)


class PageNode(VGroup):
    """A page: colored circle with its name in the middle."""

    def __init__(self, name, color, radius=NODE_RADIUS, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.color = color
        self.radius = radius
        self.circle = Circle(radius=radius, color=color, stroke_width=NODE_STROKE_WIDTH)
        self.circle.set_fill(BLACK, opacity=1)
        self.letter = Text(name, color=TEXT_COLOR, weight=BOLD).scale(0.8)
        self.add(self.circle, self.letter)


class LinkEdge(VGroup):
    """Arrow from one PageNode to another, with its probability as a label.

    If start is end, draws a small loop on the side given by `loop_direction`.
    `offset` shifts a straight arrow to its right (for two-way links).
    """

    def __init__(self, start, end, prob, offset=0.0, loop_direction=UP, **kwargs):
        super().__init__(**kwargs)
        self.start, self.end, self.prob = start, end, prob
        if start is end:
            self.arrow = self._make_loop(start, loop_direction)
        else:
            self.arrow = self._make_arrow(start, end, offset)
        self.label = self._make_label()
        self.add(self.arrow, self.label)

    @staticmethod
    def _make_arrow(start, end, offset):
        a, b = start.get_center(), end.get_center()
        right = rotate_vector(normalize(b - a), -PI / 2)
        return Arrow(
            a + offset * right,
            b + offset * right,
            buff=start.radius + 0.05,
            color=EDGE_COLOR,
            stroke_width=EDGE_STROKE_WIDTH,
            tip_length=0.2,
            max_tip_length_to_length_ratio=1,
            max_stroke_width_to_length_ratio=100,
        )

    @staticmethod
    def _make_loop(node, direction, loop_radius=0.3):
        direction = normalize(direction)
        loop = Arc(
            radius=loop_radius,
            start_angle=angle_of_vector(-direction) + 0.9,
            angle=TAU - 1.8,
            arc_center=node.get_center()
            + direction * (node.radius + loop_radius * 0.6),
            color=EDGE_COLOR,
            stroke_width=EDGE_STROKE_WIDTH,
        )
        loop.add_tip(tip_length=0.15, tip_width=0.15)
        return loop

    def _make_label(self):
        label = Text(
            f"{round(self.prob * 100)}%",
            color=TEXT_COLOR,
            font_size=EDGE_LABEL_FONT_SIZE,
        )
        if self.start is self.end:  # far side of the loop
            center = self.arrow.get_arc_center()
            label.move_to(
                center + 1.9 * (self.arrow.point_from_proportion(0.5) - center)
            )
        else:
            right = rotate_vector(
                normalize(self.arrow.get_end() - self.arrow.get_start()), -PI / 2
            )
            label.next_to(
                self.arrow.point_from_proportion(LABEL_ALONG), right, buff=0.1
            )
        return label

    def draw(self, **kwargs):
        """Animation: draw the arrow and write the label.

        Use this instead of Create(edge): Create on Text fills half-traced
        glyphs, so the letters look jagged while they appear. Write defaults
        to linear timing, so it is eased like Create to finish in step.
        """
        return AnimationGroup(
            draw_arrow(self.arrow), Write(self.label, rate_func=smooth), **kwargs
        )

    def bold(self, color=TEXT_COLOR):
        """Animation: thicker, brighter arrow and bold label.

        The label is thickened with an outline (not a bold font) so the
        letters grow smoothly instead of morphing into new glyphs.
        """
        return AnimationGroup(
            self.arrow.animate.set_stroke(width=EDGE_BOLD_STROKE_WIDTH).set_color(
                color
            ),
            self.label.animate.set_stroke(
                TEXT_COLOR, width=EDGE_LABEL_BOLD_STROKE_WIDTH
            ),
        )

    def unbold(self):
        """Animation: back to the normal look."""
        return AnimationGroup(
            self.arrow.animate.set_stroke(width=EDGE_STROKE_WIDTH).set_color(
                EDGE_COLOR
            ),
            self.label.animate.set_stroke(width=0),
        )


class PageGraph(VGroup):
    """Pages and links built from a transitions table and page positions."""

    def __init__(self, transitions, positions, colors=PAGE_COLORS, **kwargs):
        super().__init__(**kwargs)
        self.transitions = transitions
        self.nodes = {
            name: PageNode(name, colors[i % len(colors)]).move_to(pos)
            for i, (name, pos) in enumerate(positions.items())
        }

        center = np.mean(list(positions.values()), axis=0)
        self.edges = {}
        for u, row in transitions.items():
            for v, prob in row.items():
                two_way = u != v and u in transitions.get(v, {})
                self.edges[u, v] = LinkEdge(
                    self.nodes[u],
                    self.nodes[v],
                    prob,
                    offset=PAIR_OFFSET if two_way else 0.0,
                    loop_direction=positions[u] - center,  # loops point outward
                )

        # nodes on top of edges, even when the edges are animated in later
        for node in self.nodes.values():
            node.set_z_index(1)
        self.add(*self.edges.values(), *self.nodes.values())

    def outgoing(self, name):
        return [edge for (u, _), edge in self.edges.items() if u == name]

    def bold_outgoing(self, name):
        """Animation: bold every link leaving `name`."""
        return AnimationGroup(*[edge.bold() for edge in self.outgoing(name)])

    def unbold_all(self):
        return AnimationGroup(*[edge.unbold() for edge in self.edges.values()])

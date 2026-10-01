"""A plot of each page's PageRank over the iterations, one line per page.

    from pagerank_style.plot import RankPlot

    plot = RankPlot(graph).to_edge(RIGHT)
    self.play(FadeIn(plot))   # axes, labels and values; the lines start empty
    self.play(surfers.step(), plot.step())   # draw iteration 0 -> 1, and so on

The values are not counted from the surfers: they come from multiplying the
start vector [1/n, ..., 1/n] by the link-probability matrix, once per step.
"""

from manim import *

from pagerank_style import SURFER_STEP_TIME, TEXT_COLOR


class RankPlot(VGroup):
    def __init__(self, graph, steps=20, **kwargs):
        super().__init__(**kwargs)
        pages = list(graph.nodes)
        matrix = np.array(
            [[graph.transitions[u].get(v, 0) for v in pages] for u in pages]
        )
        ranks = [np.full(len(pages), 1 / len(pages))]
        for _ in range(steps):
            ranks.append(ranks[-1] @ matrix)  # one click for everyone at once
        self.ranks = dict(zip(pages, np.array(ranks).T))  # ranks[page][t]
        self.steps = steps
        self.t = 0

        self.axes = Axes(
            x_range=[0, steps, 5],
            y_range=[0, 0.5, 0.1],
            x_length=4.5,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 24},
        )
        # axis labels lined up with the end of their axis line
        x_label = Text("Iteration", font_size=24, color=TEXT_COLOR)
        x_label.next_to(self.axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = Text("PageRank", font_size=24, color=TEXT_COLOR)
        y_label.next_to(self.axes.y_axis.get_end(), UP, buff=0.2)

        self.lines = {page: VMobject(color=graph.nodes[page].color) for page in pages}

        # current value of every page, in its color, under the plot
        self.values = {
            page: DecimalNumber(self.ranks[page][0], num_decimal_places=3, font_size=28)
            for page in pages
        }
        row = VGroup(
            *[
                VGroup(Tex(page, font_size=28), self.values[page])  # LaTeX, like the digits
                .arrange(RIGHT, buff=0.15)
                .set_color(graph.nodes[page].color)
                for page in pages
            ]
        ).arrange(RIGHT, buff=0.5)
        row.next_to(self.axes, DOWN, buff=0.4)
        row.set_x(self.axes.c2p(steps / 2, 0)[0])  # centered on the x-axis line

        self.add(self.axes, x_label, y_label, row, *self.lines.values())
        self.center()  # the values row hangs below, so recenter the whole plot

    def curve(self, page):
        """The full line of `page`, from iteration 0 to the last one."""
        return VMobject().set_points_as_corners(
            [self.axes.c2p(t, r) for t, r in enumerate(self.ranks[page])]
        )

    def step(self, run_time=SURFER_STEP_TIME, **kwargs):
        """Animation: extend every line by one iteration and update the values."""
        start, end = self.t / self.steps, (self.t + 1) / self.steps
        self.t += 1

        def grow(page):
            curve = self.curve(page)  # built now, so it follows the plot if moved
            return UpdateFromAlphaFunc(
                self.lines[page],
                lambda line, a: line.pointwise_become_partial(
                    curve, 0, start + a * (end - start)
                ),
            )

        counts = [
            ChangeDecimalToValue(number, self.ranks[page][self.t])
            for page, number in self.values.items()
        ]
        return AnimationGroup(
            *[grow(p) for p in self.lines], *counts, run_time=run_time, **kwargs
        )

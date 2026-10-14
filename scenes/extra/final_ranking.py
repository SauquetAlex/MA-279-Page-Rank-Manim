"""Final ranking (end of math part 2): "the final ranking is ...".

Plays after Alex's RandomSurfer: the same web, each page grows to its
PageRank, and the pages line up as a ranked bar chart.

Render:  uv run manim -pql scenes/extra/final_ranking.py FinalRanking
"""

from manim import *

from pagerank_style import *
from pagerank_style.graph import PageGraph

# Same web as Alex's RandomSurfer
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

BAR_MAX_WIDTH = 5  # width of a bar at 50%


def pagerank(transitions, steps=200):
    """Where the surfers end up: [1/n, ...] times the link matrix, many times."""
    pages = list(transitions)
    matrix = np.array([[transitions[u].get(v, 0) for v in pages] for u in pages])
    ranks = np.full(len(pages), 1 / len(pages))
    for _ in range(steps):
        ranks = ranks @ matrix
    return dict(zip(pages, ranks))


class FinalRanking(Scene):
    def construct(self):
        graph = PageGraph(TRANSITIONS, POSITIONS)
        self.add(graph)
        self.wait()

        ranks = pagerank(TRANSITIONS)
        order = sorted(ranks, key=ranks.get, reverse=True)

        # every page grows to its rank (area ~ rank; the average page stays put)
        self.play(
            *[
                node.animate.scale(np.sqrt(ranks[name] * len(ranks)))
                for name, node in graph.nodes.items()
            ],
            run_time=2,
        )
        values = VGroup(
            *[
                Text(f"{ranks[n] * 100:.1f}%", font_size=30, color=graph.nodes[n].color)
                .next_to(graph.nodes[n], LEFT if POSITIONS[n][0] < 0 else RIGHT, buff=0.2)
                for n in graph.nodes
            ]
        )
        self.play(FadeIn(values))
        self.wait(2)

        # "And the final ranking is ..."
        self.play(
            graph.animate.scale(0.6).to_edge(LEFT, buff=0.6),
            FadeOut(values),
        )
        title = Text("Final ranking", font_size=40, color=TEXT_COLOR)
        rows = VGroup()
        for place, name in enumerate(order, start=1):
            color = graph.nodes[name].color
            num = Text(f"{place}.", font_size=34, color=TEXT_COLOR)
            badge = Circle(radius=0.3, color=color, stroke_width=5)
            badge.set_fill(BLACK, 1)
            badge_letter = Text(name, font_size=28, color=TEXT_COLOR, weight=BOLD).move_to(badge)
            bar = Rectangle(
                width=BAR_MAX_WIDTH * ranks[name] / 0.5,
                height=0.4,
                stroke_width=0,
                fill_color=color,
                fill_opacity=0.85,
            )
            value = Text(f"{ranks[name] * 100:.1f}%", font_size=28, color=color)
            row = VGroup(num, VGroup(badge, badge_letter), bar, value)
            row.arrange(RIGHT, buff=0.25)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        # bars start at the same x
        bar_x = max(r[1].get_right()[0] for r in rows) + 0.25
        for r in rows:
            r[2].align_to([bar_x, 0, 0], LEFT)
            r[3].next_to(r[2], RIGHT, buff=0.2)
        VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(
            3 * RIGHT
        )

        self.play(Write(title))
        for name, row in zip(order, rows):
            num, badge, bar, value = row
            self.play(
                TransformFromCopy(graph.nodes[name], badge),
                FadeIn(num),
                GrowFromEdge(bar, LEFT),
                FadeIn(value),
                run_time=0.9,
            )
        self.wait(4)
        self.play(FadeOut(Group(*self.mobjects)))

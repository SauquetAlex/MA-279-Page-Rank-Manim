"""Math part 1: why counting keywords or links isn't enough, and the graph model.

Plays after Johnny's intro and right before Alex's RandomSurfer. Each scene
matches one "**...**" note in the script, in order:

    KeywordRanking   two pages ranked by how often they say the keyword
    KeywordStuffing  the same pages, after the second one stuffs keywords
    LinkRanking      the same pages ranked by how many sites link to them
    LinkSpam         spam sites pile links onto the second page
    CircularProblem  "only relevant pages should count" needs relevance itself
    TrafficModel     the way out: model random web traffic
    GraphModel       the web as pages (nodes) and links (arrows with probabilities)

Every scene is timed to Abbas's voiceover (assets/audio/math_part1_voiceover.m4a).
VO holds when each scene starts in the voiceover, and each `self.at(t)` waits
until second t of the voiceover, so the animation lands on the spoken words
quoted next to it. GAPS lengthens chosen pauses of the recording (the part
runs 2:00); both the scenes and join_voiceover.py apply it. To retime after a
new recording, edit only these numbers.

Render one:  uv run manim -pql scenes/abbas/math_part1.py KeywordRanking
Render all:  uv run manim -qh scenes/abbas/math_part1.py -a
Join with the voiceover:  uv run python scenes/abbas/join_voiceover.py
"""

from manim import *

from pagerank_style import *
from pagerank_style.graph import PageGraph, draw_arrow
import pagerank_style.search as search
from pagerank_style.search import LinkCard, link_arrows, magnifier
from pagerank_style.timing import TimedScene
from pagerank_style.webpage import WebPage, page_text

KEYWORD = "jaguar"

GOOD_PAGE = (
    "jaguarfacts.org",
    "All About Jaguars",
    "The jaguar is the largest cat in\n"
    "the Americas. A jaguar's bite is\n"
    "the strongest of any big cat, and\n"
    "every jaguar has its own spots.\n"
    "Learn where the jaguar lives, what\n"
    "a jaguar eats, and why the jaguar\n"
    "is near threatened.",
)

WEAK_PAGE = (
    "bobs-cat-blog.net",
    "Bob's Cat Blog",
    "My cat Whiskers looks like a tiny\n"
    "jaguar when she pounces. Next\n"
    "week: a review of a jaguar plush.",
)

STUFFING = "\n".join(["jaguar jaguar jaguar jaguar"] * 3)  # 12 hidden copies

HIDDEN = "#26272A"  # almost the page background: text readers can't see

# Same web as Alex's RandomSurfer, so this scene hands straight over to it.
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

# Second of the voiceover where each scene starts (the last entry is the end).
VO = {
    "KeywordRanking": 0.0,
    "KeywordStuffing": 19.3,  # "This seems a little too naive"
    "LinkRanking": 33.4,  # "We can also try to measure relevance..."
    "LinkSpam": 39.5,  # "However, once again..."
    "CircularProblem": 52.1,  # "So really, we should only care about..."
    "TrafficModel": 68.7,  # "However, it turns out..."
    "GraphModel": 80.3,  # "To do this, think of the web..."
    "end": 96.8,  # 1.5 s after the last word
}

# Extra silence added to the voiceover so the part runs exactly 2:00:
# (second of the recording, inside one of its pauses; seconds of silence added).
# Times in VO and self.at() stay in recording time; TimedScene shifts them.
GAPS = [
    (6.8, 2.5),  # after "...the keywords appear"
    (18.5, 3.0),  # after "...mentioning two times": the #1 / #2 badges
    (31.5, 3.0),  # after the stuffing sentence: Bob crossed out
    (38.5, 2.5),  # after "...endorse via links": the #1 / #2 badges
    (50.5, 3.0),  # after the spam sentence: Bob takes #1
    (56.4, 2.0),  # before "But now we run into a problem"
    (65.5, 2.0),  # before "This seems sort of circular"
    (68.0, 2.2),  # after "...circular": hold "Circular?"
    (79.6, 2.0),  # after "...determining page rank"
    (89.6, 1.0),  # before "We will label the arrow..."
]


BOB_LIFT = 1.0  # LinkSpam: how far Bob's page moves up before the spam arrives
LEFT_SLOT = 3.4 * LEFT + 0.6 * DOWN
RIGHT_SLOT = 3.4 * RIGHT + 0.6 * DOWN


def search_header(query):
    """Small search bar at the top of the screen with `query` typed in."""
    bar = RoundedRectangle(
        corner_radius=0.25,
        width=4.5,
        height=0.5,
        stroke_width=0,
        fill_color=SEARCH_BAR_FILL,
        fill_opacity=1,
    )
    icon = magnifier().move_to(bar).align_to(bar, LEFT).shift(0.25 * RIGHT)
    text = page_text(query, 24).next_to(icon, RIGHT, buff=0.2)
    return VGroup(bar, icon, text).to_edge(UP, buff=0.35)


def rank_badge(n, color=HIGHLIGHT):
    return Text(f"#{n}", color=color, weight=BOLD, font_size=44)


def score_line(label, value, color=TEXT_COLOR):
    """`label` followed by a number that can count up, e.g. "jaguar" x 6."""
    number = Integer(value, font_size=40, color=color)
    row = VGroup(Text(label, font_size=30, color=color), number).arrange(
        RIGHT, buff=0.25
    )
    return row, number


def keyword_pages():
    good = WebPage(*GOOD_PAGE, keyword=KEYWORD, height=4.1)
    weak = WebPage(*WEAK_PAGE, keyword=KEYWORD, height=4.1)
    good.shift(LEFT_SLOT - good.frame.get_center())
    weak.shift(RIGHT_SLOT - weak.frame.get_center())
    return good, weak


def badges_over(slots):
    return VGroup(
        *[
            rank_badge(i + 1).move_to(slot + 2.5 * UP)
            for i, slot in enumerate(slots)
        ]
    )


class KeywordRanking(TimedScene):
    """"This page mentioning jaguar 6 times would rank higher than this one (2)"."""

    def construct(self):
        header = search_header(KEYWORD)
        good, weak = keyword_pages()

        # "An early simple approach ... rank sites by the frequency
        #  at which the keywords appear"
        self.at(1.0)
        self.play(FadeIn(header, shift=0.2 * DOWN))
        idea = Text("rank = how often the keyword appears", font_size=36)
        idea[:4].set_color(HIGHLIGHT)
        self.at(3.4)
        self.play(FadeIn(idea, shift=0.2 * UP))

        # "Here's a simple example to show why this approach might work"
        self.at(7.3)
        self.play(FadeOut(idea), run_time=0.5)
        self.play(FadeIn(good, shift=0.3 * UP), FadeIn(weak, shift=0.3 * UP))

        # "This page mentioning jaguar six times" / "...than this one mentioning two times"
        for page, t in ((good, 11.0), (weak, 14.4)):
            self.at(t)
            row, number = score_line(f'"{KEYWORD}" ×', 0, HIGHLIGHT)
            row.next_to(page, DOWN, buff=0.3)
            self.play(FadeIn(row), run_time=0.3)
            for word in page.keyword_words():
                self.play(
                    Indicate(word, color=HIGHLIGHT, scale_factor=1.3),
                    number.animate.set_value(number.get_value() + 1),
                    run_time=0.33,
                )

        # "would rank higher"
        self.at(16.3)
        badges = badges_over([LEFT_SLOT, RIGHT_SLOT])
        badges[1].set_color(LIGHT_GRAY)
        self.play(LaggedStart(*[FadeIn(b, scale=1.5) for b in badges], lag_ratio=0.4))
        self.end()


class KeywordStuffing(TimedScene):
    """Bob hides "jaguar" in invisible text and jumps to #1 without changing."""

    def construct(self):
        header = search_header(KEYWORD)
        good, weak = keyword_pages()
        good_row, good_n = score_line(f'"{KEYWORD}" ×', len(good.keyword_words()), HIGHLIGHT)
        weak_row, weak_n = score_line(f'"{KEYWORD}" ×', len(weak.keyword_words()), HIGHLIGHT)
        good_row.next_to(good, DOWN, buff=0.3)
        weak_row.next_to(weak, DOWN, buff=0.3)
        badges = badges_over([LEFT_SLOT, RIGHT_SLOT])
        badges[1].set_color(LIGHT_GRAY)
        self.add(header, good, weak, good_row, weak_row, badges)

        # "simply repeating the words in the content of a site"
        stuffing = page_text(STUFFING, 17, HIDDEN, line_spacing=1.2)
        stuffing.next_to(weak.body, DOWN, buff=0.2, aligned_edge=LEFT)
        self.at(23.5)
        self.play(Write(stuffing, run_time=1.2))

        # reveal the hidden text, and count every copy
        hidden_label = Text("hidden text", font_size=24, color=RED)
        box = SurroundingRectangle(stuffing, color=RED, buff=0.08)
        hidden_label.next_to(box, DOWN, buff=0.1).align_to(box, LEFT)  # in the empty space under the box
        self.play(Create(box), FadeIn(hidden_label), run_time=0.4)
        words = weak.keyword_words(stuffing)
        self.play(
            LaggedStart(*[w.animate.set_color(HIGHLIGHT) for w in words], lag_ratio=0.1),
            weak_n.animate.set_value(weak_n.get_value() + len(words)),
            run_time=1.3,
        )

        # "makes it easy to boost the rank of your page"
        self.at(26.5)
        self.play(FadeOut(box), FadeOut(hidden_label), run_time=0.3)
        bob = VGroup(weak, stuffing, weak_row)
        jag = VGroup(good, good_row)
        self.play(
            bob.animate.shift(LEFT_SLOT - RIGHT_SLOT),
            jag.animate.shift(RIGHT_SLOT - LEFT_SLOT),
            path_arc=PI / 2,
            run_time=1.2,
        )

        # "without changing the actual relevance of the site"
        self.at(28.5)
        cross = Cross(bob[0], stroke_color=RED, stroke_width=8)
        note = Text("Same page. No more relevant.", font_size=30, color=RED)
        note.next_to(header, DOWN, buff=0.15)
        self.play(Create(cross), FadeIn(note))

        self.at(VO["LinkRanking"] - 0.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        self.end()


def link_pages():
    """The two pages as compact windows, stacked on the right."""
    good = WebPage(GOOD_PAGE[0], GOOD_PAGE[1], "", width=3.4, height=1.3)
    weak = WebPage(WEAK_PAGE[0], WEAK_PAGE[1], "", width=3.4, height=1.3)
    good.move_to(1.2 * RIGHT + 1.6 * UP)
    weak.move_to(1.2 * RIGHT + 1.6 * DOWN)
    return good, weak


GOOD_LINKERS = [
    ("University", "purdue.edu", BLUE, "university.svg"),
    ("Government", "nps.gov", YELLOW, "government.svg", 0.9),  # wide icon: shrink
    ("National Geographic", "nationalgeographic.com", GREEN),
]
WEAK_LINKERS = [("Friend's Blog", "catlady.net", RED)]
NUM_SPAM = 5
LINK_CARD_WIDTH = 3.4  # wide enough for "National Geographic"
SPAM_CARD_WIDTH = 2.5


def link_layout():
    search.CARD_WIDTH = LINK_CARD_WIDTH  # LinkCard reads it when each card is built
    good, weak = link_pages()
    cards = VGroup(*[LinkCard(*l) for l in GOOD_LINKERS]).arrange(DOWN, buff=0.25)
    cards.move_to(4.5 * LEFT + good.get_y() * UP + 0.35 * UP)
    weak_cards = VGroup(*[LinkCard(*l) for l in WEAK_LINKERS])
    weak_cards.move_to(4.5 * LEFT + weak.get_y() * UP)
    good_arrows = link_arrows(cards, good, spread=0.3)
    weak_arrows = link_arrows(weak_cards, weak)
    return good, weak, cards, weak_cards, good_arrows, weak_arrows


def link_scores(good, weak, good_value, weak_value):
    rows = []
    for page, value in ((good, good_value), (weak, weak_value)):
        row, number = score_line("links in:", value, HIGHLIGHT)
        row.scale(0.8).next_to(page, DOWN, buff=0.15)
        rows.append((row, number))
    return rows


def side_badges(good, weak):
    badges = VGroup(rank_badge(1), rank_badge(2, LIGHT_GRAY))
    for badge, page in zip(badges, (good, weak)):
        badge.next_to(page, RIGHT, buff=0.35)
    return badges


class LinkRanking(TimedScene):
    """"Count how many pages endorse a page with links"."""

    def construct(self):
        good, weak, cards, weak_cards, good_arrows, weak_arrows = link_layout()

        # "We can also try to measure relevance by counting how many pages
        #  endorse via links"
        self.play(
            FadeIn(good, shift=0.2 * LEFT),
            FadeIn(weak, shift=0.2 * LEFT),
            LaggedStart(
                *[FadeIn(c, shift=0.2 * RIGHT) for c in (*cards, *weak_cards)],
                lag_ratio=0.2,
            ),
            run_time=1,
        )
        (good_row, good_n), (weak_row, weak_n) = link_scores(good, weak, 0, 0)
        self.play(FadeIn(good_row), FadeIn(weak_row), run_time=0.3)

        # "how many pages" ... "links"
        self.at(35.2)
        for arrow in good_arrows:
            self.play(
                GrowArrow(arrow),
                good_n.animate.set_value(good_n.get_value() + 1),
                run_time=0.45,
            )
        for arrow in weak_arrows:
            self.play(
                GrowArrow(arrow),
                weak_n.animate.set_value(weak_n.get_value() + 1),
                run_time=0.45,
            )

        # pause after "links"
        self.at(37.4)
        badges = side_badges(good, weak)
        self.play(LaggedStart(*[FadeIn(b, scale=1.5) for b in badges], lag_ratio=0.4))
        self.end()


class LinkSpam(TimedScene):
    """Bob makes a pile of empty sites that all link to him, and takes #1."""

    def construct(self):
        good, weak, cards, weak_cards, good_arrows, weak_arrows = link_layout()
        (good_row, good_n), (weak_row, weak_n) = link_scores(good, weak, 3, 1)
        badges = side_badges(good, weak)
        self.add(good, weak, cards, weak_cards, good_arrows, weak_arrows)
        self.add(good_row, weak_row, badges)

        # "However, once again, without actually making our page more relevant"
        # Bob's page moves up toward the middle, so the spam sites under it
        # are easy to see; the score row moves beside the badge, out of the arrows' way
        self.at(40.5)
        bob = VGroup(weak, weak_cards, weak_arrows, badges[1])
        self.play(
            bob.animate.shift(BOB_LIFT * UP),
            weak_row.animate.next_to(badges[1].copy().shift(BOB_LIFT * UP), RIGHT, buff=0.4),
            run_time=1.2,
        )

        # spam sites in a row under Bob's page (standard-width cards, so they fit)
        search.CARD_WIDTH = SPAM_CARD_WIDTH
        spam = VGroup(
            *[
                LinkCard(f"spam{i + 1}", f"spam{i + 1}.biz", LIGHT_GRAY).scale(0.72)
                for i in range(NUM_SPAM)
            ]
        ).arrange(RIGHT, buff=0.15)
        spam.next_to(weak, DOWN, buff=1.0).set_x(weak.get_x() - 0.3)
        spam_arrows = VGroup(
            *[
                Arrow(
                    s.get_top(),
                    weak.get_bottom() + (s.get_x() - weak.get_x()) * 0.25 * RIGHT,
                    buff=0.05,
                    color=URL_GRAY,
                    stroke_width=2,
                    tip_length=0.12,
                    max_tip_length_to_length_ratio=1,
                )
                for s in spam
            ]
        )
        # "we can boost its rank by simply proliferating sites that link to it"
        self.at(44.3)
        self.play(
            LaggedStart(*[FadeIn(s, scale=0.6) for s in spam], lag_ratio=0.08),
            run_time=1.1,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in spam_arrows], lag_ratio=0.1),
            weak_n.animate.set_value(1 + NUM_SPAM),
            run_time=1.4,
        )

        # "but that don't have any relevance of their own"
        self.at(47.4)
        zero = Text("each spam site: 0 links in", font_size=28, color=RED)
        zero.next_to(spam, DOWN, buff=0.3)
        self.play(spam.animate.set_opacity(0.4), FadeIn(zero))

        # pause: Bob's page takes #1
        self.at(49.3)
        top, bottom = badges[0].get_center(), badges[1].get_center()
        self.play(
            badges[0].animate.move_to(bottom).set_color(HIGHLIGHT),
            badges[1].animate.move_to(top).set_color(LIGHT_GRAY),
            path_arc=PI / 2,
            run_time=1.2,
        )

        self.at(VO["CircularProblem"] - 0.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        self.end()


class CircularProblem(TimedScene):
    """"Only relevant pages endorsing... but that needs relevance: circular"."""

    def construct(self):
        rank = Text("Rank of a page", font_size=38, color=ACCENT)
        needs = Text("links from\nrelevant pages", font_size=34, color=TEXT_COLOR)
        relevance = Text("how relevant\nthose pages are", font_size=34, color=TEXT_COLOR)
        same = Text("their rank!", font_size=40, color=HIGHLIGHT)

        rank.move_to(2.4 * UP)
        needs.move_to(3.6 * RIGHT + 1.2 * DOWN)
        relevance.move_to(3.6 * LEFT + 1.2 * DOWN)

        def arc(start, end):
            return CurvedArrow(start, end, angle=-PI / 3, color=LIGHT_GRAY, stroke_width=4)

        a1 = arc(rank.get_right() + 0.2 * RIGHT, needs.get_top() + 0.2 * UP)
        a2 = arc(needs.get_bottom() + 0.2 * DOWN, relevance.get_bottom() + 0.2 * DOWN)
        a3 = arc(relevance.get_top() + 0.2 * UP, rank.get_left() + 0.2 * LEFT)

        # "So really, we should only care about relevant pages endorsing via links"
        self.at(52.2)
        self.play(Write(rank))
        self.at(53.6)
        self.play(Create(a1), run_time=0.8)
        self.play(Write(needs))

        # "whatever means of measuring this would require a measure of relevance"
        self.at(60.3)
        self.play(Create(a2), run_time=0.8)
        self.play(Write(relevance))

        # "precisely what we're trying to find"
        self.at(63.2)
        same.move_to(relevance)
        self.play(ReplacementTransform(relevance, same))
        self.play(Create(a3), run_time=0.8)
        self.play(
            *[Indicate(m, color=HIGHLIGHT) for m in (a1, a2, a3)],
            run_time=1.2,
        )

        # "This seems sort of circular"
        self.at(66.4)
        question = Text("Circular?", font_size=56, color=RED).move_to(0.3 * DOWN)
        self.play(FadeIn(question, scale=1.5))

        # "However, it turns out..."
        self.at(68.2)
        self.play(FadeOut(VGroup(rank, needs, same, a1, a2, a3, question)), run_time=0.5)
        self.end()


class TrafficModel(TimedScene):
    """"By modelling random website traffic according to users following links,
    on average this converges to a useful metric for determining page rank"."""

    def construct(self):
        steps = VGroup(
            Text("Model random web traffic", font_size=38),
            Text("Users follow links at random", font_size=38),
            Text("On average, it settles down", font_size=38),
            Text("A useful ranking: PageRank", font_size=38, color=HIGHLIGHT),
        ).arrange(DOWN, buff=0.85)
        arrows = VGroup(
            *[
                Arrow(a.get_bottom(), b.get_top(), buff=0.1, color=LIGHT_GRAY)
                for a, b in zip(steps, steps[1:])
            ]
        )

        # "by modelling random website traffic"
        self.at(70.4)
        self.play(FadeIn(steps[0], shift=0.2 * DOWN))
        # "according to users following links"
        self.at(72.5)
        self.play(GrowArrow(arrows[0]), FadeIn(steps[1], shift=0.2 * DOWN))
        # "on average, this converges"
        self.at(75.1)
        self.play(GrowArrow(arrows[1]), FadeIn(steps[2], shift=0.2 * DOWN))
        # "to a useful metric for determining page rank"
        self.at(77.0)
        self.play(GrowArrow(arrows[2]), FadeIn(steps[3], shift=0.2 * DOWN))
        self.play(Circumscribe(steps[3], color=HIGHLIGHT))

        self.at(VO["GraphModel"] - 0.6)
        self.play(FadeOut(VGroup(steps, arrows)), run_time=0.6)
        self.end()


class GraphModel(TimedScene):
    """"Think of the web as nodes (pages) and arrows (links) labeled with the
    probability that a random link is clicked."""

    def construct(self):
        graph = PageGraph(TRANSITIONS, POSITIONS)
        nodes = graph.nodes
        edges = graph.edges

        # "think of the web as a collection of nodes"
        self.at(81.6)
        self.play(
            LaggedStart(*[GrowFromCenter(n) for n in nodes.values()], lag_ratio=0.2),
            run_time=1.2,
        )

        # "corresponding to the webpages"
        self.at(84.0)
        node_note = Text("node = webpage", font_size=32, color=TEXT_COLOR)
        node_note.next_to(nodes["A"], LEFT, buff=0.6)
        node_arrow = Arrow(
            node_note.get_right(), nodes["A"].get_left(), buff=0.1, color=HIGHLIGHT
        )
        self.play(
            FadeIn(node_note),
            GrowArrow(node_arrow),
            *[Indicate(n, scale_factor=1.15) for n in nodes.values()],
        )

        # "and arrows between those webpages"
        self.at(85.9)
        self.play(
            LaggedStart(*[draw_arrow(e.arrow) for e in edges.values()], lag_ratio=0.1),
            run_time=1.6,
        )

        # "corresponding to links"
        self.at(87.8)
        ab = edges["A", "B"].arrow
        link_note = Text("arrow = link", font_size=32, color=TEXT_COLOR)
        link_note.next_to(ab, UP, buff=0.35)
        self.play(
            FadeIn(link_note),
            ab.animate.set_stroke(width=EDGE_BOLD_STROKE_WIDTH).set_color(HIGHLIGHT),
        )

        # "We will label the arrow from webpage A to B"
        self.at(90.4)
        self.play(FadeOut(link_note), FadeOut(node_note), FadeOut(node_arrow), run_time=0.6)
        self.at(91.8)
        self.play(Write(edges["A", "B"].label, rate_func=smooth), run_time=0.8)

        # "with the probability that a random link is clicked"
        self.at(93.3)
        others = [e for key, e in edges.items() if key != ("A", "B")]
        self.play(
            ab.animate.set_stroke(width=EDGE_STROKE_WIDTH).set_color(EDGE_COLOR),
            LaggedStart(
                *[Write(e.label, rate_func=smooth) for e in others], lag_ratio=0.1
            ),
            run_time=1.8,
        )
        self.end()

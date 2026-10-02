"""A Google search results page, plus cards for sites that link to a result.

    from pagerank_style.search import *

    page = SearchPage("what is pagerank", [
        SearchResult("Wikipedia", "en.wikipedia.org", "PageRank - Wikipedia",
                     "PageRank is an algorithm...", logo="wikipedia.png"),
        SearchResult("Some Blog", "someblog.com", "What Is PageRank?", "..."),
    ])
    self.play(page.show_bar())       # Google logo + empty search bar
    self.play(page.type_query())     # query types itself in
    self.play(page.show_results())   # results slide in one by one
    self.play(page.spotlight(0))     # dim every result except the first

    cards = VGroup(LinkCard("University", "stanford.edu", BLUE), ...)
    arrows = link_arrows(cards, page.results[0].favicon)

Logos (google.png, and any `logo=` you pass) live in assets/logos/.
"""

from manim import *

from pagerank_style import (
    BACKGROUND,
    LINK_BLUE,
    LOGOS,
    SEARCH_BAR_FILL,
    SEARCH_FONT,
    SEARCH_PAGE_HEIGHT,
    SEARCH_WIDTH,
    SNIPPET_GRAY,
    TEXT_COLOR,
    URL_GRAY,
)

FAVICON_RADIUS = 0.24
CARD_WIDTH = 2.5
CARD_HEIGHT = 0.85


def search_text(s, size, color=TEXT_COLOR):
    """Text in the search page font.

    Pango rounds letter spacing at small sizes ("i s" instead of "is"),
    so render big and scale down.
    """
    return Text(s, font=SEARCH_FONT, font_size=4 * size, color=color).scale(0.25)


def baseline(txt):
    """Height of a Text's baseline (the bottom of letters without g, p, y tails)."""
    on_line = [c for c, ch in zip(txt, txt.text.replace(" ", "")) if ch not in "gjpqy,"]
    return min(c.get_bottom()[1] for c in on_line)


def set_baseline(txt, y):
    """Move a Text so its baseline sits at height y."""
    return txt.shift((y - baseline(txt)) * UP)


def favicon(site, logo=None, radius=FAVICON_RADIUS):
    """A site's round icon: its logo on a white disk, or its first letter."""
    disk = Circle(radius=radius, stroke_width=0, fill_opacity=1)
    if logo is not None:
        disk.set_fill(WHITE)
        return Group(disk, ImageMobject(LOGOS / logo).set_height(1.6 * radius))
    disk.set_fill(SEARCH_BAR_FILL)
    return Group(disk, search_text(site[0], 22, URL_GRAY).move_to(disk))


def magnifier():
    lens = Circle(radius=0.1, stroke_width=3, color=URL_GRAY)
    handle = Line(ORIGIN, 0.12 * (DR / np.sqrt(2)), stroke_width=3, color=URL_GRAY)
    handle.shift(lens.point_at_angle(-PI / 4))
    return VGroup(lens, handle)


class SearchResult(Group):
    """One Google result: favicon + site/url, blue title, grey snippet."""

    def __init__(self, site, url, title, snippet, logo=None, **kwargs):
        self.favicon = favicon(site, logo)
        source = VGroup(search_text(site, 20), search_text(url, 16, URL_GRAY))
        source.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        header = Group(self.favicon, source).arrange(RIGHT, buff=0.2)
        super().__init__(
            header,
            search_text(title, 30, LINK_BLUE),
            search_text(snippet, 18, SNIPPET_GRAY),
            **kwargs,
        )
        self.arrange(DOWN, aligned_edge=LEFT, buff=0.14)


class SearchPage(Group):
    """Google logo, search bar with a query, and results below.

    Scaled to SEARCH_PAGE_HEIGHT and centered vertically on screen.
    """

    def __init__(self, query, results, **kwargs):
        self.logo = ImageMobject(LOGOS / "google.png").set_height(1.7)
        self.bar = RoundedRectangle(
            corner_radius=0.3,
            width=SEARCH_WIDTH,
            height=0.6,
            stroke_width=0,
            fill_color=SEARCH_BAR_FILL,
            fill_opacity=1,
        ).next_to(self.logo, DOWN, buff=0.5)
        self.icon = (
            magnifier().move_to(self.bar).align_to(self.bar, LEFT).shift(0.3 * RIGHT)
        )

        self.query = search_text(query, 24).next_to(self.icon, RIGHT, buff=0.25)
        # center from the top of the letters to the baseline, ignoring
        # descenders like in "p" and "g" that would push the text up
        body_center = (self.query.get_top()[1] + baseline(self.query)) / 2
        self.query.shift((self.bar.get_center()[1] - body_center) * UP)

        self.results = Group(*results).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        self.results.next_to(self.bar, DOWN, buff=0.7)
        self.results.align_to(self.bar, LEFT).shift(0.2 * RIGHT)

        super().__init__(
            self.logo, self.bar, self.icon, self.query, self.results, **kwargs
        )
        self.scale(SEARCH_PAGE_HEIGHT / self.height)
        self.shift(-self.get_center()[1] * UP)

    def show_bar(self):
        """Animation: Google logo drops in, empty search bar appears."""
        return AnimationGroup(
            FadeIn(self.logo, shift=0.2 * DOWN), FadeIn(self.bar), FadeIn(self.icon)
        )

    def type_query(self, run_time=1):
        return AddTextLetterByLetter(self.query, run_time=run_time)

    def show_results(self, lag_ratio=0.2):
        return LaggedStart(
            *[FadeIn(r, shift=0.2 * UP) for r in self.results], lag_ratio=lag_ratio
        )

    def spotlight(self, i, dim=0.4):
        """Animation: fade every result except results[i]."""
        return AnimationGroup(
            *[r.animate.fade(dim) for j, r in enumerate(self.results) if j != i]
        )

    def left_margin_x(self):
        """x of the middle of the empty space left of the page."""
        return (self.bar.get_left()[0] - config.frame_width / 2) / 2


class LinkCard(VGroup):
    """A site that links somewhere: colored letter icon, name and url on a dark card."""

    def __init__(self, name, url, color, **kwargs):
        card = RoundedRectangle(
            corner_radius=0.15,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            stroke_width=0,
            fill_color=SEARCH_BAR_FILL,
            fill_opacity=1,
        )
        disk = Circle(radius=0.2, color=color, fill_opacity=1, stroke_width=0)
        disk.move_to(card).align_to(card, LEFT).shift(0.2 * RIGHT)
        letter = search_text(name[0], 20, BACKGROUND).move_to(disk)
        # fixed baselines so every card lines up, whatever letters it has
        name_text = set_baseline(search_text(name, 20), 0.04)
        url_text = set_baseline(search_text(url, 15, URL_GRAY), -0.25)
        VGroup(name_text, url_text).next_to(disk, RIGHT, buff=0.2, coor_mask=RIGHT)
        url_text.align_to(name_text, LEFT)
        super().__init__(card, disk, letter, name_text, url_text, **kwargs)


def link_arrows(sources, target, spread=0.1):
    """Arrows from the right side of each source to just left of `target`.

    The tips fan out by `spread` so they don't pile onto one point.
    """
    end = target.get_left() + 0.1 * LEFT
    n = len(sources)
    return VGroup(
        *[
            Arrow(
                source.get_right(),
                end + spread * ((n - 1) / 2 - i) * UP,
                buff=0.12,
                color=URL_GRAY,
                stroke_width=4,
                tip_length=0.18,
                max_tip_length_to_length_ratio=1,
            )
            for i, source in enumerate(sources)
        ]
    )

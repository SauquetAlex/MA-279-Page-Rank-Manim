"""Conclusion: a Google search where Wikipedia comes up first.

Plays right after RandomSurfer. Hold on screen during the closing voiceover.

Render:  uv run manim -pql scenes/alex/conclusion.py Conclusion

Needs two logos in assets/logos/ (PNG renders from Wikimedia Commons):
    google.png     <- Google_2015_logo.svg
    wikipedia.png  <- Wikipedia-logo-v2.svg
and three icons in assets/icons/ (SVGs from thenounproject.com):
    university.svg, government.svg, developer.svg
"""

from manim import *

from pagerank_style import *
from pagerank_style.search import LinkCard, SearchPage, SearchResult, link_arrows

QUERY = "what is pagerank"

RESULTS = [
    SearchResult(
        "Wikipedia", "en.wikipedia.org › wiki › PageRank", "PageRank - Wikipedia",
        "PageRank is an algorithm used by Google Search to rank web pages...",
        logo="wikipedia.png",
    ),
    SearchResult(
        "Some Blog", "someblog.com › seo › pagerank", "What Is PageRank? A Simple Guide",
        "Everything you need to know about how Google ranks pages...",
    ),
    SearchResult(
        "Another Site", "another-site.net › articles", "PageRank Explained in 5 Minutes",
        "A quick look at the math behind the original Google algorithm...",
    ),
]

# Sites that link to Wikipedia: (name, url, color, icon in assets/icons/[, icon scale])
LINKERS = [
    ("University", "purdue.edu", BLUE, "university.svg"),
    ("Government", "nasa.gov", YELLOW, "government.svg", 0.9),  # wide icon: shrink
    ("Developer", "github.com", GREEN, "developer.svg", 0.9),
]


class Conclusion(Scene):
    def construct(self):
        page = SearchPage(QUERY, RESULTS)
        wikipedia = page.results[0]

        # "So why does Wikipedia show up first?"
        self.play(page.show_bar())
        self.play(page.type_query())
        self.wait(0.3)
        self.play(page.show_results())
        self.wait()

        self.play(page.spotlight(0))
        self.wait(2)

        # "...universities, governments, and millions of coders linked it"
        cards = VGroup(*[LinkCard(*linker) for linker in LINKERS])
        gap = 0.35  # between cards, and between the last card and the dots
        cards.arrange(DOWN, buff=gap)
        cards.move_to([page.left_margin_x(), wikipedia.favicon.get_y(), 0])
        dots = MathTex(r"\vdots", color=URL_GRAY).scale(1.6).next_to(cards, DOWN, buff=gap)
        arrows = link_arrows(cards, wikipedia.favicon)

        self.play(LaggedStart(
            *[FadeIn(m, shift=0.2 * RIGHT) for m in (*cards, dots)], lag_ratio=0.3
        ))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2))
        self.wait(8)  # rest of the voiceover: adjust to match the recording

        self.play(FadeOut(Group(page, cards, dots, arrows)))

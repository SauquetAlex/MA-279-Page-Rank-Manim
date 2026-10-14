"""Intro: a sample Google for various things search where Wikipedia comes up first.

Plays at the beginning. Hold on screen until discussing backgroun/history.

Low quality render:  uv run manim -pql scenes/johnny/introduction.py Introduction
High quality render: uv run manim -pqh scenes/johnny/introduction.py Introduction


Needs two logos in assets/logos/ (PNG renders from Wikimedia Commons):
    google.png     <- Google_2015_logo.svg
    wikipedia.png  <- Wikipedia-logo-v2.svg
"""

from manim import *

from pagerank_style import *
from pagerank_style.search import SearchPage, SearchResult

searches = [
    ("What is a Hedgehog?", [
    SearchResult(
        "Wikipedia",
        "en.wikipedia.org › wiki › Hedgehog",
        "Hedgehog - Wikipedia",
        "A hedgehog is a spiny mammal of the subfamily Erinaceinae, in the eulipotyphlan...",
        logo="wikipedia.png",
    ),
    SearchResult(
        "Some Animal Blog",
        "someblog.com › animal facts › hedgehogs",
        "Our favorite fun facts about Hedgehogs",
        "Did you know that Hedgehogs are lactose intolerant? This is because...",
    ),
    SearchResult(
        "Another Animal Site",
        "another-animal-site.net › conservation",
        "Hedgehog Conservation",
        "In the UK, Hedgehog populations are dwindling at a concerning rate...",
    ),
    ]),
    ("Where is London?", [
    SearchResult(
        "Wikipedia",
        "en.wikipedia.org › wiki › London",
        "London - Wikipedia",
        "London is the capital and largest city of England and the United Kingdom...",
        logo="wikipedia.png",
    ),
    SearchResult(
        "Some Travel Blog",
        "sometravelblog.com › UK Cities › London",
        "Places to visit in London",
        "In London, there is a wide assortment of places to visit depending on what...",
    ),
    SearchResult(
        "A History Site",
        "a-history-site.net › history",
        "History of London",
        "London has a long and rich history, going all the way back to the roman times...",
    ),
    ]),
    ("Who is John Forbes Nash Jr.?", [
    SearchResult(
        "Wikipedia",
        "en.wikipedia.org › wiki › John Forbes Nash Jr.",
        "John Forbes Nash Jr. - Wikipedia",
        "John Forbes Nash Jr., known and published as John Nash, was an American mathematician...",
        logo="wikipedia.png",
    ),
    SearchResult(
        "Some Math Blog",
        "somemathblog.com › Game Theory › Nash Equilibrium",
        "What is the Nash Equilibrium?",
        "Proposed by John Nash, the nash equilibrium is a situation in which no player...",
    ),
    SearchResult(
        "Another Biographical Site",
        "another-biographical-site.net › John Forbes Nash Jr.",
        "Who was John Forbes Nash Jr.",
        "You should focus on the video, not this small text...",
    ),
    ]),
]

class Introduction(Scene):
    def construct(self):
        pages = [SearchPage(q, r) for q, r in searches]

        # first search: full intro
        page = pages[0]
        self.play(page.show_bar().set_run_time(0.5))
        self.wait(1.3)
        self.play(page.type_query().set_run_time(0.5))
        self.play(page.show_results().set_run_time(0.5))
        self.wait(0.5)

        # later searches: query rolls up, then results regenerate
        for new in pages[1:]:
            new.align_to_page(page)
            self.play(page.roll_to(new).set_run_time(0.5))
            self.play(new.show_results().set_run_time(0.5))
            self.wait(0.5)
            page = new

        self.wait(4)
        arrow = new.top_arrow()      # after align_to_page, so it's positioned correctly
        self.play(GrowArrow(arrow))
        self.wait(13.7)
        self.clear()
        title = Title("PageRank")
        title.center()
        self.play(Write(title))
        self.wait(5)

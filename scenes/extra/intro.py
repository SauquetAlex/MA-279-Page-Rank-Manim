"""Intro and background/history (Johnny's part).

    Intro    a search for "red panda" where Wikipedia comes up first: why?
    History  1994 Yahoo! Directory, 1994 WebCrawler, 1996 PageRank

The script also shows photos of Larry Page and Sergey Brin (Wikimedia
Commons, cited in the script). Drop them in assets/photos/ as page.jpg and
brin.jpg and they replace the grey placeholders in History.

Render:  uv run manim -pql scenes/extra/intro.py Intro
"""

from pathlib import Path

from manim import *

from pagerank_style import *
from pagerank_style.search import SearchPage, SearchResult
from pagerank_style.webpage import WebPage, page_text

PHOTOS = Path(__file__).resolve().parents[2] / "assets" / "photos"

QUERY = "red panda"

RESULTS = [
    SearchResult(
        "Wikipedia", "en.wikipedia.org › wiki › Red_panda", "Red panda - Wikipedia",
        "The red panda is a small mammal native to the eastern Himalayas...",
        logo="wikipedia.png",
    ),
    SearchResult(
        "Zoo Atlanta", "zooatlanta.org › animals", "Red Panda | Zoo Atlanta",
        "Meet the red pandas at Zoo Atlanta and learn about their habitat...",
    ),
    SearchResult(
        "Animal Facts", "animalfacts.net › red-panda", "10 Fun Facts About Red Pandas",
        "Red pandas spend most of their lives in trees and eat bamboo...",
    ),
]


class Intro(Scene):
    """"Look up an animal... the first website is usually Wikipedia. Why?"."""

    def construct(self):
        page = SearchPage(QUERY, RESULTS)
        self.play(page.show_bar())
        self.play(page.type_query())
        self.wait(0.3)
        self.play(page.show_results())
        self.wait()
        self.play(page.spotlight(0))

        wiki = page.results[0]
        box = SurroundingRectangle(wiki, color=HIGHLIGHT, buff=0.15, corner_radius=0.1)
        self.play(Create(box))
        self.wait()

        # "Did someone at Google HQ just say that Wikipedia should always be first?"
        question = Text("Why always first?", font_size=36, color=HIGHLIGHT)
        question.next_to(box, LEFT, buff=0.3)
        if question.get_left()[0] < -config.frame_width / 2 + 0.2:
            question.scale_to_fit_width(box.get_left()[0] + config.frame_width / 2 - 0.6)
            question.next_to(box, LEFT, buff=0.3)
        self.play(FadeIn(question, shift=0.2 * RIGHT))
        self.wait(4)
        self.play(FadeOut(Group(page, box, question)))


def year_label(year):
    return Text(str(year), font_size=48, color=HIGHLIGHT, weight=BOLD)


def directory_panel():
    """Yahoo!-style phone book of links, sorted into categories by hand."""
    title = page_text("Yahoo! Directory", 30, "#B388FF")
    categories = [
        ("Arts", "Humanities, Photography"),
        ("Business", "Companies, Jobs"),
        ("Computers", "Internet, Software"),
        ("Science", "Biology, Astronomy"),
    ]
    rows = VGroup(
        *[
            VGroup(page_text(c, 22, LINK_BLUE), page_text(sub, 16, SNIPPET_GRAY)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06
            )
            for c, sub in categories
        ]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    body = VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    card = SurroundingRectangle(
        body, buff=0.25, corner_radius=0.15, color=SEARCH_BAR_FILL,
        fill_color="#202124", fill_opacity=1, stroke_width=3,
    )
    return VGroup(card, body)


def crawler_panel():
    """A WebCrawler-style result: ranked by keyword count, easy to stuff."""
    page = WebPage(
        "webcrawler.com",
        "Search: red panda",
        "1. cheap-deals.biz\n"
        "    red panda red panda red panda\n"
        "2. Red Panda Facts\n"
        "    red panda, a small mammal...",
        keyword="panda",
        width=4.2,
        height=2.7,
    )
    return page


def person(name, photo):
    """A photo (or a grey placeholder) with a name under it."""
    path = PHOTOS / photo
    if path.exists():
        img = ImageMobject(path).set_height(2)
    else:
        img = RoundedRectangle(
            corner_radius=0.1, width=1.6, height=2, color=LIGHT_GRAY,
            fill_color=SEARCH_BAR_FILL, fill_opacity=1, stroke_width=2,
        )
        img = VGroup(img, Text("photo", font_size=22, color=LIGHT_GRAY).move_to(img))
    label = Text(name, font_size=26, color=TEXT_COLOR)
    return Group(img, label).arrange(DOWN, buff=0.15)


class History(Scene):
    """1994 Yahoo! Directory -> 1994 WebCrawler -> 1996 PageRank."""

    def construct(self):
        line = Line(6.6 * LEFT, 6.6 * RIGHT, color=LIGHT_GRAY).to_edge(UP, buff=1.8)
        xs = [-4.6, 0, 4.6]
        ticks = VGroup(*[Line(0.15 * UP, 0.15 * DOWN, color=LIGHT_GRAY).move_to(line.get_center() + x * RIGHT) for x in xs])
        years = VGroup(*[year_label(y).next_to(t, UP, buff=0.15) for y, t in zip((1994, 1994, 1996), ticks)])
        self.play(Create(line), FadeIn(ticks))

        # 1994: Yahoo! Directory, updated by hand
        self.play(FadeIn(years[0], shift=0.2 * DOWN))
        directory = directory_panel().scale(1.0).next_to(ticks[0], DOWN, buff=0.5)
        self.play(FadeIn(directory, shift=0.2 * UP))
        hand = Text("sorted by hand", font_size=30, color=RED)
        hand.next_to(directory, DOWN, buff=0.2)
        new_site = page_text("new-site.com ?", 26, URL_GRAY).next_to(hand, DOWN, buff=0.2)
        self.play(FadeIn(hand), FadeIn(new_site, shift=0.2 * UP))
        self.play(Wiggle(new_site))
        self.wait(2)

        # 1994: WebCrawler, ranked by keywords
        self.play(FadeIn(years[1], shift=0.2 * DOWN))
        crawler = crawler_panel().scale(0.9).next_to(ticks[1], DOWN, buff=0.5)
        self.play(FadeIn(crawler, shift=0.2 * UP))
        stuffing = Text("keyword stuffing", font_size=30, color=RED)
        stuffing.next_to(crawler, DOWN, buff=0.2)
        self.play(FadeIn(stuffing), Indicate(crawler.keyword_words()[:3], color=RED))
        self.wait(2)

        # 1996: Larry Page and Sergey Brin at Stanford
        self.play(FadeIn(years[2], shift=0.2 * DOWN))
        people = Group(
            person("Larry Page", "page.jpg"), person("Sergey Brin", "brin.jpg")
        ).arrange(RIGHT, buff=0.25).scale(0.95)
        people.next_to(ticks[2], DOWN, buff=0.5)
        self.play(FadeIn(people, shift=0.2 * UP))
        pagerank = Text("PageRank", font_size=48, color=ACCENT, weight=BOLD)
        stanford = Text("Stanford University", font_size=26, color=LIGHT_GRAY)
        caption = VGroup(pagerank, stanford).arrange(DOWN, buff=0.1)
        caption.next_to(people, DOWN, buff=0.3)
        self.play(Write(pagerank), FadeIn(stanford))
        self.play(Circumscribe(pagerank, color=HIGHLIGHT))
        self.wait(3)
        self.play(FadeOut(Group(*self.mobjects)))

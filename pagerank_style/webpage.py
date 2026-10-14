"""A small browser window showing a web page, for comparing pages side by side.

    from pagerank_style.webpage import *

    page = WebPage("jaguarfacts.org", "All About Jaguars", BODY, keyword="jaguar")
    page.keyword_words      # the highlighted copies of the keyword in the body
    self.play(page.count_up(counter))

`body` is plain text with newlines; every copy of `keyword` in it is colored
HIGHLIGHT so viewers can count them.
"""

from manim import *

from pagerank_style import (
    HIGHLIGHT,
    LINK_BLUE,
    SEARCH_BAR_FILL,
    SEARCH_FONT,
    SNIPPET_GRAY,
    TEXT_COLOR,
    URL_GRAY,
)

WINDOW_WIDTH = 4.6
WINDOW_HEIGHT = 3.6
TOOLBAR_HEIGHT = 0.45
WINDOW_FILL = "#202124"  # Google dark-mode page background


def page_text(s, size, color=TEXT_COLOR, **kwargs):
    """Text in the search page font, rendered big and scaled down (see search.py)."""
    return Text(s, font=SEARCH_FONT, font_size=4 * size, color=color, **kwargs).scale(
        0.25
    )


class WebPage(VGroup):
    """Browser window: toolbar with dots and url, a blue title and body text."""

    def __init__(
        self,
        url,
        title,
        body,
        keyword=None,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.keyword = keyword
        self.frame = RoundedRectangle(
            corner_radius=0.15,
            width=width,
            height=height,
            stroke_color=SEARCH_BAR_FILL,
            stroke_width=3,
            fill_color=WINDOW_FILL,
            fill_opacity=1,
        )
        self.toolbar = Rectangle(
            width=width - 0.06,
            height=TOOLBAR_HEIGHT,
            stroke_width=0,
            fill_color=SEARCH_BAR_FILL,
            fill_opacity=1,
        ).align_to(self.frame, UP).shift(0.03 * DOWN)
        dots = VGroup(
            *[
                Dot(radius=0.05, color=c)
                for c in ("#FC6255", "#FFFF00", "#83C167")
            ]
        ).arrange(RIGHT, buff=0.08)
        dots.move_to(self.toolbar).align_to(self.toolbar, LEFT).shift(0.15 * RIGHT)
        self.url = page_text(url, 16, URL_GRAY).next_to(dots, RIGHT, buff=0.25)

        self.title = page_text(title, 26, LINK_BLUE)
        self.title.next_to(self.toolbar, DOWN, buff=0.25).align_to(dots, LEFT)
        t2c = {keyword: HIGHLIGHT} if keyword else {}
        self.body = page_text(body, 17, SNIPPET_GRAY, t2c=t2c, line_spacing=1.2)
        self.body.next_to(self.title, DOWN, buff=0.2, aligned_edge=LEFT)

        self.add(self.frame, self.toolbar, dots, self.url, self.title, self.body)

    def keyword_words(self, text=None):
        """The copies of the keyword inside `text` (the body by default)."""
        text = self.body if text is None else text
        if not self.keyword:
            return VGroup()
        letters = text.text.replace(" ", "").replace("\n", "")
        n = len(self.keyword)
        return VGroup(
            *[
                text[i : i + n]
                for i in range(len(letters) - n + 1)
                if letters[i : i + n] == self.keyword
            ]
        )

    def mini(self):
        """A copy without the body text: just the window and title, for graphs."""
        return VGroup(self.frame, self.toolbar, self.url, self.title).copy()

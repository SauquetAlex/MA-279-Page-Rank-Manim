"""Johnny's Background scene.

Low Quality Render:  uv run manim -pql scenes/johnny/background.py Background
High Quality Render: uv run manim -pqh scenes/johnny/background.py Background
"""

from manim import *
from pagerank_style import *
from pathlib import Path

#Image filepaths
assets_path = "assets/background images/"
Yahoo_Logo = assets_path + "Yahoo.svg"
Yahoo_Directory_Logo = assets_path + "Yahoo_Directory.webp"
Yahoo_Directory_Snapshot = assets_path + "Yahoo_Directory_Snapshop.png"
Brian_Pinkerton = assets_path + "Brian_Pinkerton.gif"
WebCrawler_Snapshot = assets_path + "WebCrawler_Snapshot.png"
AmericaOnline_Logo = assets_path + "AmericaOnline_logo.svg"
AOL_Logo = assets_path + "AOL_logo.svg"
Larry_Page = assets_path + "Larry_Page.jpg"
Sergey_Brin = assets_path + "Sergey_Brin.jpg"

def load_image(image):
    image = Path(image)
    if image.suffix == ".svg":
        return SVGMobject(image)
    else:
        return ImageMobject(image)

def add_caption(image,text):
    return Text(text,font_size=48).scale(0.2).next_to(image, DOWN, buff=0.1)

def load_citation(citation):
    return Text(citation, font_size=48).scale(0.2).to_corner(DL)

#APA Citations
Citations = {
    "Aaron Wall, 2006":r"Aaron Wall. (2006). History of Search Engines: From 1945 to Google Today. Search Engine History. http://www.searchenginehistory.com/",
    "America Online Inc, 1991":r"America Online Inc. (1991). America Online Logo [Graphic]. https://commons.wikimedia.org/wiki/File:America_Online_logo.svg",
    "Brian Pinkerton, 1996":r"Brian Pinkerton. (1996, October 23). WebCrawler Searching. https://web.archive.org/web/19961023234707/http://www.webcrawler.com/",
    "Brian Pinkerton, 2005a":r"Brian Pinkerton. (2005a, November 28). WebCrawler Timeline. Think Pink. https://web.archive.org/web/20051128091213/http://www.thinkpink.com/bp/WebCrawler/History.html",
    "Brian Pinkerton, 2005b":r"Brian Pinkerton. (2005b, December 12). Brian Pinkerton. https://web.archive.org/web/20051212132303/http://www.thinkpink.com/bp/bio.html",
    "Stansfield PL, 2009":r"Stansfield PL. (2009, June 17). Larry Page. Wikimedia Commons. https://commons.wikimedia.org/wiki/File:Larry_Page_in_the_European_Parliament,_17.06.2009_(cropped_2).jpg",
    "Steve Jurvetson, 2010":r"Steve Jurvetson. (2010, February 12). Sergey Brin. Wikimedia Commons. https://commons.wikimedia.org/wiki/File:Sergey_Brin_Ted_2010_(cropped).jpg",
    "Verizon Media - Pentagram, 2019":r"Verizon Media - Pentagram. (2019). Yahoo! Logo [Graphic]. https://www.yahoo.com/. https://commons.wikimedia.org/wiki/File:Yahoo!_(2019).svg",
    "Yahoo! Inc, 2002":r"Yahoo! Inc. (2002, August 14). Yahoo! Search and Directory. https://web.archive.org/web/20020814071233/http://dir.yahoo.com/",
    "Yahoo! Inc, 2013":r"Yahoo! Inc. (2013). Yahoo! Directory logo [Graphic]. dir.yahoo.com. https://commons.wikimedia.org/wiki/File:Yahoo!_Directory_Logo_(2013-2014).png",
    "Yahoo! Inc, 2024":r"Yahoo! Inc. (2024). AOL logo [Graphic]. https://www.aol.com. https://commons.wikimedia.org/wiki/File:AOL_logo_(2024).svg"
}

class Background(Scene):
    def construct(self):

        # For clarifying citations
        info_text = load_citation("Information:")
        images_text = load_citation("Images:")

        # ---- Walk through events ------------------------------------------
        ### Yahoo Directory ###
        # Load Images
        img_Yahoo = load_image(Yahoo_Logo)
        img_Yahoo_Directory = load_image(Yahoo_Directory_Logo).scale(1.5).next_to(img_Yahoo, DOWN)
        img_Yahoo_Directory_Snapshot = load_image(Yahoo_Directory_Snapshot)

        # Load Citations
        cit_AaronWall = load_citation(Citations["Aaron Wall, 2006"])
        cit_Yahoo_Directory = load_citation(Citations["Yahoo! Inc, 2013"])
        cit_Yahoo = load_citation(Citations["Verizon Media - Pentagram, 2019"])
        cit_Yahoo_Directory_Snapshot = load_citation(Citations["Yahoo! Inc, 2002"])

        # Group images/text
        Group(
            img_Yahoo_Directory,img_Yahoo
        ).arrange(UP, buff=0.5)

        VGroup(
            cit_Yahoo_Directory, cit_Yahoo, images_text, cit_AaronWall, info_text
        ).arrange(UP, aligned_edge=LEFT, buff=0.1).to_corner(DL)

        # Add captions to images for citations
        cap_Yahoo_Directory = add_caption(img_Yahoo_Directory,"(Yahoo! Inc, 2013)")
        cap_Yahoo = add_caption(img_Yahoo,"(Verizon Media - Pentagram, 2019)")
        cap_Yahoo_Directory_Snapshot = add_caption(img_Yahoo_Directory_Snapshot,"(Yahoo! Inc, 2002)")

        self.add(info_text, cit_AaronWall)
        self.wait(2)
        self.add(img_Yahoo, cap_Yahoo, cit_Yahoo, images_text)
        self.wait(3.5)

        self.add(BackgroundRectangle(img_Yahoo_Directory, color=WHITE, fill_opacity=1))
        self.add(img_Yahoo_Directory, cap_Yahoo_Directory, cit_Yahoo_Directory)
        self.wait(4)

        self.clear()
        self.add(img_Yahoo_Directory_Snapshot, cap_Yahoo_Directory_Snapshot, cit_Yahoo_Directory_Snapshot)
        self.wait(12.5)
        self.clear()

        ### WebCrawler ###
        # Load Images
        img_BrianPinkerton = load_image(Brian_Pinkerton)
        img_WebCrawlerSnapshot = load_image(WebCrawler_Snapshot)
        img_AmericaOnline = load_image(AmericaOnline_Logo)
        img_AOL = load_image(AOL_Logo)

        # Load Citations
        cit_BrianPinkerton = load_citation(Citations["Brian Pinkerton, 2005b"])
        cit_WebCrawlerTimeline = load_citation(Citations["Brian Pinkerton, 2005a"])
        cit_WebCrawlerSnapshot = load_citation(Citations["Brian Pinkerton, 1996"])
        cit_AmericaOnline = load_citation(Citations["America Online Inc, 1991"])
        cit_AOL = load_citation(Citations["Yahoo! Inc, 2024"])

        # Group images/text
        Group(
            img_BrianPinkerton,img_WebCrawlerSnapshot
            ).arrange(RIGHT, buff=0.75)

        Group(
            img_AmericaOnline,img_AOL
            ).arrange(RIGHT, buff=0.5)


        VGroup(
            cit_WebCrawlerSnapshot,cit_BrianPinkerton,images_text,cit_WebCrawlerTimeline,info_text
            ).arrange(UP, aligned_edge=LEFT, buff=0.1).to_corner(DL)

        VGroup(
            cit_AOL,cit_AmericaOnline,images_text,cit_WebCrawlerTimeline,info_text
            ).arrange(UP, aligned_edge=LEFT, buff=0.1).to_corner(DL) 

        # Add captions to images for citations
        cap_BrianPinkerton = add_caption(img_BrianPinkerton,"(Brian Pinkerton, 2005b)")
        cap_WebCrawlerSnapshot = add_caption(img_WebCrawlerSnapshot,"(Brian Pinkerton, 1996)")
        cap_AmericaOnline = add_caption(img_AmericaOnline,"(America Online Inc, 1991)")
        cap_AOL = add_caption(img_AOL,"(Yahoo! Inc, 2024)")

        self.add(cit_WebCrawlerTimeline,info_text)
        self.wait(1.5)
        self.add(BackgroundRectangle(img_BrianPinkerton, color=WHITE, fill_opacity=1))
        self.add(img_BrianPinkerton, cap_BrianPinkerton,cit_BrianPinkerton,images_text)
        self.wait(4)
        self.add(img_WebCrawlerSnapshot, cap_WebCrawlerSnapshot,cit_WebCrawlerSnapshot)
        self.wait(8.5)

        self.clear()
        self.add(cit_WebCrawlerTimeline,info_text)
        self.wait(1)
        self.add(BackgroundRectangle(img_AmericaOnline, color=WHITE, fill_opacity=1))
        self.add(img_AmericaOnline, cap_AmericaOnline,cit_AmericaOnline,images_text)
        self.wait(3.5)
        self.add(BackgroundRectangle(img_AOL, color=WHITE, fill_opacity=1))
        self.add(img_AOL, cap_AOL,cit_AOL)
        self.wait(9)
        self.clear()


        ### PageRank ###
        # Load Images
        img_LarryPage = load_image(Larry_Page)
        img_SergeyBrin = load_image(Sergey_Brin)

        # Load Citations
        cit_LarryPage = load_citation(Citations["Stansfield PL, 2009"])
        cit_SergeyBrin = load_citation(Citations["Steve Jurvetson, 2010"])

        # Group images/text
        Group(
            img_LarryPage,img_SergeyBrin
        ).arrange(RIGHT, buff=0.5)

        VGroup(
            cit_SergeyBrin,cit_LarryPage,images_text,cit_AaronWall,info_text
        ).arrange(UP, aligned_edge=LEFT, buff=0.1).to_corner(DL)

        # Add captions to images for citations
        cap_LarryPage = add_caption(img_LarryPage,"(Stansfield PL, 2009)")
        cap_SergeyBrin = add_caption(img_SergeyBrin,"(Steve Jurvetson, 2010)")

        self.add(cit_AaronWall,info_text)
        self.wait(3.75)
        self.add(img_LarryPage, cap_LarryPage,cit_LarryPage,images_text)
        self.wait(1)
        self.add(img_SergeyBrin, cap_SergeyBrin,cit_SergeyBrin)
        self.wait(2.74)
        self.clear()
        
        title = Title("PageRank")
        title.center()
        self.play(Write(title))
        self.wait(15)
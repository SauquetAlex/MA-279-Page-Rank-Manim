"""Scenes timed to a voiceover.

A scene file defines VO: {scene class name: second of the voiceover where it
starts, ..., "end": total length}, in playing order. It may also define
GAPS: [(second of the recording, seconds of silence inserted there), ...] to
lengthen pauses; times stay in recording time and are shifted here. Then:

    from pagerank_style.timing import TimedScene

    class MyScene(TimedScene):
        def construct(self):
            self.at(12.5)          # wait until 12.5 s into the voiceover
            self.play(...)
            self.end()             # hold until the next scene starts
"""

import sys

from manim import Scene, logger


def shifted(t, gaps):
    """Recording time `t` -> time in the final video, after inserting `gaps`."""
    return t + sum(seconds for at, seconds in gaps if at < t)


class TimedScene(Scene):
    def setup(self):
        module = sys.modules[type(self).__module__]
        self.timeline = module.VO
        self.gaps = getattr(module, "GAPS", [])
        self.start = self.video_time(self.timeline[type(self).__name__])

    def video_time(self, t):
        return shifted(t, self.gaps)

    def at(self, t):
        """Wait until second `t` of the recording (warn if already past it)."""
        delay = self.video_time(t) - self.start - self.time
        if delay > 1 / 120:
            self.wait(delay)
        elif delay < -0.05:
            logger.warning(f"{type(self).__name__}: {-delay:.2f}s late for t={t}")

    def end(self):
        """Hold the last frame until the next scene starts."""
        names = list(self.timeline)
        self.at(self.timeline[names[names.index(type(self).__name__) + 1]])

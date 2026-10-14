"""Join the rendered Math Part 1 scenes and put Abbas's voiceover under them.

The voiceover gets the extra silences listed in GAPS and is cut at VO["end"];
the video is padded or trimmed to that exact length.

Run from the repo root after:  uv run manim -qh scenes/abbas/math_part1.py -a
    uv run python scenes/abbas/join_voiceover.py [output.mp4]
"""

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from math_part1 import GAPS, VO  # noqa: E402

from pagerank_style.timing import shifted  # noqa: E402

SCENES = [name for name in VO if name != "end"]
VIDEO_DIR = Path("media/videos/math_part1/1080p60")
AUDIO = Path("assets/audio/math_part1_voiceover.m4a")
out = Path(sys.argv[1] if len(sys.argv) > 1 else "media/math_part1_with_voiceover.mp4")

end = shifted(VO["end"], GAPS)

# audio: recording pieces with silence between them
cuts = [0.0] + [at for at, _ in GAPS] + [VO["end"]]
parts, labels = [], []
for i, (a, b) in enumerate(zip(cuts, cuts[1:])):
    parts.append(f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS[p{i}]")
    labels.append(f"[p{i}]")
    if i < len(GAPS):
        parts.append(f"anullsrc=r=16000:cl=mono,atrim=duration={GAPS[i][1]}[s{i}]")
        labels.append(f"[s{i}]")
parts.append(f"{''.join(labels)}concat=n={len(labels)}:v=0:a=1,afade=t=out:st={end - 0.5}:d=0.5[a]")
parts.append(
    f"[0:v]tpad=stop_mode=clone:stop_duration=2,trim=duration={end},setpts=PTS-STARTPTS[v]"
)

with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as listing:
    for name in SCENES:
        listing.write(f"file '{(VIDEO_DIR / f'{name}.mp4').resolve()}'\n")

subprocess.run(
    ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", listing.name,
     "-i", str(AUDIO), "-filter_complex", ";".join(parts), "-map", "[v]", "-map", "[a]",
     "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
     str(out)],
    check=True,
)
Path(listing.name).unlink()
print(f"{out}: {end:.2f} s")

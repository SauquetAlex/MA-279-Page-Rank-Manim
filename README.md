# MA-279-Page-Rank-Manim

Animations explaining PageRank, made with [Manim](https://www.manim.community/).

## 1. Install the tools (one time)

You need **git** and **uv**.

- **git**: on Mac, run `git --version`. If it isn't installed, macOS will offer to install it. On Windows, get it from https://git-scm.com.
- **uv**:
  - Mac / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

Close and reopen your terminal afterward.

## 2. Get the project (one time)

```bash
git clone https://github.com/SauquetAlex/MA-279-Page-Rank-Manim.git
cd MA-279-Page-Rank-Manim
uv sync
```

`uv sync` downloads the right Python version and installs Manim. You don't need to install Python yourself.

## 3. Render an animation

```bash
uv run manim -pql scenes/johnny/hello.py Hello
```

- `-p` opens the video when it's done
- `-ql` renders in low quality, which is fast. Use `-qh` for the final high-quality version.

Videos are saved in the `media/` folder. Git ignores that folder, so don't commit videos.

Everyone has a starter "Hello World" scene:

| Who    | Command                                        |
|--------|------------------------------------------------|
| Johnny | `uv run manim -pql scenes/johnny/hello.py Hello` |
| Abbas  | `uv run manim -pql scenes/abbas/hello.py Hello`  |
| Alex   | `uv run manim -pql scenes/alex/hello.py Hello`   |

## 4. Make your own animation

Work in **your own folder** (`scenes/<your-name>/`) so we don't overwrite each other's work.
Start every file with:

```python
from manim import *
from pagerank_style import *
```

This gives you our shared colors: `BACKGROUND` (black), `TEXT_COLOR` (white), `ACCENT` (blue) and `HIGHLIGHT` (yellow).

**Don't hard-code colors in your scene.** If we want to change the look, edit `pagerank_style/__init__.py` and tell the group.

## 5. Save and share your work

```bash
git pull                      # get everyone else's changes first
git add scenes/<your-name>
git commit -m "Describe what you did"
git push
```

## Troubleshooting

- **`uv: command not found`**: close and reopen your terminal.
- **Need a new package?** Run `uv add <package>` and commit `pyproject.toml` and `uv.lock` so everyone else gets it too. They then run `uv sync`.
- **Math formulas (`MathTex`)** require LaTeX. On Mac, install it with `brew install --cask mactex-no-gui`. On Windows, install [MiKTeX](https://miktex.org). Plain `Text` works without LaTeX.

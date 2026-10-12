"""neurostyle: matplotlib styles and helpers for neuroscience figures.

    import matplotlib.pyplot as plt
    import neurostyle

    plt.style.use("neuro")                                 # paper (one column)
    plt.style.use(["neuro", "neuro-talk"])                 # slides
    plt.style.use(["neuro", "neuro-talk", "neuro-dark"])   # dark slides

    fig, ax = plt.subplots(figsize=neurostyle.figsize("double", height_mm=80))
    neurostyle.panel_label(ax, "A")
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation

__version__ = "0.1.0"

# --- 1. Register the styles ----------------------------------------------------
_STYLE_DIR = Path(__file__).parent / "styles"
for _file in sorted(_STYLE_DIR.glob("*.mplstyle")):
    plt.style.library[_file.stem] = mpl.rc_params_from_file(_file, use_default_template=False)
plt.style.available[:] = sorted(plt.style.library)

# --- 2. Sizes ------------------------------------------------------------------
mm = 1 / 25.4  # one millimetre in inches: figsize=(89 * mm, 60 * mm)

WIDTHS_MM = {"single": 89, "1.5": 120, "double": 183}  # Nature; edit for your journal


def figsize(width="single", height_mm=None, aspect=0.75):
    """(width, height) in inches for a journal column width.

    figsize("single")                 -> 89 mm wide, height = 0.75 * width
    figsize("double", height_mm=80)   -> 183 x 80 mm
    """
    w = WIDTHS_MM[width] * mm
    h = height_mm * mm if height_mm is not None else w * aspect
    return (w, h)


# --- 3. Colors -----------------------------------------------------------------
OKABE_ITO = {
    "blue": "#0072B2", "vermillion": "#D55E00", "green": "#009E73", "purple": "#CC79A7",
    "orange": "#E69F00", "skyblue": "#56B4E9", "yellow": "#F0E442", "black": "#000000",
}

# One condition = one color, in every figure. Edit for your project.
CONDITION_COLORS = {"baseline": OKABE_ITO["blue"], "drug": OKABE_ITO["vermillion"]}


# --- 4. Decorations a style file can't do ----------------------------------------
def panel_label(ax, label, dx=-18, dy=4, size=9):
    """Bold panel letter at the top-left corner of `ax`, shifted by (dx, dy) points."""
    offset = ScaledTranslation(dx / 72, dy / 72, ax.figure.dpi_scale_trans)
    return ax.text(0, 1, label, transform=ax.transAxes + offset,
                   fontsize=size, fontweight="bold", va="bottom", ha="left")


def add_scalebar(ax, x, y, dx, dy, xlabel, ylabel, color=None, hide_axes=True):
    """L-shaped scale bar with its corner at (x, y), in data units."""
    color = color or mpl.rcParams["axes.edgecolor"]
    kw = dict(color=color, linewidth=1, solid_capstyle="butt", clip_on=False)
    ax.plot([x, x + dx], [y, y], **kw)
    ax.plot([x, x], [y, y + dy], **kw)
    ax.text(x + dx / 2, y, xlabel, ha="center", va="top")
    ax.text(x, y + dy / 2, ylabel + " ", ha="right", va="center")
    if hide_axes:
        # Not ax.set_axis_off(): it confuses constrained layout when labels sit outside the Axes
        ax.spines[:].set_visible(False)
        ax.set(xticks=[], yticks=[])

"""Classes to build and plot energy level diagrams."""

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

from matplotlib.transforms import Bbox

import matplotlib.pyplot as plt
import numpy as np

@dataclass(eq=False)
class Level:
    """Represents a single energy level."""

    energy: float
    label: Optional[str] = None
    # Reference to parent column, populated when added to a column
    column: Optional["Column"] = field(default=None, repr=False, init=False)


@dataclass
class Column:
    """A vertical column containing multiple :class:`Level` objects."""

    levels: List[Level] = field(default_factory=list)
    width: float = 0.5
    separation: float = 1.0
    label: Optional[str] = None

    def add_level(self, energy: float, label: Optional[str] = None) -> Level:
        """Append a level to this column and return it."""

        level = Level(energy, label)
        level.column = self
        self.levels.append(level)
        return level

@dataclass
class Diagram:
    """Container for columns composing the energy level diagram."""

    columns: List[Column] = field(default_factory=list)
    auto_regulation: bool = True
    label: Optional[str] = None
    # store explicit connections between levels
    _connections: List[Tuple[Level, Level]] = field(default_factory=list, init=False)
    # store vertical arrows between two levels
    _arrows: List[Tuple[Level, Level, float, Optional[str], str]] = field(default_factory=list, init=False)
    # store broken vertical arrows
    _broken_arrows: List[Tuple[Level, Level, float, Optional[str], float, str]] = field(
        default_factory=list,
        init=False,
    )
    # store transition arrows
    _transitions: List[Tuple[Level, Level, float, Optional[str], str]] = field(default_factory=list, init=False)
    # store spontaneous emission arrows
    _emissions: List[Tuple[Level, Level, float, Optional[str], str]] = field(default_factory=list, init=False)

    def add_column(
        self,
        levels: Optional[Iterable[float]] = None,
        *,
        width: Optional[float] = None,
        separation: Optional[float] = None,
        label: Optional[str] = None,
    ) -> Column:
        """Create a column, optionally with initial levels, and return it."""

        column = Column(width=width or 0.5, separation=separation or 1.0, label=label)
        if levels is not None:
            for energy in levels:
                column.add_level(energy)
        self.columns.append(column)
        return column

    def connect(self, level_a: Level, level_b: Level) -> None:
        """Register a dashed connection between two levels."""

        self._connections.append((level_a, level_b))

    def add_vertical_arrow(
        self,
        level_a: Level,
        level_b: Level,
        x: float,
        label: Optional[str] = None,
        color: str = "black",
    ) -> None:
        """Add a vertical arrow between two levels at a fixed x position."""

        self._arrows.append((level_a, level_b, x, label, color))

    def add_vertical_broken_arrow(
        self,
        level_a: Level,
        level_b: Level,
        x: float,
        label: Optional[str] = None,
        break_position: float = 0.5,
        color: str = "black",
    ) -> None:
        """Add a broken vertical arrow between two levels at a fixed x position."""

        self._broken_arrows.append((level_a, level_b, x, label, break_position, color))

    def add_transition(
        self,
        level_a: Level,
        level_b: Level,
        x: float,
        label: Optional[str] = None,
        color: str = "blue",
    ) -> None:
        """Add a one-way transition arrow between two levels."""

        self._transitions.append((level_a, level_b, x, label, color))

    def add_spontaneous_emission(
        self,
        level_a: Level,
        level_b: Level,
        x: float,
        label: Optional[str] = None,
        color: str = "red",
    ) -> None:
        """Add a spontaneous emission arrow between two levels."""

        self._emissions.append((level_a, level_b, x, label, color))

    def _compute_column_positions(self) -> List[float]:
        """Return the x coordinate for the start of each column."""

        positions: List[float] = []
        current_pos = 0.0
        for col in self.columns:
            positions.append(current_pos)
            current_pos += col.width
            current_pos += col.separation
        return positions

    def _regulate_levels(self, energies: List[float]) -> List[float]:
        """Optionally normalise a list of energies for plotting."""

        if not energies:
            return []
        if not self.auto_regulation:
            return energies
        min_level = min(energies)
        max_level = max(energies)
        span = max_level - min_level or 1.0
        return [(e - min_level) / span for e in energies]

    def plot(
        self,
        connect: bool = False,
        *,
        show_level_name: bool = False,
        show_column_name: bool = False,
        debug_mode: bool = False,
        padding: float = 0.05,
        padding_left: Optional[float] = None,
        padding_right: Optional[float] = None,
        padding_top: Optional[float] = None,
        padding_bottom: Optional[float] = None,
        column_label_gap: float = 0.1,
    ) -> Tuple[plt.Figure, plt.Axes]:
        """Plot the diagram and return the figure and axes objects.

        Parameters controlling padding can be provided either via the
        general ``padding`` argument or individually for each side. The
        ``column_label_gap`` argument sets the space between the lowest
        level and the column labels.
        """

        fig, ax = plt.subplots()
        positions = self._compute_column_positions()

        level_coords: Dict[Level, Tuple[float, float, float]] = {}
        column_data: List[Tuple[Column, float, List[float]]] = []
        min_level_y = float("inf")

        for col, x in zip(self.columns, positions):
            energies = [lvl.energy for lvl in col.levels]
            ys = self._regulate_levels(energies)
            column_data.append((col, x, ys))
            if ys:
                min_level_y = min(min_level_y, min(ys))
            for lvl, y in zip(col.levels, ys):
                ax.hlines(y, x, x + col.width, colors="black")
                if show_level_name and lvl.label:
                    ax.text(
                        x,
                        y + 0.02,
                        lvl.label,
                        ha="left",
                        va="bottom",
                    )
                level_coords[lvl] = (x, x + col.width, y)

        label_y = min_level_y - column_label_gap

        for col, x, ys in column_data:
            if show_column_name and col.label:
                ax.text(
                    x + col.width / 2,
                    label_y,
                    col.label,
                    ha="center",
                    va="top",
                )

        for left, right in self._connections:
            if left in level_coords and right in level_coords:
                lx0, lx1, y0 = level_coords[left]
                rx0, rx1, y1 = level_coords[right]
                ax.plot([lx1, rx0], [y0, y1], "--", color="gray")

        for start, end, x_pos, label, color in self._arrows:
            if start in level_coords and end in level_coords:
                _, _, y0 = level_coords[start]
                _, _, y1 = level_coords[end]
                ax.annotate(
                    "",
                    xy=(x_pos, y1),
                    xytext=(x_pos, y0),
                    arrowprops={"arrowstyle": "<->", "color": color},
                )
                if label:
                    ax.text(x_pos + 0.05, (y0 + y1) / 2, label, va="center", ha="left")

        for start, end, x_pos, label, break_pos, color in self._broken_arrows:
            if start in level_coords and end in level_coords:
                _, _, y0 = level_coords[start]
                _, _, y1 = level_coords[end]
                break_y = y0 + (y1 - y0) * break_pos
                ax.annotate(
                    "",
                    xy=(x_pos, y1),
                    xytext=(x_pos, y0),
                    arrowprops={"arrowstyle": "<->", "color": color},
                )
                gap = (y1 - y0) * 0.05
                ax.plot([x_pos, x_pos], [break_y - gap, break_y + gap], color="white", linewidth=3)
                ax.text(x_pos + 0.02, break_y, "~~", ha="left", va="center")
                if label:
                    ax.text(x_pos + 0.05, (y0 + y1) / 2, label, va="center", ha="left")

        for start, end, x_pos, label, color in self._transitions:
            if start in level_coords and end in level_coords:
                _, _, y0 = level_coords[start]
                _, _, y1 = level_coords[end]
                ax.annotate(
                    "",
                    xy=(x_pos, y1),
                    xytext=(x_pos, y0),
                    arrowprops={"arrowstyle": "-|>", "color": color},
                )
                if label:
                    ax.text(x_pos + 0.05, (y0 + y1) / 2, label, va="center", ha="left")

        for start, end, x_pos, label, color in self._emissions:
            if start in level_coords and end in level_coords:
                _, _, y0 = level_coords[start]
                _, _, y1 = level_coords[end]
                ax.annotate(
                    "",
                    xy=(x_pos, y1),
                    xytext=(x_pos, y0),
                    arrowprops={"arrowstyle": "->", "color": color, "linestyle": "--"},
                )
                if label:
                    ax.text(x_pos + 0.05, (y0 + y1) / 2, label, va="center", ha="left")

        if connect and len(self.columns) > 1 and not self._connections:
            # default behaviour: connect every level of adjacent columns
            for idx in range(1, len(self.columns)):
                left_col = self.columns[idx - 1]
                right_col = self.columns[idx]
                for l in left_col.levels:
                    for r in right_col.levels:
                        if l in level_coords and r in level_coords:
                            lx0, lx1, y0 = level_coords[l]
                            rx0, rx1, y1 = level_coords[r]
                            ax.plot([lx1, rx0], [y0, y1], "--", color="gray")

        if debug_mode:
            ax.set_xlabel("Column")
            ax.set_ylabel("Energy")
        else:
            ax.set_xlabel("")
            ax.set_ylabel("")
            ax.set_xticks([])
            ax.set_yticks([])
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        bbox: Optional[Bbox] = None
        for artist in ax.get_children():
            if not artist.get_visible() or not hasattr(artist, "get_window_extent"):
                continue
            try:
                artist_bbox = artist.get_window_extent(renderer)
            except Exception:
                continue
            if not np.isfinite(artist_bbox.extents).all():
                continue
            bbox = artist_bbox if bbox is None else Bbox.union([bbox, artist_bbox])

        if bbox is not None:
            data_bbox = bbox.transformed(ax.transData.inverted())
            left = padding_left if padding_left is not None else padding
            right = padding_right if padding_right is not None else padding
            bottom = padding_bottom if padding_bottom is not None else padding
            top = padding_top if padding_top is not None else padding
            ax.set_xlim(data_bbox.xmin - left, data_bbox.xmax + right)
            ax.set_ylim(data_bbox.ymin - bottom, data_bbox.ymax + top)

        ax.set_title(self.label or "Energy Level Diagram")
        plt.show()
        return fig, ax


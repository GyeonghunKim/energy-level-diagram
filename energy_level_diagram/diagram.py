"""Classes to build and plot energy level diagrams."""

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

import matplotlib.pyplot as plt

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
    # store explicit connections between levels
    _connections: List[Tuple[Level, Level]] = field(default_factory=list, init=False)

    def add_column(
        self,
        levels: Optional[Iterable[float]] = None,
        *,
        width: Optional[float] = None,
        separation: Optional[float] = None,
    ) -> Column:
        """Create a column, optionally with initial levels, and return it."""

        column = Column(width=width or 0.5, separation=separation or 1.0)
        if levels is not None:
            for energy in levels:
                column.add_level(energy)
        self.columns.append(column)
        return column

    def connect(self, level_a: Level, level_b: Level) -> None:
        """Register a dashed connection between two levels."""

        self._connections.append((level_a, level_b))

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

    def plot(self, connect: bool = False) -> None:
        fig, ax = plt.subplots()
        positions = self._compute_column_positions()

        level_coords: Dict[Level, Tuple[float, float, float]] = {}

        for col, x in zip(self.columns, positions):
            energies = [lvl.energy for lvl in col.levels]
            ys = self._regulate_levels(energies)
            for lvl, y in zip(col.levels, ys):
                ax.hlines(y, x, x + col.width, colors="black")
                level_coords[lvl] = (x, x + col.width, y)

        for left, right in self._connections:
            if left in level_coords and right in level_coords:
                lx0, lx1, y0 = level_coords[left]
                rx0, rx1, y1 = level_coords[right]
                ax.plot([lx1, rx0], [y0, y1], "--", color="gray")

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

        ax.set_xlabel("Column")
        ax.set_ylabel("Energy")
        ax.set_title("Energy Level Diagram")
        plt.show()


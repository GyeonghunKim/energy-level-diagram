"""Energy level diagram plotting utilities."""

from dataclasses import dataclass, field
from typing import List, Optional
import matplotlib.pyplot as plt

@dataclass
class Column:
    levels: List[float]
    width: Optional[float] = None
    separation: Optional[float] = None

@dataclass
class EnergyLevelDiagram:
    columns: List[Column] = field(default_factory=list)
    auto_regulation: bool = True

    def add_column(self, levels: List[float], width: Optional[float] = None, separation: Optional[float] = None) -> None:
        self.columns.append(Column(levels=levels, width=width, separation=separation))

    def _compute_column_positions(self) -> List[float]:
        positions = []
        current_pos = 0.0
        for col in self.columns:
            positions.append(current_pos)
            sep = col.separation if col.separation is not None else 1.0
            if col.width is not None:
                current_pos += col.width
            current_pos += sep
        return positions

    def _regulate_levels(self, levels: List[float]) -> List[float]:
        if not levels:
            return []
        if not self.auto_regulation:
            return levels
        # Normalize levels to start at 0 and scale to unit spacing
        min_level = min(levels)
        max_level = max(levels)
        span = max_level - min_level or 1.0
        return [(lvl - min_level) / span for lvl in levels]

    def plot(self, connect: bool = False) -> None:
        fig, ax = plt.subplots()
        positions = self._compute_column_positions()

        for idx, (col, x) in enumerate(zip(self.columns, positions)):
            levels = self._regulate_levels(col.levels)
            width = col.width if col.width is not None else 0.5
            for level in levels:
                ax.hlines(level, x, x + width, colors='black')
            if connect and idx > 0:
                prev_x = positions[idx - 1]
                prev_col = self.columns[idx - 1]
                prev_levels = self._regulate_levels(prev_col.levels)
                for y0 in prev_levels:
                    for y1 in levels:
                        ax.plot([prev_x + width, x], [y0, y1], '--', color='gray')

        ax.set_xlabel("Column")
        ax.set_ylabel("Energy")
        ax.set_title("Energy Level Diagram")
        plt.show()


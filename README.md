# energy-level-diagram

A simple library to plot energy level diagrams using Matplotlib. It supports multiple columns of levels, optional automatic regulation of level spacing, and dashed connections between columns.

## Example

```python
from energy_level_diagram import Diagram

diagram = Diagram(auto_regulation=True)
col_a = diagram.add_column([0, 1, 2])
col_b = diagram.add_column([0.5, 1.5, 2.5])
diagram.connect(col_a.levels[1], col_b.levels[0])
diagram.plot()
```

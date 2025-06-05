# energy-level-diagram

A simple library to plot energy level diagrams using Matplotlib. It supports multiple columns of levels, optional automatic regulation of level spacing, and dashed connections between columns.

## Example

```python
from energy_level_diagram import EnergyLevelDiagram

eld = EnergyLevelDiagram(auto_regulation=True)
eld.add_column([0, 1, 2])
eld.add_column([0.5, 1.5, 2.5])
eld.plot(connect=True)
```

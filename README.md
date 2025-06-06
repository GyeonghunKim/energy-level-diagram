# energy-level-diagram

A simple library to plot energy level diagrams using Matplotlib. It supports multiple columns of levels, optional automatic regulation of level spacing, and dashed connections between columns.

The `label` parameter sets the title of the diagram, and `plot()` now returns the
``matplotlib`` figure and axes objects for further customisation. Column labels
are drawn along the bottom of the diagram and the plot limits are calculated from
the bounding boxes of all artists. The padding around the plot can be adjusted
with the `padding` argument or per-side using `padding_left`,
`padding_right`, `padding_top` and `padding_bottom`. The gap between the lowest
level and the column labels is controlled by `column_label_gap`.

## Example scripts

The `examples` directory contains scripts demonstrating typical usage. You can run them directly with Python to see how the diagram API works.

```
python examples/basic_usage.py
python examples/vertical_arrow.py
python examples/broken_arrow.py
```

These scripts create diagrams using different features of the library but do not display their resulting plots here.


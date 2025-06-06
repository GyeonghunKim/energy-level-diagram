from energy_level_diagram import Diagram

# Demonstrates using a vertical arrow between two levels

diagram = Diagram(auto_regulation=True)
column = diagram.add_column([0, 1, 2, 3], label="Levels")

# Add a vertical arrow between the bottom and top level

diagram.add_vertical_arrow(column.levels[0], column.levels[-1], x=0.25, label="transition")

diagram.plot(show_level_name=True, show_column_name=True)

from energy_level_diagram import Diagram

# Demonstrates using a broken vertical arrow to indicate a large energy gap

diagram = Diagram(auto_regulation=True)
column = diagram.add_column([0, 1, 5], label="Levels")

# Add a broken arrow between the bottom and top level

diagram.add_vertical_broken_arrow(column.levels[0], column.levels[-1], x=0.25, label="gap")

diagram.plot(show_level_name=True, show_column_name=True)

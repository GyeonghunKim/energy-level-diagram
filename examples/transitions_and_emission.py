from energy_level_diagram import Diagram

# Demonstrates transition and spontaneous emission arrows

diagram = Diagram(auto_regulation=True)
col = diagram.add_column([0, 1, 2], label="Levels")

# Add transition from top to middle level with custom color

diagram.add_transition(col.levels[2], col.levels[1], x=0.25, label="transition", color="blue")

# Add spontaneous emission from middle to bottom level

diagram.add_spontaneous_emission(col.levels[1], col.levels[0], x=0.35, label="emission")

# Also show frequency splitting between bottom and top

diagram.add_vertical_arrow(col.levels[0], col.levels[2], x=0.15, label="splitting")

diagram.plot(show_level_name=True, show_column_name=True)

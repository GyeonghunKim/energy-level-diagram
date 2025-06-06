from energy_level_diagram import Diagram

# Basic example with two columns and one connection

diagram = Diagram(auto_regulation=True)
column_a = diagram.add_column([0, 1, 2], label="A")
column_b = diagram.add_column([0.5, 1.5, 2.5], label="B")

# connect the middle level of column A to the bottom level of column B

diagram.connect(column_a.levels[1], column_b.levels[0])

diagram.plot(show_level_name=True, show_column_name=True)

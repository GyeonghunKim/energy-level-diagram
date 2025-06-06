import os
import sys
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from energy_level_diagram import Diagram, Column, Level


def test_add_column_and_levels():
    diagram = Diagram()
    col = diagram.add_column([1.0, 2.0], label="A")
    col.add_level(3.0, label="extra")
    assert len(diagram.columns) == 1
    assert len(col.levels) == 3
    assert isinstance(col.levels[0], Level)
    assert col.levels[0].column is col


def test_compute_column_positions():
    diagram = Diagram()
    diagram.add_column([0], width=0.5, separation=1.0)
    diagram.add_column([0], width=0.2, separation=0.3)
    diagram.add_column([0], width=0.4, separation=0.4)
    positions = diagram._compute_column_positions()
    assert positions == [0.0, 1.5, 2.0]


def test_regulate_levels_auto():
    diagram = Diagram(auto_regulation=True)
    result = diagram._regulate_levels([0.0, 1.0, 2.0])
    assert result == [0.0, 0.5, 1.0]


def test_regulate_levels_no_auto():
    diagram = Diagram(auto_regulation=False)
    energies = [0.0, 1.0, 2.0]
    result = diagram._regulate_levels(energies)
    assert result == energies


def test_connections_and_arrows():
    diagram = Diagram()
    col1 = diagram.add_column([0, 1])
    col2 = diagram.add_column([0, 1])
    diagram.connect(col1.levels[0], col2.levels[1])
    diagram.add_vertical_arrow(col1.levels[1], col2.levels[0], x=0.5, label="test")
    assert diagram._connections == [(col1.levels[0], col2.levels[1])]
    assert diagram._arrows == [(col1.levels[1], col2.levels[0], 0.5, "test", "black")]


def test_add_vertical_broken_arrow():
    diagram = Diagram()
    col = diagram.add_column([0, 1])
    diagram.add_vertical_broken_arrow(col.levels[0], col.levels[1], x=0.5, label="gap", break_position=0.6)
    assert diagram._broken_arrows == [(col.levels[0], col.levels[1], 0.5, "gap", 0.6, "black")]


def test_add_transition_and_emission():
    diagram = Diagram()
    col = diagram.add_column([0, 1, 2])
    diagram.add_transition(col.levels[2], col.levels[1], x=0.3)
    diagram.add_spontaneous_emission(col.levels[1], col.levels[0], x=0.4, color="purple")
    assert diagram._transitions == [(col.levels[2], col.levels[1], 0.3, None, "blue")]
    assert diagram._emissions == [(col.levels[1], col.levels[0], 0.4, None, "purple")]


def test_plot_invokes_matplotlib(monkeypatch):
    diagram = Diagram()
    diagram.add_column([0, 1])
    diagram.add_column([1, 2])
    called = {}

    def fake_show():
        called['show'] = True

    monkeypatch.setattr(plt, "show", fake_show)
    diagram.plot(connect=True, show_level_name=True, show_column_name=True, debug_mode=True)
    assert called.get('show')


def test_plot_with_padding(monkeypatch):
    diagram = Diagram()
    diagram.add_column([0, 1])
    called = {}

    def fake_show():
        called['show'] = True

    monkeypatch.setattr(plt, "show", fake_show)
    diagram.plot(
        padding_left=0.1,
        padding_right=0.2,
        padding_top=0.3,
        padding_bottom=0.4,
        column_label_gap=0.2,
    )
    assert called.get('show')

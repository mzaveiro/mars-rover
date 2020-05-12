# pylint:disable=redefined-outer-name
'''Test Control class'''
import pytest

import rover.control


@pytest.fixture
def controller():
    """Helper that instantiates the Control class"""
    return rover.control.Control()


@pytest.fixture
def possible_states():
    """Helper that instantiates State class"""
    return rover.control.State


@pytest.mark.parametrize("boundary,expect", [
    ("5 5", True),
    ("5 5 N", False),
    ("MLLR", False),
    ("5 R", False),
    ("-1 -1", False)
])
def test_process_boundary(controller, boundary, expect):
    """Sanity check on setting boundaries"""
    assert controller.process_boundary(boundary) == expect


@pytest.mark.parametrize("coordinates,expect", [
    ("5 5 N", True),
    ("5 5", False),
    ("MLLR", False),
    ("5 5 R", False),
    ("L 5 N", False)
])
def test_process_coordinates(controller, coordinates, expect):
    """Sanity check on setting coordinates"""
    controller.process_boundary("5 5")
    assert controller.process_coordinates(coordinates) == expect


@pytest.mark.parametrize("cmds,expect", [
    ("MLLR", "2 2 N"),
    ("5 5 N", "1 2 E"),
    ("5 5", "1 2 E"),
    ("5 5 R", "1 2 S"),
    ("L 5 N", "1 2 N")
])
def test_process_cmds(controller, cmds, expect):
    """Sanity check on setting commands"""
    controller.process_boundary("5 5")
    controller.process_coordinates("1 2 E")
    assert controller.process_cmds(cmds) == expect


def test_good_process_seq(controller, possible_states):
    """Check a normal sequence of commands"""
    assert controller.state == possible_states.WAIT_BOUNDARY
    controller.process("5 5")
    assert controller.state == possible_states.WAIT_COORDINATES
    controller.process("1 2 E")
    assert controller.state == possible_states.WAIT_CMDS
    controller.process("LLRMM")
    assert controller.state == possible_states.WAIT_COORDINATES


def test_wrong_process_seq(controller, possible_states):
    """Check a normal sequence of commands"""
    assert controller.state == possible_states.WAIT_BOUNDARY
    controller.process("1 2 E")
    assert controller.state == possible_states.WAIT_BOUNDARY
    controller.process("5 5")
    assert controller.state == possible_states.WAIT_COORDINATES
    controller.process("LLRMM")
    assert controller.state == possible_states.WAIT_COORDINATES
    controller.process("1 2 E")
    assert controller.state == possible_states.WAIT_CMDS
    controller.process("LLRMM")
    assert controller.state == possible_states.WAIT_COORDINATES

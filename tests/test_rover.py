# pylint:disable=redefined-outer-name
'''Test Rover class'''
import pytest

import rover.exceptions as exceptions
import rover.rover


@pytest.fixture
def test_rover():
    """Helper that instantiates the Rover class"""
    new_rover = rover.rover.Rover()
    new_rover.set_boundaries(5, 5)
    return new_rover


@pytest.mark.parametrize("x,y,orientation,expect", [
    [1, 2, "N", "1 2 N"],
])
def test_initial_position(test_rover, x, y, orientation, expect):
    '''Sanity check on setting the initial position'''
    test_rover.set_inital_position(x, y, orientation)
    assert str(test_rover.navigation.location) == expect


@pytest.mark.parametrize("x,y", [
    [-1, -1],
    [-1, 0],
    [0, -1],
])
def test_invalid_boundary(test_rover, x, y):
    """Test boundary lower limits"""
    with pytest.raises(exceptions.InvalidBoundary):
        test_rover.set_boundaries(x, y)


@pytest.mark.parametrize("x,y,orientation,exp", [
    [6, 6, "N", exceptions.BoundaryError],
    [3, 4, "T", exceptions.InvalidCardinalPoint],
])
def test_invalid_initial(test_rover, x, y, orientation, exp):
    """Test invalid set up"""
    with pytest.raises(exp):
        test_rover.set_inital_position(x, y, orientation)


@pytest.mark.parametrize("initial_coord,cmds,expect", [
    ((1, 2, "N"), "LMLMLMLMM", "1 3 N"),
    ((3, 3, "E"), "MMRMMRMRRM", "5 1 E"),
])
def test_navigation(test_rover, initial_coord, cmds, expect):
    """Test rover's navigation"""
    test_rover.set_inital_position(*initial_coord)
    final_coord = test_rover.navigate(cmds)
    assert final_coord == expect


@pytest.mark.parametrize("cmds,expect", [
    ("MMMMMMMMMMMMMMMMMM", "0 5 N"),
    ("MMMTRUM", "1 3 E"),
])
def test_invalid_wont_crash(test_rover, cmds, expect):
    """Invalid commands shouldn't make the rover crash"""
    final_coord = test_rover.navigate(cmds)
    assert final_coord == expect

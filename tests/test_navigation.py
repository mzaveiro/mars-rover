# pylint:disable=redefined-outer-name
'''Test navigation system'''
import pytest

import rover.navigation
import rover.cardinal as cardinal
import rover.expections as expections


@pytest.fixture
def navigation():
    '''Fixture helper that instantiate Navigation'''
    return rover.navigation.Navigation()


def test_set_cardinal_points(navigation):
    '''Basic test on the initial cardinal points list setup'''
    nav = navigation

    assert str(nav.head) == cardinal.North.short_name
    assert nav.head.left is None
    assert str(nav.tail) == cardinal.West.short_name
    assert nav.tail.right is None


@pytest.mark.parametrize('expect', [4])
def test_list_has_all_cardinal_points(navigation, expect):
    '''Test whether we have all 4 cardinal points in the list'''
    nav = navigation
    count = 1
    orientation_list = nav.head
    while orientation_list.right:
        count += 1
        orientation_list = orientation_list.right

    assert count == expect


@pytest.mark.parametrize('cardinals', [
    (cardinal.North(),),
    (cardinal.East(), cardinal.South()),
])
def test_add_cardinal_point(navigation, cardinals):
    """Test adding cardinal points"""
    nav = navigation
    # clean state
    nav.head = None
    nav.tail = None

    for orientation in cardinals:
        nav.add_cardinal_point(orientation)

    assert str(nav.head) == str(cardinals[0])
    assert str(nav.tail) == str(cardinals[-1])


@pytest.mark.parametrize('orientation', ["N", "S", "E", "W"])
def test_set_initial_orientation(navigation, orientation):
    '''Test setting all 4 cardinal points'''
    nav = navigation
    nav.set_initial_orientation(orientation)
    assert str(nav.location.orientation) == orientation


@pytest.mark.parametrize('position, expect', [
    ((1, 2), (1, 2)),
    pytest.param((3, 4), (4, 4), marks=pytest.mark.xfail),
])
def test_set_position(navigation, position, expect):
    '''Sanity check on setting position'''
    nav = navigation
    nav.set_position(position)
    assert nav.location.position == expect


@pytest.mark.parametrize('boundary, expect', [
    ((1, 2), (1, 2)),
    pytest.param((3, 4), (4, 4), marks=pytest.mark.xfail),
])
def test_set_boundaries(navigation, boundary, expect):
    '''Sanity check on setting boundary'''
    nav = navigation
    nav.set_boundaries(boundary)
    assert nav.location.boundaries == expect


@pytest.mark.parametrize('n_times,expect', [
    (1, 'W'),
    (2, 'S'),
    (3, 'E'),
    (4, 'N'),
    (5, 'W'),
])
def test_move_left(navigation, n_times, expect):
    '''Move n times and check orientation'''
    nav = navigation
    for _ in range(n_times):
        nav.move_left()
    assert str(nav.location.orientation) == expect


@pytest.mark.parametrize('n_times,expect', [
    (1, 'E'),
    (2, 'S'),
    (3, 'W'),
    (4, 'N'),
    (5, 'E'),
])
def test_move_right(navigation, n_times, expect):
    '''Move n times and check orientation'''
    nav = navigation
    for _ in range(n_times):
        nav.move_right()
    assert str(nav.location.orientation) == expect


@pytest.mark.parametrize("position,orientation,expect", [
    ((3, 3), "N", (3, 4)),
    ((3, 3), "S", (3, 2)),
    ((3, 3), "E", (4, 3)),
    ((3, 3), "W", (2, 3)),
    ((0, 0), "E", (1, 0)),
    ((0, 0), "N", (0, 1)),
    ((0, 5), "S", (0, 4)),
    ((0, 5), "E", (1, 5)),
    ((5, 5), "S", (5, 4)),
    ((5, 5), "W", (4, 5)),
    ((5, 0), "W", (4, 0)),
    ((5, 0), "N", (5, 1)),
])
def test_move(navigation, position, orientation, expect):
    '''Test basic moves on all cardinal points'''
    nav = navigation
    nav.set_position(position)
    nav.set_initial_orientation(orientation)
    nav.set_boundaries((5, 5))
    nav.move()
    assert nav.location.position == expect


@pytest.mark.parametrize("position,orientation", [
    ((0, 0), "W"),
    ((0, 0), "S"),
    ((0, 5), "N"),
    ((0, 5), "W"),
    ((5, 5), "N"),
    ((5, 5), "E"),
    ((5, 0), "E"),
    ((5, 0), "S"),
])
def test_invalid_moves(navigation, position, orientation):
    '''Test the boundaries invalid moves'''
    nav = navigation
    nav.set_position(position)
    nav.set_initial_orientation(orientation)
    nav.set_boundaries((5, 5))
    with pytest.raises(expections.BoundaryError):
        nav.move()


@pytest.mark.parametrize("func,cmd", [
    ("move_left", "L"),
    ("move_right", "R"),
    ("move", "M"),
])
def test_process_cmd(navigation, mocker, func, cmd):
    """Test calling all available commands"""
    nav = navigation
    nav.set_boundaries((1, 1))
    spy = mocker.spy(nav, func)
    nav.process_cmd(cmd)
    spy.assert_called_once()


def test_invalid_cmd(navigation):
    """Test one invalid command"""
    nav = navigation
    with pytest.raises(expections.InvalidCommand):
        nav.process_cmd("E")

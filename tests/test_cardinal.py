'''Test basic cardinal points functionalities'''
import pytest

import rover.cardinal as cardinal


@pytest.mark.parametrize("position,class_name,expect", [
    ((0, 0), cardinal.North, (0, 1)),
    pytest.param((0, 0), cardinal.North, (0, 2), marks=pytest.mark.xfail),
    pytest.param((0, 0), cardinal.North, (1, 1), marks=pytest.mark.xfail),
    ((0, 1), cardinal.South, (0, 0)),
    pytest.param((0, 1), cardinal.South, (0, -1), marks=pytest.mark.xfail),
    pytest.param((0, 1), cardinal.South, (1, 0), marks=pytest.mark.xfail),
    ((0, 0), cardinal.East, (1, 0)),
    pytest.param((0, 0), cardinal.East, (2, 0), marks=pytest.mark.xfail),
    pytest.param((0, 0), cardinal.East, (1, 1), marks=pytest.mark.xfail),
    ((1, 0), cardinal.West, (0, 0)),
    pytest.param((1, 0), cardinal.West, (-1, 0), marks=pytest.mark.xfail),
    pytest.param((1, 0), cardinal.West, (0, 1), marks=pytest.mark.xfail),
])
def test_move(position, class_name, expect):
    """Test possible moves

    For each cardinal position, the sequency is:
        1 - valid move
        2 - move in the right axis, but a number larger than 1
        3 - move in the wrong axis
    """
    cardinal_point = class_name()
    assert cardinal_point.move(position) == expect


@pytest.mark.parametrize("class_name,expect", [
    (cardinal.North, 'N'),
    pytest.param(cardinal.North, 'S', marks=pytest.mark.xfail),
    (cardinal.South, 'S'),
    pytest.param(cardinal.South, 'N', marks=pytest.mark.xfail),
    (cardinal.East, 'E'),
    pytest.param(cardinal.East, 'N', marks=pytest.mark.xfail),
    (cardinal.West, 'W'),
    pytest.param(cardinal.West, 'N', marks=pytest.mark.xfail),
])
def test_short_names(class_name, expect):
    '''Sanity check of the short names'''
    assert class_name().short_name == expect

@pytest.mark.parametrize("class_name,expect", [
    (cardinal.North, 'N'),
    pytest.param(cardinal.North, 'S', marks=pytest.mark.xfail),
    (cardinal.South, 'S'),
    pytest.param(cardinal.South, 'N', marks=pytest.mark.xfail),
    (cardinal.East, 'E'),
    pytest.param(cardinal.East, 'N', marks=pytest.mark.xfail),
    (cardinal.West, 'W'),
    pytest.param(cardinal.West, 'N', marks=pytest.mark.xfail),
])
def test_str_convertion(class_name, expect):
    '''Sanity check of str to short name'''
    assert str(class_name()) == expect


@pytest.mark.parametrize("class_name,expect", [
    (cardinal.North, 'North'),
    pytest.param(cardinal.North, 'N', marks=pytest.mark.xfail),
    (cardinal.South, 'South'),
    pytest.param(cardinal.South, 'S', marks=pytest.mark.xfail),
    (cardinal.East, 'East'),
    pytest.param(cardinal.East, 'E', marks=pytest.mark.xfail),
    (cardinal.West, 'West'),
    pytest.param(cardinal.West, 'W', marks=pytest.mark.xfail),
])
def test_long_names(class_name, expect):
    '''Sanity check of the long names'''
    assert class_name().long_name == expect


def test_base_class_expection():
    """Sanity check on abstract method

    Since CardinalPoints is an abstract class, it can't be instantiated alone.
    """
    with pytest.raises(TypeError):
        cardinal.CardinalPoints()

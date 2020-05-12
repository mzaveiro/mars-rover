# pylint:disable=redefined-outer-name
'''Test LocationStorage class'''

import pytest

import rover.cardinal as cardinal
import rover.location_storage as location_storage


@pytest.fixture(scope="module")
def location():
    """Fixture with a global LocationStorage.

    Since we don't need to create it every time, we have a global fixture. It
    also tests whether constantly changing the class doesn't affects the
    other tests.
    """
    return location_storage.LocationStorage()


@pytest.mark.parametrize("position,expect", [
    ((2, 3), (2, 3)),
    pytest.param((4, 3), (5, 6), marks=pytest.mark.xfail),
])
def test_position(position, expect, location):
    """Test whether can set the position"""
    location.position = position
    assert location.position == expect


@pytest.mark.parametrize("boundary,expect", [
    ((2, 3), (2, 3)),
    pytest.param((4, 3), (5, 6), marks=pytest.mark.xfail),
])
def test_boundary(boundary, expect, location):
    """Test whether can set boundaries"""
    location.boundaries = boundary
    assert location.boundaries == expect


@pytest.mark.parametrize("orientation_class,expect", [
    (cardinal.North, 'N'),
    pytest.param(cardinal.South, "n", marks=pytest.mark.xfail),
])
def test_orientation(orientation_class, expect, location):
    """Test whether can set the orientation"""
    location.orientation = orientation_class()
    assert str(location.orientation) == expect

'''Location Storage

This module stores the run-time information, like the position, boundaries and
rover orientation.
'''


class LocationStorage:
    '''Holds the rover's run-time data'''
    lower_boundary = (0, 0)

    def __init__(self):
        self._position = self.lower_boundary
        self._boundaries = (0, 0)
        self._orientation = None

    def __str__(self):
        x, y = self.position
        return f"{x} {y} {self.orientation}"

    @property
    def position(self):
        '''Stores the rover's position as a tuple'''
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    @property
    def boundaries(self):
        '''Stores the limits the rover can go as a tuple'''
        return self._boundaries

    @boundaries.setter
    def boundaries(self, new_boundaries):
        self._boundaries = new_boundaries

    @property
    def orientation(self):
        '''Stores the current cardinal position as a :class: `cardinal` obj'''
        return self._orientation

    @orientation.setter
    def orientation(self, new_orientation):
        self._orientation = new_orientation

'''Navigation module

This module controls the rover navigation.

The rover's navigation system uses something similar to a double linked list
where the head is North and, moving right, the tail is West as shown below:

(head)N <--> E <--> S <--> W (tail)

For each node, it can see left and right what the cardinal point is and if it
reaches one of the extremes, it just switches between head/tail, depending on
where it is. It doesn't make a direct link between West and North as it is more
prone of infinite lookups, so it's better to avoid it.

For instance:

Rover is facing West and receives a command to turn 90 degrees right. The
navigation systems knows it has reached the end of the list of cardinal points
so it resets to head.
'''
import logging
import pathlib

from . import cardinal
from . import location_storage
from . import expections


class Navigation():
    '''Controls the hover navigation system'''

    def __init__(self):
        self.head = None
        self.tail = None
        self.logger = logging.getLogger(pathlib.PurePath(__file__).name)
        self.location = location_storage.LocationStorage()
        self.set_cardinal_points()

    def __str__(self):
        '''String representation of the class lists all cardinal points'''
        last = self.head
        all_nodes = [str(last)]
        while last.right:
            last = last.right
            all_nodes.append(str(last))
        return " ".join(all_nodes)

    def set_cardinal_points(self):
        '''Sets the 4 cardinal points into the list'''
        orientation_guide = (
            cardinal.North(),
            cardinal.East(),
            cardinal.South(),
            cardinal.West()
        )

        for cardinal_point in orientation_guide:
            self.add_cardinal_point(cardinal_point)
        # initiate the orientation
        self.location.orientation = self.head

    def add_cardinal_point(self, node):
        '''Add a cardinal point

        :param node: The cardinal point you want to add
        :type node: :class: `cardinal.CardinalPoints`
        '''

        # no head, to initiate both head and tail
        if self.head is None:
            self.head = node
            self.tail = node
            return

        # tail is the last element of the list, so first add new node to
        # the right of it.
        self.tail.right = node
        # link the left of the new node to the current last element
        node.left = self.tail
        # everything set, so now make the new node as the end of the list
        self.tail = node
        # make sure the last element always points to None to the right, i.e.,
        # no further elements after the tail
        self.tail.right = None

    def set_initial_orientation(self, orientation):
        '''Initiate the orientation list

        Here the set the rover to face to the given direction by starting at
        head and moving right until finding the desired orientation.

        :param orientation: The desired cardinal position (N, S, E or W)
        :type orientation: str
        '''

        self.logger.debug("head: %s", self.head)
        # set current to the head of the list (first cardinal point)
        current_orientation = self.head
        # keep going right until you find the element
        while current_orientation.right:
            if current_orientation.short_name == orientation:
                break
            current_orientation = current_orientation.right
        self.set_orientation(current_orientation)
        self.logger.debug("initial orientation: %s", self.location.orientation)

    def set_orientation(self, new_orientation):
        '''Set the rover's orientation

        :param new_orientation: The desired orientation we want to set
        :type new_orientation: tuple
        '''
        self.location.orientation = new_orientation

    def set_position(self, new_position):
        '''Set the rover's position

        :param new_position: The desired position we want to set
        :type new_position: tuple
        '''
        self.location.position = new_position

    def set_boundaries(self, new_boundaries):
        '''Set the rover's boundaries (limits)

        :param new_boundaries: The desired boundary we want to set
        :type new_boundaries: tuple
        '''
        self.location.boundaries = new_boundaries

    def move_left(self):
        '''Change rover's direction to the left'''

        # get the the current orientation
        current = self.location.orientation

        # if reached the limit to the left (first cardinal point of the list),
        # reset to tail (last cardinal point)
        new_orientation = self.tail if current.left is None else current.left
        self.set_orientation(new_orientation)
        self.logger.info("to the left, now %s", self.location.orientation)

    def move_right(self):
        '''Change rover's direction to the right'''

        # get the the current orientation
        current = self.location.orientation

        # if reached the limit to the right (last cardinal point of the list),
        # reset to head (first cardinal point)
        new_orientation = self.head if current.right is None else current.right
        self.set_orientation(new_orientation)
        self.logger.info("to the right, now %s", self.location.orientation)

    def move(self):
        '''Move the rover'''

        position = self.location.position
        boundary = self.location.boundaries
        orientation = self.location.orientation
        new_position = orientation.move(position)
        self.logger.info("move to %s", new_position)
        x_min, y_min = self.location.lower_boundary
        x_max, y_max = boundary
        x, y = new_position
        if not(x_min <= x <= x_max and y_min <= y <= y_max):
            raise expections.BoundaryError("Outside of boundaries")

        self.set_position(new_position)

    def process_cmd(self, command):
        '''Process each command sent by central server'''
        if command == 'L':
            self.move_left()
        elif command == 'R':
            self.move_right()
        elif command == 'M':
            self.move()
        else:
            raise expections.InvalidCommand("Invalid command")

#!/usr/bin/env python
import abc


class Orientation():
    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        self.right = None
        self.left = None
        self.data = data

    def __str__(self):
        return self.data

    @abc.abstractmethod
    def move(self, position):
        """Implement move on the children classes"""


class North(Orientation):
    def move(self, position):
        x, y = position
        return x, y+1


class South(Orientation):
    def move(self, position):
        x, y = position
        return x, y-1


class East(Orientation):
    def move(self, position):
        x, y = position
        return x+1, y


class West(Orientation):
    def move(self, position):
        x, y = position
        return x-1, y


class Navigation():
    def __init__(self):
        self.head = None
        self.tail = None
        self.location = LocationStorage()

    def __str__(self):
        last = self.head
        all_nodes = [str(last)]
        while last.right:
            last = last.right
            all_nodes.append(str(last))
        return " ".join(all_nodes)

    def add(self, node):
        #  print(node)
        if self.head is None:
            self.head = node
            self.tail = node
            return

        self.tail.right = node
        node.left = self.tail
        self.tail = node
        self.tail.right = None

    def set_inital_orientation(self, orientation):
        current_orientation = self.head
        print(f"head: {self.head}")
        while current_orientation.right:
            if current_orientation.data == orientation:
                break
            current_orientation = current_orientation.right
        self.location.orientation = current_orientation
        print(self.location.orientation)

    def set_position(self, new_position):
        self.location.position = new_position

    def set_boundaries(self, new_boundaries):
        self.location.boundaries = new_boundaries

    def move_left(self):
        current = self.location.orientation
        # reached the left orientation boundary so we reset to tail
        new_orientation = self.tail if current.left is None else current.left
        self.location.orientation = new_orientation
        print(self.location.orientation)

    def move_right(self):
        current = self.location.orientation
        new_orientation = self.head if current.right is None else current.right
        self.location.orientation = new_orientation
        print(self.location.orientation)

    def move(self):
        position = self.location.position
        boundary = self.location.boundaries
        orientation = self.location.orientation
        new_position = orientation.move(position)
        print(f"move {new_position}")
        if new_position > boundary:
            raise Exception("Outside of boundaries")

        self.set_position(new_position)

    def process_cmd(self, command):
        if command == 'L':
            self.move_left()
        elif command == 'R':
            self.move_right()
        elif command == 'M':
            self.move()


class LocationStorage:
    def __init__(self):
        self._position = (0, 0)
        self._boundaries = (0, 0)
        self._orientation = None

    def __str__(self):
        x, y = self.position
        return f"{x} {y} {self.orientation}"

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    @property
    def boundaries(self):
        return self._boundaries

    @boundaries.setter
    def boundaries(self, new_boundaries):
        self._boundaries = new_boundaries

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, new_orientation):
        self._orientation = new_orientation


class Rover:
    def __init__(self):
        self.navigation = Navigation()

    def set_orientation(self):
        orientation_guide = (North("N"), East("E"), South("S"), West("W"))

        for position in orientation_guide:
            self.navigation.add(position)

    def set_boundaries(self, x, y):
        self.navigation.set_boundaries((x, y))

    def set_inital_position(self, x, y, orientation):
        self.navigation.set_position((x, y))
        self.navigation.set_inital_orientation(orientation)

    def navigate(self, commands):
        cmds = list(commands)
        for cmd in cmds:
            self.navigation.process_cmd(cmd)
            print(self.navigation.location)

        print(self.navigation.location)

if __name__ == "__main__":
    rover = Rover()
    rover.set_orientation()
    #  print(rover.orientation)
    rover.set_boundaries(5, 5)

    rover.set_inital_position(1, 2, 'N')
    rover.navigate('LMLMLMLMM')

    rover.set_inital_position(3, 3, 'E')
    rover.navigate('MMRMMRMRRM')

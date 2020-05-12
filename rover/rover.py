#!/usr/bin/env python
import cardinal
import location_storage


class Navigation():
    def __init__(self):
        self.head = None
        self.tail = None
        self.location = location_storage.LocationStorage()
        self.set_cardinal_points()

    def __str__(self):
        last = self.head
        all_nodes = [str(last)]
        while last.right:
            last = last.right
            all_nodes.append(str(last))
        return " ".join(all_nodes)

    def set_cardinal_points(self):
        orientation_guide = (
            cardinal.North(),
            cardinal.East(),
            cardinal.South(),
            cardinal.West()
        )

        for cardinal_point in orientation_guide:
            self.add(cardinal_point)

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
            if current_orientation.short_name == orientation:
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


class Rover:
    def __init__(self):
        self.navigation = Navigation()

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
    #  print(rover.orientation)
    rover.set_boundaries(5, 5)

    rover.set_inital_position(1, 2, 'N')
    rover.navigate('LMLMLMLMM')

    rover.set_inital_position(3, 3, 'E')
    rover.navigate('MMRMMRMRRM')

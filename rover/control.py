"""Controls one or more rovers"""
import enum
import logging
import pathlib

from . import exceptions as exp
from . import rover


class State(enum.Enum):
    """Possible controller states"""
    WAIT_BOUNDARY = 1
    WAIT_COORDINATES = 2
    WAIT_CMDS = 3


class Control:
    """Holds status and rovers"""
    def __init__(self):
        self.state = State.WAIT_BOUNDARY
        self.logger = logging.getLogger(pathlib.PurePath(__file__).name)
        self.mars_hover = rover.Rover()

    def process_boundary(self, cmd):
        """Parses the cmd and send to rover to process

        :param cmd: Should contain the x, y limits of the plateau
        :type cmd: str

        :returns: True if the rover could process the cmd; otherwise, False
        """
        self.logger.debug("processing boundary")
        try:
            x, y = map(int, cmd.split(" "))
        except ValueError:
            self.logger.error("expected boundary command (x, y)")
            return False

        try:
            self.mars_hover.set_boundaries(x, y)
        except exp.InvalidBoundary as bd_err:
            self.logger.error(bd_err)
            return False

        return True

    def process_coordinates(self, cmd):
        """Parses the cmd and send to rover to process

        :param cmd: Should contain the x, y position and the orientation
        :type cmd: str

        :returns: True if the rover could process the cmd; otherwise, False
        """
        self.logger.debug("processing coordinates")
        try:
            x, y, orientation = cmd.split(" ")
            x, y = map(int, (x, y))
        except ValueError:
            self.logger.error(
                "expected coordinates command (x, y, orientation)")
            return False

        logging.debug("coordinates %s %s %s", x, y, orientation)

        try:
            self.mars_hover.set_inital_position(x, y, orientation)
        except (exp.InvalidCardinalPoint, exp.BoundaryError) as err:
            self.logger.error(err)
            return False

        return True

    def process_cmds(self, cmd):
        """Parses the cmd and send to rover to process

        :param cmd: Should contain the x, y position and the orientation
        :type cmd: str

        :returns: True if the rover could process the cmd; otherwise, False
        """
        self.logger.debug("processing commands")
        return self.mars_hover.navigate(cmd)

    def process(self, cmd):
        """Runs cmds in a defined order

        The cmds should be:
        1. boundary of the plateau
        2. initial coordinates
        3. navigation commands
        4. Go back to 2.

        :param cmd: The command we want to process
        :type cmd: str
        """
        if self.state == State.WAIT_BOUNDARY:
            if self.process_boundary(cmd):
                self.state = State.WAIT_COORDINATES

        elif self.state == State.WAIT_COORDINATES:
            if self.process_coordinates(cmd):
                self.state = State.WAIT_CMDS

        elif self.state == State.WAIT_CMDS:
            final_coordinates = self.process_cmds(cmd)
            print(final_coordinates)
            self.state = State.WAIT_COORDINATES

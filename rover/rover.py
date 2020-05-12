'''Rover module

This is the rover's interface between an external script that sends commands
and the rover's internal navigation system.
'''
import logging
import pathlib

from . import exceptions as exp
from . import navigation


class Rover:
    '''Rover interface module'''

    def __init__(self):
        self.logger = logging.getLogger(pathlib.PurePath(__file__).name)
        self.navigation = navigation.Navigation()

    def set_boundaries(self, x, y):
        '''Set the rover space boundary (limit) into the navigation system

        :param x: The x boundary coordinate
        :type x: int
        :param y: The y boundary coordinate
        :type y: int
        '''
        self.navigation.set_boundaries((x, y))

    def set_inital_position(self, x, y, orientation):
        '''Set the rover's initial position

        :param x: The x position coordinate
        :type x: int
        :param y: The y position coordinate
        :type y: int
        :param orientation: The cardinal point the rover is heading
        :type orientation: str
        '''
        self.navigation.set_position((x, y))
        self.navigation.set_initial_orientation(orientation)

    def navigate(self, commands):
        '''Navigate the rover according to a list of commands

        :param commands: A series of commands (L, R, M)
        :type commands: str

        :returns: The rover's location after all commands were processed
        :rtype: str
        '''
        # break the commands into a list
        cmds = list(commands)
        for cmd in cmds:
            try:
                self.navigation.process_cmd(cmd)
            except (exp.BoundaryError, exp.InvalidCommand) as err:
                logging.exception(err)
                continue
            self.logger.info(self.navigation.location)

        return str(self.navigation.location)

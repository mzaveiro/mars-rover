'''Cardinal

Module that holds the 4 cardinal points

Each module has it's own function that process what's the new coordinate
position in case a move command is fired. It also contains the idea of what's
the left and right cardinal point in relation to itself.

N <--> E <--> W <--> S

So, if you are pointing at E cardinal position, on your left is North and on
your right is South. This information is not hard-coded here, take a look at
:class: `navigation.Navigation` for more information.

The idea is to provide easy-to-debug classes as at any point a developer
can ``print`` or ``type`` the class to inspect the current cardinal point
it is dealing and possible moves. This information is also helpful when an
exception occurs as the trace event will tell the class name.
'''
import abc


class CardinalPoints(abc.ABC):
    '''Abstract class that provides interface for the cardinal points'''
    short_name = ""
    long_name = ""

    def __init__(self):
        self.right = None
        self.left = None

    def __str__(self):
        '''The string representation of the class

        :returns: The string that represents the class (N, S, E or W)
        '''
        return self.short_name

    @abc.abstractmethod
    def move(self, position):
        """Implement move on the children classes"""


class North(CardinalPoints):
    '''Class that represents North cardinal points and moves'''
    short_name = 'N'
    long_name = 'North'

    def move(self, position):
        '''Calculates new position when moving on its direction

        If you facing North, your new position is +1 in y axis

        :param position: A tuple that describes x and y position
        :type position: tuple

        :returns: The new calculated position
        :rtype: tuple
        '''
        x, y = position
        return x, y+1


class South(CardinalPoints):
    '''Class that represents South cardinal points and moves'''
    short_name = 'S'
    long_name = 'South'

    def move(self, position):
        '''Calculates new position when moving on its direction

        If you facing South, your new position is -1 in y axis

        :param position: A tuple that describes x and y position
        :type position: tuple

        :returns: The new calculated position
        :rtype: tuple
        '''
        x, y = position
        return x, y-1


class East(CardinalPoints):
    '''Class that represents East cardinal points and moves'''
    short_name = 'E'
    long_name = 'East'

    def move(self, position):
        '''Calculates new position when moving on its direction

        If you facing East, your new position is +1 in x axis

        :param position: A tuple that describes x and y position
        :type position: tuple

        :returns: The new calculated position
        :rtype: tuple
        '''
        x, y = position
        return x+1, y


class West(CardinalPoints):
    '''Class that represents West cardinal points and moves'''
    short_name = 'W'
    long_name = 'West'

    def move(self, position):
        '''Calculates new position when moving on its direction

        If you facing West, your new position is -1 in x axis

        :param position: A tuple that describes x and y position
        :type position: tuple

        :returns: The new calculated position
        :rtype: tuple
        '''
        x, y = position
        return x-1, y

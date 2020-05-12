'''Custom exceptions'''


class BoundaryError(Exception):
    """Out-of_boundary errors"""
    pass


class InvalidCommand(Exception):
    """Invalid commands sent"""
    pass


class InvalidCardinalPoint(Exception):
    """Invalid cardinal point"""
    pass


class InvalidBoundary(Exception):
    """Invalid boundary"""
    pass

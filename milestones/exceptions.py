"""
Application-specific exception classes used throughout the implementation
"""


class InvalidCourseKeyException(Exception):
    pass


class InvalidContentKeyException(Exception):
    pass


class InvalidMilestoneException(Exception):
    pass


class InvalidMilestoneRelationshipTypeException(Exception):
    pass


class InvalidUserException(Exception):
    pass

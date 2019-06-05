"""
Application-specific exception classes used throughout the implementation
"""
from __future__ import absolute_import, unicode_literals
from django.core.exceptions import ValidationError


class InvalidCourseKeyException(ValidationError):
    """ CourseKey validation exception class """


class InvalidContentKeyException(ValidationError):
    """ Course content/module/usage key validation exception class """


class InvalidCourseContentMilestoneRequirementsException(ValidationError):
    """ CourseContentMilestone.requirements validation exception class """


class InvalidMilestoneException(ValidationError):
    """ Milestone validation exception class """


class InvalidMilestoneRelationshipTypeException(ValidationError):
    """ Milestone Relationship Type validation exception class """


class InvalidUserException(ValidationError):
    """ User validation exception class """


def raise_exception(entity_type, entity, exception):
    """ Exception helper """
    raise exception(
        'The {} you have provided is not valid: {}'.format(entity_type, entity)
    )

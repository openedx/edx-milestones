"""
Validators confirm the integrity of inbound information prior to a data.py handoff
"""
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey, UsageKey

import data


def course_key_is_valid(course_key):
    """
    Course key object validation
    """
    if course_key is None:
        return False
    try:
        CourseKey.from_string(unicode(course_key))
    except InvalidKeyError:
        return False
    return True


def content_key_is_valid(content_key):
    """
    Course module/content/usage key object validation
    """
    if content_key is None:
        return False
    try:
        UsageKey.from_string(unicode(content_key))
    except InvalidKeyError:
        return False
    return True


def milestone_is_valid(milestone):
    """
    Milestone object validation
    """
    if milestone is None:
        return False
    if milestone.get('namespace') is None or len(milestone.get('namespace')) == 0:
        return False
    return True


def milestone_relationship_type_is_valid(name):
    """
    Milestone relationship type object validation
    """
    valid_types = [
        'requires',
        'fulfills',
    ]
    if name is None:
        return False
    if name not in valid_types:
        return False
    return True


def user_is_valid(user):
        """
    User object validation
    """
    if user is None:
        return False
    if not user.get('id', 0):
        return False
    return True

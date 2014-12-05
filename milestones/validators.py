"""
Validators confirm the integrity of inbound information prior to a data.py handoff
"""
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey, UsageKey

import data


def course_key_is_valid(course_key):
    if course_key is None:
        return False
    try:
        CourseKey.from_string(unicode(course_key))
    except InvalidKeyError:
        return False
    return True


def content_key_is_valid(content_key):
    if content_key is None:
        return False
    try:
        UsageKey.from_string(unicode(content_key))
    except InvalidKeyError:
        return False
    return True


def milestone_is_valid(milestone):
    if milestone is None:
        return False
    if not len(milestone.get('namespace', '')):
        return False
    return True


def milestone_relationship_type_is_valid(name):
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
    if user is None:
        return False
    if not user.get('id', 0):
        return False
    return True

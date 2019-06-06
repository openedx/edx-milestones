"""
Validators confirm the integrity of inbound information prior to a data.py handoff
"""
from __future__ import absolute_import, unicode_literals

import json
import six

from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey, UsageKey

from .data import fetch_milestone_relationship_types


def course_key_is_valid(course_key):
    """
    Course key object validation
    """
    if course_key is None:
        return False
    try:
        CourseKey.from_string(six.text_type(course_key))
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
        UsageKey.from_string(six.text_type(content_key))
    except InvalidKeyError:
        return False
    return True


def course_content_milestone_requirements_is_valid(requirements):
    """
    CourseContentMilestone.requirements should be a valid JSON string

    Args:
        requirements: JSON serializable object containing requirements data

    Returns:
        bool: True if valid, otherwise False
    """
    try:
        json.dumps(requirements)
    except TypeError:
        return False
    return True


def milestone_data_is_valid(milestone_data):
    """
    Milestone data validation
    """
    if milestone_data is None:
        return False
    if 'id' in milestone_data and not milestone_data.get('id'):
        return False
    if 'name' in milestone_data and not milestone_data.get('name'):
        return False
    if 'namespace' in milestone_data and not milestone_data.get('namespace'):
        return False
    return True


def milestone_relationship_type_is_valid(name):
    """
    Milestone relationship type object validation
    """
    return name in list(fetch_milestone_relationship_types().values())


def user_is_valid(user):
    """
    User object validation
    """
    if user is None:
        return False
    if not user.get('id', 0):
        return False
    return True

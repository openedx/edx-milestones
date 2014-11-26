"""
Validators are used by the MilestoneManager to confirm the validity of
inbound information prior to a data.py handoff
"""
import data
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey

def course_key_is_valid(course_key):
    if course_key is None:
        return False
    try:
        CourseKey.from_string(unicode(course_key))
    except InvalidKeyError:
        return False
    return True


def milestone_is_valid(milestone):
    if milestone is None:
        return False
    if not len(milestone.namespace):
        return False
    return True

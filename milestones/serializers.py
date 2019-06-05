"""
Data layer serialization operations.  Converts querysets to simple
python containers (mainly arrays and dicts).
"""
from __future__ import absolute_import, unicode_literals
import json

from . import models


def serialize_milestone(milestone):
    """
    Milestone object-to-dict serialization
    """
    return {
        'id': milestone.id,
        'name': milestone.name,
        'display_name': milestone.display_name,
        'namespace': milestone.namespace,
        'description': milestone.description
    }


def serialize_milestone_with_course(course_milestone):
    """
    CourseMilestone serialization (composite object)
    """
    return {
        'id': course_milestone.milestone.id,
        'name': course_milestone.milestone.name,
        'display_name': course_milestone.milestone.display_name,
        'namespace': course_milestone.milestone.namespace,
        'description': course_milestone.milestone.description,
        'course_id': course_milestone.course_id
    }


def serialize_milestone_with_course_content(course_content_milestone):
    """
    CourseContentMilestone serialization (composite object)
    """
    return {
        'id': course_content_milestone.milestone.id,
        'name': course_content_milestone.milestone.name,
        'display_name': course_content_milestone.milestone.display_name,
        'namespace': course_content_milestone.milestone.namespace,
        'description': course_content_milestone.milestone.description,
        'course_id': course_content_milestone.course_id,
        'content_id': course_content_milestone.content_id,
        'requirements': deserialize_requirements(course_content_milestone.requirements)
    }


def serialize_milestones(milestones):
    """
    Milestone serialization
    Converts list of objects to list of dicts
    """
    return [serialize_milestone(milestone) for milestone in milestones]


def deserialize_milestone(milestone_dict):
    """
    Milestone dict-to-object serialization
    """
    return models.Milestone(
        id=milestone_dict.get('id'),
        name=milestone_dict.get('name', ''),
        display_name=milestone_dict.get('display_name', ''),
        namespace=milestone_dict.get('namespace', ''),
        description=milestone_dict.get('description', '')
    )


def serialize_requirements(requirements):
    """
    Convert JSON serializable object to string
    """
    if requirements is not None:
        requirements = json.dumps(requirements)
    return requirements


def deserialize_requirements(requirements):
    """
    Convert JSON string to object
    """
    if requirements is not None:
        requirements = json.loads(requirements)
    else:
        requirements = {}
    return requirements

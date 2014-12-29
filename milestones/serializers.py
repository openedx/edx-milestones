"""
Data layer serialization operations.  Converts querysets to simple
python containers (mainly arrays and dicts).
"""
from . import models


def serialize_milestone(milestone):
    """
    Milestone object-to-dict serialization
    """
    return {
        'id': milestone.id,
        'name': milestone.name,
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
        'namespace': course_content_milestone.milestone.namespace,
        'description': course_content_milestone.milestone.description,
        'course_id': course_content_milestone.course_id,
        'content_id': course_content_milestone.content_id
    }


def serialize_milestones(milestones):
    """
    Milestone serialization
    Converts list of objects to list of dicts
    """
    response_data = []
    for milestone in milestones:
        response_data.append(serialize_milestone(milestone))
    return response_data


def deserialize_milestone(milestone_dict):
    """
    Milestone dict-to-object serialization
    """
    return models.Milestone(
        id=milestone_dict.get('id'),
        name=milestone_dict.get('name'),
        namespace=milestone_dict.get('namespace'),
        description=milestone_dict.get('description')
    )

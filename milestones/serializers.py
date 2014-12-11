"""
Data layer serialization operations.  Converts querysets to simple
python containers (mainly arrays and dicts).
"""
from models import Milestone


def serialize_milestone(milestone):
    return {
        'id': milestone.id,
        'name': milestone.name,
        'namespace': milestone.namespace,
        'description': milestone.description
    }


def serialize_milestone_with_course(course_milestone):
    return {
        'id': course_milestone.milestone.id,
        'name': course_milestone.milestone.name,
        'namespace': course_milestone.milestone.namespace,
        'description': course_milestone.milestone.description,
        'course_id': course_milestone.course_id
    }


def serialize_milestones(milestones):
    response_data = []
    for milestone in milestones:
        response_data.append(serialize_milestone(milestone))
    return response_data


def deserialize_milestone(milestone_dict):
    return Milestone(
        id=milestone_dict.get('id'),
        name=milestone_dict.get('name'),
        namespace=milestone_dict.get('namespace'),
        description=milestone_dict.get('description')
    )

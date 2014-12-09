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

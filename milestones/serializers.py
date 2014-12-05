"""
Data layer serialization operations.  Converts querysets to simple
python containers (mainly arrays and dicts).
"""
from models import Milestone

def serialize_milestone(milestone):
    return {
        'id': milestone.id,
        'namespace': milestone.namespace,
        'description': milestone.description
    }

def deserialize_milestone(milestone_dict):
    return Milestone(
        id=milestone_dict.get('id'),
        namespace=milestone_dict.get('namespace'),
        description=milestone_dict.get('description')
    )

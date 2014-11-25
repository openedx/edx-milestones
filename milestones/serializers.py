"""
Data layer serialization operations.  Converts querysets to simple
python containers (mainly arrays and dicts).
"""

def serialize_milestone(milestone):
    return {
        'id': milestone.id,
        'namespace': milestone.namespace,
        'description': milestone.description
    }

"""
Application data management/abstraction layer.  Responsible for:

1) Accessing information/state from internal and external resources
* Internal app models  (through models.py)
* External app models  (through direct ORM integrations, yuck)
* Remote data services (through resources.py)

2) Calculating derivative information from existing state
* Algorithms and data manipulations
* Aggregations
* Annotations
* Alternative data representations

Returns standard Python data structures (dicts, arrays of dicts) for easy consumption by callers
"""
import models as internal
import resources as remote
import serializers


def create_course_milestone(course_key, milestone, relationship):
        mrt, created = internal.MilestoneRelationshipType.objects.get_or_create(name=relationship)
        internal.CourseMilestone.objects.get_or_create(
            course_id=unicode(course_key),
            milestone=milestone,
            milestone_relationship_type=mrt,
        )


def create_milestone(milestone):
    return internal.Milestone.objects.create(
        namespace=milestone['namespace'],
        description=milestone['description']
    )


def get_course_milestones(course_key, type=None):

    if type is None:
        queryset = internal.Milestone.objects.filter(coursemilestone__course_id=unicode(course_key))
    else:
        mrt = internal.MilestoneRelationshipType.objects.get(name=type)
        queryset = internal.Milestone.objects.filter(
            coursemilestone__course_id=unicode(course_key),
            coursemilestone__milestone_relationship_type=mrt.id
        )
    course_milestones = []
    if len(queryset):
        for milestone in queryset:
            course_milestones.append(serializers.serialize_milestone(milestone))
    return course_milestones


def get_milestone(milestone, create):
    if milestone is not None:
        try:
            milestone = internal.Milestone.objects.get(namespace=milestone.namespace)
        except Milestone.DoesNotExist:
            if create:
                milestone = internal.Milestone.objects.create(
                    namespace=milestone.namespace,
                    description=milestone.description
                )
    return milestone

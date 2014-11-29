"""
Application data management/abstraction layer.  Responsible for:

1) Accessing information from various resources:
* Internal application state  (through local models in models.py)
* External application state  (ORM bindings with other apps, yuck)
* Remote data services (through service adapters in resources.py)

2) Calculating derivative information from existing state:
* Algorithms and data manipulations
* Aggregations
* Annotations
* Alternative data representations

Returns standard Python data structures (dicts, arrays of dicts) for
easy consumption and manipulation by callers -- the queryset stops here!
"""
from django.conf import settings

import serializers
import models as internal
if not settings.TEST_MODE:
    import resources as remote
else:
    import tests.mocks.resources as remote


def create_milestone(milestone):
    milestone, created = internal.Milestone.objects.get_or_create(
        namespace=milestone['namespace'],
        defaults={
            'description': milestone['description']
        }
    )

    return milestone


def get_milestone(milestone, create=False):
    if milestone is None:
        return milestone
    try:
        milestone = internal.Milestone.objects.get(namespace=milestone.get('namespace'))
        return milestone
    except internal.Milestone.DoesNotExist:
        if create:
            milestone = internal.Milestone.objects.create(
                namespace=milestone.namespace,
                description=milestone.description
            )
            return milestone
        return None


def create_course_milestone(course_key, relationship, milestone):
        mrt, created = internal.MilestoneRelationshipType.objects.get_or_create(name=relationship)
        internal.CourseMilestone.objects.get_or_create(
            course_id=unicode(course_key),
            milestone=milestone,
            milestone_relationship_type=mrt,
        )


def delete_course_milestone(course_key, relationship, milestone):
        try:
            mrt = internal.MilestoneRelationshipType.objects.get(name=relationship)
        except internal.MilestoneRelationshipType.DoesNotExist:
            # If the relationship type doesn't exist then we can't do much more
            # But it's okay, because the data's gone and we're deleting...
            pass
        try:
            internal.CourseMilestone.objects.get(
                course_id=unicode(course_key),
                milestone=milestone,
                milestone_relationship_type=mrt,
            ).delete()
        except internal.CourseMilestone.DoesNotExist:
            pass


def get_course_milestones(course_key, relationship=None):

    if relationship is None:
        queryset = internal.Milestone.objects.filter(coursemilestone__course_id=unicode(course_key))
    else:
        mrt = internal.MilestoneRelationshipType.objects.get(name=relationship)
        queryset = internal.Milestone.objects.filter(
            coursemilestone__course_id=unicode(course_key),
            coursemilestone__milestone_relationship_type=mrt.id
        )
    course_milestones = []
    if len(queryset):
        for milestone in queryset:
            course_milestones.append(serializers.serialize_milestone(milestone))
    return course_milestones


def delete_course_references(course_key):
    internal.CourseMilestone.objects.filter(course_id=unicode(course_key)).delete()
    internal.Milestone.objects.filter(namespace=unicode(course_key)).delete()

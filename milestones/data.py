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

Accepts and returns standard Python data structures (dicts, arrays of dicts)
for easy consumption and manipulation by callers -- the queryset stops here!
"""
from django.conf import settings

import serializers
import models as internal
if hasattr(settings, 'TEST_MODE') and settings.TEST_MODE:
    import tests.mocks.resources as remote
else:
    import resources as remote


def create_milestone(milestone):
    milestone_obj = serializers.deserialize_milestone(milestone)
    milestone, created = internal.Milestone.objects.get_or_create(
        namespace=milestone['namespace'],
        defaults={
            'description': milestone['description']
        }
    )

    return serializers.serialize_milestone(milestone)


def get_milestone(milestone, create=False):
    if milestone is None:
        return None
    milestone_obj = serializers.deserialize_milestone(milestone)
    try:
        if milestone_obj.id is not None:
            milestone = internal.Milestone.objects.get(id=milestone_obj.id)
        elif milestone_obj.namespace is not None:
            milestone = internal.Milestone.objects.get(namespace=milestone_obj.namespace)
        return serializers.serialize_milestone(milestone)
    except internal.Milestone.DoesNotExist:
        if create:
            milestone = internal.Milestone.objects.create(
                namespace=milestone_obj.namespace,
                description=milestone_obj.description
            ).save()
            return serializers.serialize_milestone(milestone)
        return None


def create_course_milestone(course_key, relationship, milestone):
        mrt, created = internal.MilestoneRelationshipType.objects.get_or_create(name=relationship)
        milestone_obj = serializers.deserialize_milestone(milestone)
        internal.CourseMilestone.objects.get_or_create(
            course_id=unicode(course_key),
            milestone=milestone_obj,
            milestone_relationship_type=mrt,
        )


def delete_course_milestone(course_key, relationship, milestone):
        milestone_obj = serializers.deserialize_milestone(milestone)
        try:
            mrt = internal.MilestoneRelationshipType.objects.get(name=relationship)
            try:
                internal.CourseMilestone.objects.get(
                    course_id=unicode(course_key),
                    milestone=milestone_obj.id,
                    milestone_relationship_type=mrt
                ).delete()
            except internal.CourseMilestone.DoesNotExist:
                pass

        except internal.MilestoneRelationshipType.DoesNotExist:
            # If the relationship type doesn't exist then we can't do much more
            # But it's okay, because the data's gone and we're deleting...
            try:
                internal.CourseMilestone.objects.get(
                    course_id=unicode(course_key),
                    milestone=milestone_obj.id,
                ).delete()
            except internal.CourseMilestone.DoesNotExist:
                pass

def get_course_milestones(course_key, relationship=None):

    if relationship is None:
        queryset = internal.Milestone.objects.filter(coursemilestone__course_id=unicode(course_key))
    else:
        try:
            mrt = internal.MilestoneRelationshipType.objects.get(name=relationship)
        except internal.MilestoneRelationshipType.DoesNotExist:
            # If the relationship type doesn't exist then we can't do much more
            return None
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

"""
The MilestoneManager is the orchestration layer that does all of the
internal running around so the api, receivers, and views don't have to.

Helplful Hint:  When modelling Milestones, I've found that it's helpful
to first consider the thing that fulfills the Milestone, and then
consider the thing that requires the Milestone.
"""
from .models import Milestone, CourseMilestone

class MilestoneManager(object):

    @classmethod
    def add_prerequisite_course_to_course(course_key, prerequisite_course_key, milestone=None):
        """
        Models the Pre-Requisite Course concept as single Milestone related to a pair of CourseMilestones
        1) Pre-Requisite Course fulfills Milestone
        2) Course requires Milestone
        """
        if milestone is not None:
            try:
                milestone = Milestone.objects.get(namespace=milestone.namespace)
            except Milestone.DoesNotExist:
                milestone = Milestone.objects.create(namespace=milestone.namespace, description=milestone.description)
        else:
            namespace = '{}'.format(prequisite_course_key)
            description = 'Auto-generated Course Completion Milestone for {}'.format(prerequisite_course_key)
            milestone = Milestone.objects.create(namespace=namespace, description=description)

        # Create the milestone links now that we have a milestone
        requires_mrt = MilestoneRelationshipType.objects.get_or_create(name='REQUIRES')
        CourseMilestone.objects.get_or_create(
            course_id=unicode(course_key),
            milestone=milestone,
            milestone_relationship_type=requires_mrt,
        )

        fulfills_mrt = MilestoneRelationshipType.objects.get_or_create(name='FULFILLS')
        CourseMilestone.objects.get_or_create(
            course_id=unicode(prerequisite_course_key),
            milestone=milestone,
            milestone_relationship_type=fulfills_mrt,
        )

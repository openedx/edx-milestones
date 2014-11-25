"""
The MilestoneManager is the orchestration layer that does all of the
internal running around so the api, receivers, and views don't have to.

Helplful Hint:  When modelling Milestones, I've found that it's helpful
to first consider the thing that fulfills the Milestone, and then
consider the thing that requires the Milestone.
"""
from data import create_course_milestone, create_milestone, get_course_milestones
from exceptions import InvalidMilestoneException
from validators import milestone_is_valid

class MilestoneManager(object):

    @classmethod
    def add_prerequisite_course_to_course(cls, **kwargs):
        """
        Models the Pre-Requisite Course concept as single Milestone related to a pair of CourseMilestones
        1) Pre-Requisite Course fulfills Milestone
        2) Course requires Milestone
        """
        course_key = kwargs.get('course_key')
        prerequisite_course_key = kwargs.get('prerequisite_course_key')
        milestone = kwargs.get('milestone')

        # If a milestone was provided, we'll need to do some checks
        # We also create one on-the-fly if it doesn't already exist
        if milestone is not None:
            if not milestone_is_valid(milestone):
                raise InvalidMilestoneException('The Milestone entity you have provided is not valid.')
            milestone = create_milestone({
                    'namespace': milestone.get('namespace'),
                    'description': milestone.get('description'),
                }
            )

        # If a milestone was not provided, we'll need to create one
        if milestone is None:
            auto_namespace = '{}'.format(prerequisite_course_key)
            auto_description = 'Auto-generated Course Completion Milestone for {}'.format(prerequisite_course_key)
            milestone = create_milestone({
                    'namespace': auto_namespace,
                    'description': auto_description,
                }
            )

        # Now that the milestone exists, we can link it to the specified courses
        create_course_milestone(course_key=course_key, milestone=milestone, relationship='requires')
        create_course_milestone(course_key=prerequisite_course_key, milestone=milestone, relationship='fulfills')

    @classmethod
    def get_course_milestones(cls, **kwargs):
        """
        Retrieves the set of milestones for a given course
        'type': optional filter on milestone relationship type
        Returns an array of dicts containing milestones
        """
        course_key = kwargs.get('course_key')
        type = kwargs.get('type')
        course_milestones = get_course_milestones(course_key, type=type)
        return get_course_milestones(course_key=course_key, type=type)

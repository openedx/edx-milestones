"""
The MilestoneManager is the orchestration layer that does all of the
internal running around so the api, receivers, and views don't have to.

Helplful Hint:  When modeling Milestones, I've found that it's helpful
to first consider the process for fulfilling the Milestone, and then
consider the process for requiring the Milestone.

State-altering operations should broadast signals when complete!
"""
import data
import exceptions
import signals
import validators

class MilestoneManager(object):

    @classmethod
    def _validate_course_key(cls, course_key):
        if not validators.course_key_is_valid(course_key):
            raise exceptions.InvalidCourseKeyException('The CourseKey you have provided is not valid')

    @classmethod
    def _validate_milestone(cls, milestone):
        if not validators.milestone_is_valid(milestone):
            raise InvalidMilestoneException('The Milestone you have provided is not valid.')

    @classmethod
    def get_milestone(cls, **kwargs):
        """
        Retrieves the specified milestone, either by id or namespace
        """
        milestone = {}
        if kwargs.get('id'):
            milestone['id'] = kwargs.get('id')
        if kwargs.get('namespace'):
            milestone['namespace'] = kwargs.get('namespace')

        cls._validate_milestone(milestone)
        return data.get_milestone(milestone)


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

        # Validate the course keys
        cls._validate_course_key(course_key)
        cls._validate_course_key(prerequisite_course_key)

        # If a milestone was provided, we'll need to check that as well
        # We'll create a record for it on-the-fly if one doesn't already exist
        if milestone is not None:
            cls._validate_milestone(milestone)
            milestone = data.create_milestone(
                {
                    'namespace': milestone.get('namespace'),
                    'description': milestone.get('description'),
                }
            )

        # If a milestone was not provided, we'll need to create one
        if milestone is None:
            auto_namespace = unicode(prerequisite_course_key)
            auto_description = 'Auto-generated Course Completion Milestone for {}'.format(prerequisite_course_key)
            milestone = data.create_milestone(
                {
                    'namespace': auto_namespace,
                    'description': auto_description,
                }
            )

        # Now that the milestone exists, we can link it to the specified courses
        data.create_course_milestone(course_key=course_key, relationship='requires', milestone=milestone)
        signals.course_milestone_added.send(
            sender=cls,
            course_key=course_key,
            relationship='requires',
            milestone=milestone
        )

        data.create_course_milestone(course_key=prerequisite_course_key, relationship='fulfills', milestone=milestone)
        signals.course_milestone_added.send(
            sender=cls,
            course_key=prerequisite_course_key,
            relationship='fulfills',
            milestone=milestone
        )

    @classmethod
    def remove_prerequisite_course_from_course(cls, **kwargs):
        course_key = kwargs.get('course_key')
        prerequisite_course_key = kwargs.get('prerequisite_course_key')
        milestone = kwargs.get('milestone')

        # Validate the course keys
        cls._validate_course_key(course_key)
        cls._validate_course_key(prerequisite_course_key)

        # If a milestone was provided, we'll need to check that as well
        if milestone is not None:
            _validate_milestone(milestone)

        # If a milestone wash't provided, we'll need to look for a generic one
        else:
            milestone = {
                'namespace': unicode(prerequisite_course_key)
            }
            milestone = data.get_milestone(milestone)

        # Okay, if we have a milestone...
        if milestone is not None:

            # Unlink it from the specified course and broadcast to the system
            data.delete_course_milestone(course_key=course_key, relationship='requires', milestone=milestone)
            signals.course_milestone_removed.send(
                sender=cls,
                course_key=course_key,
                relationship='requires',
                milestone=milestone
            )

    @classmethod
    def get_course_milestones(cls, **kwargs):
        """
        Retrieves the set of milestones for a given course
        'type': optional filter on milestone relationship type
        Returns an array of dicts containing milestones
        """
        course_key = kwargs.get('course_key')
        relationship = kwargs.get('relationship')
        return data.get_course_milestones(course_key=course_key, relationship=relationship)

    @classmethod
    def remove_course_references(cls, **kwargs):
        course_key = kwargs.get('course_key')
        cls._validate_course_key(course_key)
        data.delete_course_references(course_key)
        signals.course_references_removed.send(sender=cls, course_key=course_key)

# pylint: disable=too-many-public-methods
"""
Test Case Module for Milestones Signal Receivers
"""
from django.test import TestCase

from opaque_keys.edx.keys import CourseKey

import milestones.api as api

from milestones.tests.mocks import signals as mock_signals


class ReceiverTestCase(TestCase):
    """
    Main Test Suite for Milestones Signal Receivers
    """

    def setUp(self):
        """
        Test Case scaffolding
        """
        self.signal_log = []
        self.test_course_key = CourseKey.from_string('the/course/key')
        self.test_prerequisite_course_key = CourseKey.from_string('prerequisite/course/key')
        self.test_milestone_data = {
            'name': 'Test Milestone',
            'namespace': unicode(self.test_prerequisite_course_key),
            'description': 'This is only a test.',
        }

    def test_on_course_deleted(self):
        """
        Unit Test: test_on_course_deleted
        Note, this test adds a milestone and two course links
        We're going to confirm that all three entities are removed
        """

        # Add a new milestone and links to the system
        milestone = api.add_milestone(milestone=self.test_milestone_data)
        api.add_course_milestone(
            course_key=self.test_course_key,
            relationship='requires',
            milestone=milestone
        )
        api.add_course_milestone(
            course_key=self.test_prerequisite_course_key,
            relationship='fulfills',
            milestone=milestone
        )

        # Inform the milestones app that the prerequisite course has
        # now been removed from the system.
        mock_signals.course_deleted.send(
            sender=self,
            course_key=self.test_prerequisite_course_key
        )

        # Confirm the course relationship no longer exists
        prereq_milestones = api.get_course_milestones(course_key=self.test_prerequisite_course_key)
        self.assertEqual(len(prereq_milestones), 0)

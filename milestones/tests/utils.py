# pylint: disable=too-many-public-methods
"""
Utility module for Milestones test cases
"""
from django.contrib.auth.models import User
from django.test import TestCase

from opaque_keys.edx.keys import CourseKey, UsageKey


class MilestonesTestCaseBase(TestCase):
    """
    Parent/Base class for Milestones test cases
    """

    def setUp(self):
        """
        Helper method for test case scaffolding
        """
        self.test_course_key = CourseKey.from_string('the/course/key')
        self.test_prerequisite_course_key = CourseKey.from_string('the/prerequisite/key')
        self.test_content_key = UsageKey.from_string('i4x://the/content/key/12345678')
        self.test_user = User.objects.create(
            first_name='Test',
            last_name='User',
            email='test_user@edx.org',
            username='test_user',
            password='ABcd12!@'
        )
        self.serialized_test_user = self.test_user.__dict__

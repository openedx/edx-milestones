# pylint: disable=no-member,too-many-public-methods
"""
Utility module for Milestones test cases
"""
from __future__ import absolute_import, unicode_literals
from django.contrib.auth.models import User
from django.test import TestCase
from opaque_keys.edx.keys import CourseKey, UsageKey
from milestones.models import MilestoneRelationshipType


class MilestonesTestCaseBase(TestCase):
    """
    Parent/Base class for Milestones test cases
    """

    def setUp(self):
        """
        Helper method for test case scaffolding
        """
        super(MilestonesTestCaseBase, self).setUp()
        self.test_course_key = CourseKey.from_string('the/course/key')
        self.test_alternate_course_key = CourseKey.from_string('the/alternate_course/key')
        self.test_prerequisite_course_key = CourseKey.from_string('the/prerequisite/key')
        self.test_content_key = UsageKey.from_string('i4x://the/content/key/12345678')
        self.test_alternate_content_key = UsageKey.from_string('i4x://the/alternate_content/key/12345678')
        self.test_user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test_user@edx.org',
            username='test_user',
            password='ABcd12!@'
        )
        self.serialized_test_user = self.test_user.__dict__


class MilestonesTestCaseMixin(TestCase):
    """
    TestCase mixin for loading initial milestones data
    """
    def setUp(self):
        super(MilestonesTestCaseMixin, self).setUp()
        MilestoneRelationshipType.objects.get_or_create(name='requires')
        MilestoneRelationshipType.objects.get_or_create(name='fulfills')

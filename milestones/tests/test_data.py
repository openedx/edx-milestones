# pylint: disable=invalid-name
# pylint: disable=too-many-public-methods
"""
Milestones Data Module Test Cases

Note: 'Unit Test: ' labels are output to the console during test runs
"""
from __future__ import absolute_import, unicode_literals
import milestones.api as api
import milestones.data as data
import milestones.exceptions as exceptions
import milestones.tests.utils as utils
import six


class MilestonesDataTestCase(utils.MilestonesTestCaseBase):
    """
    Main Test Case module for Milestones Data
    Many of the module operations are covered indirectly via the test_api.py test suite
    So at the moment we're mainly focused on hitting the corner cases with this suite
    """
    def setUp(self):
        """
        Milestones Data Test Case scaffolding
        """
        super(MilestonesDataTestCase, self).setUp()
        self.relationship_types = api.get_milestone_relationship_types()

    def test_fetch_courses_milestones_invalid_milestone_relationship_type(self):
        """ Unit Test: test_fetch_courses_milestones_invalid_milestone_relationship_type"""
        milestone1 = api.add_milestone({
            'display_name': 'Test Milestone',
            'name': 'test_milestone',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Test Milestone Description',
        })
        api.add_course_milestone(self.test_course_key, self.relationship_types['REQUIRES'], milestone1)
        milestone2 = api.add_milestone({
            'display_name': 'Test Milestone 2',
            'name': 'test_milestone_2',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Test Milestone Description 2',
        })
        api.add_course_milestone(self.test_course_key, self.relationship_types['FULFILLS'], milestone2)
        with self.assertRaises(exceptions.InvalidMilestoneRelationshipTypeException):
            data.fetch_courses_milestones(
                [self.test_course_key, ],
                'invalid_relationshipppp',
                milestone1
            )

    def test_fetch_course_content_milestones_invalid_milestone_relationship_type(self):
        """ Unit Test: test_fetch_course_content_milestones_invalid_milestone_relationship_type"""
        milestone1 = api.add_milestone({
            'display_name': 'Test Milestone',
            'name': 'test_milestone',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Test Milestone Description',
        })
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            milestone1
        )
        milestone2 = api.add_milestone({
            'display_name': 'Test Milestone 2',
            'name': 'test_milestone2',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Test Milestone Description 2',
        })
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['FULFILLS'],
            milestone2
        )
        with self.assertRaises(exceptions.InvalidMilestoneRelationshipTypeException):
            data.fetch_course_content_milestones(
                self.test_course_key,
                self.test_content_key,
                'invalid_relationshipppp'
            )

    def test_fetch_courses_milestones_invalid_milestone(self):
        """ Unit Test: test_fetch_courses_milestones_invalid_milestone"""
        with self.assertRaises(exceptions.InvalidMilestoneException):
            data.fetch_milestones(milestone=None)
        with self.assertRaises(exceptions.InvalidMilestoneException):
            data.fetch_milestones(milestone={})

    def test_fetch_milestones_invalid_milestone_namespace(self):
        """ Unit Test: test_fetch_milestones_invalid_milestone_namespace"""
        milestones = data.fetch_milestones(milestone={'namespace': "some.namespace"})
        self.assertEqual(len(milestones), 0)

    def test_fetch_course_content_milestones_null_keys(self):
        """ Unit Test: test_fetch_course_content_milestones_null_keys"""
        namespace = '{}.entrance_exams'.format(six.text_type(self.test_course_key))
        milestone1 = api.add_milestone({
            'display_name': 'Test Milestone',
            'name': 'test_milestone',
            'namespace': namespace,
            'description': 'Test Milestone Description',
        })
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            milestone1
        )
        milestones = data.fetch_milestones(milestone={'namespace': namespace})
        self.assertEqual(len(milestones), 1)

        ccms = data.fetch_course_content_milestones(
            content_key=self.test_content_key,
            course_key=None,
            relationship=None
        )
        self.assertEqual(len(ccms), 1)

        ccms = data.fetch_course_content_milestones(
            content_key=None,
            course_key=self.test_course_key,
            relationship=None
        )
        self.assertEqual(len(ccms), 1)

    def test_fetch_milestone_courses_no_relationship_type(self):
        """ Unit Test: test_fetch_milestone_courses_no_relationship_type"""
        milestone1 = api.add_milestone({
            'display_name': 'Test Milestone',
            'name': 'test_milestone',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Test Milestone Description',
        })
        api.add_course_milestone(self.test_course_key, 'fulfills', milestone1)
        self.assertEqual(len(data.fetch_milestone_courses(milestone1)), 1)

    def test_fetch_milestone_course_content_no_relationship_type(self):
        """ Unit Test: test_fetch_milestone_course_content_no_relationship_type"""
        milestone1 = api.add_milestone({
            'display_name': 'Test Milestone',
            'name': 'test_milestone',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Test Milestone Description',
        })
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['FULFILLS'],
            milestone1
        )
        self.assertEqual(len(data.fetch_milestone_course_content(milestone1)), 1)

    def test_fetch_user_milestones_missing_match_criteria_throws_exception(self):
        """ Unit Test: test_fetch_user_milestones_missing_match_criteria_throws_exception """
        milestone1 = api.add_milestone({
            'display_name': 'Test Milestone',
            'name': 'test_milestone',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Test Milestone Description',
        })
        api.add_user_milestone(self.serialized_test_user, milestone1)

        with self.assertRaises(exceptions.InvalidMilestoneException):
            data.fetch_user_milestones(self.serialized_test_user, {})

        # Ensure we cover all remaining logical branches per coverage.py
        data.fetch_user_milestones(
            self.serialized_test_user,
            {'id': milestone1['id']}
        )

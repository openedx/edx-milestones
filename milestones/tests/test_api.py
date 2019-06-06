# -*- coding: utf-8 -*- pylint: disable=too-many-lines
# pylint: disable=invalid-name
# pylint: disable=too-many-public-methods
"""
Milestones API Module Test Cases
"""
from __future__ import absolute_import, unicode_literals

from opaque_keys.edx.keys import UsageKey

import milestones.api as api
import milestones.exceptions as exceptions
import milestones.tests.utils as utils
import six


class MilestonesApiTestCase(utils.MilestonesTestCaseMixin, utils.MilestonesTestCaseBase):
    """
    Main Test Case module for Milestones API
    """
    def setUp(self):
        """
        Milestones API Test Case scaffolding
        """
        super(MilestonesApiTestCase, self).setUp()
        self.test_milestone = api.add_milestone({
            'name': 'test_milestone',
            'display_name': 'Test Milestone',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Test Milestone Description',
        })
        self.relationship_types = api.get_milestone_relationship_types()

    def test_add_milestone(self):
        """ Unit Test: test_add_milestone"""
        with self.assertNumQueries(2):
            milestone = api.add_milestone({
                'name': 'local_milestone',
                'display_name': 'Local Milestone',
                'namespace': six.text_type(self.test_course_key),
                'description': 'Local Milestone Description'
            })
        self.assertGreater(milestone['id'], 0)

    def test_add_milestone_active_exists(self):
        """ Unit Test: test_add_milestone_active_exists"""
        milestone_data = {
            'name': 'local_milestone',
            'display_name': 'Local Milestone',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Local Milestone Description'
        }
        milestone = api.add_milestone(milestone_data)
        self.assertGreater(milestone['id'], 0)
        with self.assertNumQueries(1):
            milestone = api.add_milestone(milestone_data)

    def test_add_milestone_inactive_to_active(self):
        """ Unit Test: test_add_milestone_inactive_to_active """
        milestone_data = {
            'name': 'local_milestone',
            'display_name': 'Local Milestone',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Local Milestone Description'
        }
        milestone = api.add_milestone(milestone_data)
        self.assertGreater(milestone['id'], 0)
        api.remove_milestone(milestone['id'])

        with self.assertNumQueries(6):
            milestone = api.add_milestone(milestone_data)

    def test_add_milestone_inactive_milestone_with_relationships(self):
        """ Unit Test: test_add_milestone_inactive_milestone_with_relationships"""
        milestone_data = {
            'name': 'local_milestone',
            'display_name': 'Local Milestone',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Local Milestone Description'
        }
        milestone = api.add_milestone(milestone_data)
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            milestone
        )
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['FULFILLS'],
            milestone
        )
        api.add_user_milestone(self.serialized_test_user, milestone)
        self.assertGreater(milestone['id'], 0)
        api.remove_milestone(milestone['id'])

        with self.assertNumQueries(9):
            milestone = api.add_milestone(milestone_data)

    def test_add_milestone_inactive_milestone_with_relationships_propagate_false(self):
        """ Unit Test: test_add_milestone_inactive_milestone_with_relationships_propagate_false"""
        milestone_data = {
            'name': 'local_milestone',
            'display_name': 'Local Milestone',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Local Milestone Description'
        }
        milestone = api.add_milestone(milestone_data)
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            milestone
        )
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['FULFILLS'],
            milestone
        )
        api.add_user_milestone(self.serialized_test_user, milestone)
        self.assertGreater(milestone['id'], 0)
        api.remove_milestone(milestone['id'])

        with self.assertNumQueries(3):
            milestone = api.add_milestone(milestone_data, propagate=False)

    def test_add_milestone_invalid_data_throws_exceptions(self):
        """ Unit Test: test_add_milestone_invalid_namespaces_throw_exceptions"""
        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidMilestoneException):
                api.add_milestone({
                    'name': 'local_milestone',
                    'display_name': 'Local Milestone',
                    'namespace': '',  # Should throw an exception
                    'description': 'Local Milestone Description'
                })

        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidMilestoneException):
                api.add_milestone({
                    'name': 'Local Milestone',  # Missing namespace should throw exception
                    'description': 'Local Milestone Description'
                })

        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidMilestoneException):
                api.add_milestone({
                    'name': '',  # Empty name should throw an exception on create
                    'namespace': 'fixed',
                    'description': 'Local Milestone Description 2'
                })

        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidMilestoneException):
                api.add_milestone({
                    'namespace': 'fixed',  # Missing name should throw exception
                    'description': 'Local Milestone Description 2'
                })

    def test_edit_milestone(self):
        """ Unit Test: test_edit_milestone"""
        self.test_milestone['name'] = 'Edited Milestone'

        with self.assertNumQueries(1):
            api.edit_milestone(self.test_milestone)

    def test_edit_milestone_invalid_data_throws_exceptions(self):
        """ Unit Test: test_edit_milestone_missing_namespace """
        self.test_milestone['namespace'] = ''
        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidMilestoneException):
                api.edit_milestone(self.test_milestone)

        self.test_milestone['namespace'] = 'fixed'
        self.test_milestone['id'] = 0
        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidMilestoneException):
                api.edit_milestone(self.test_milestone)

    def test_edit_milestone_bogus_milestone(self):
        """ Unit Test: test_edit_milestone_bogus_milestone """
        self.test_milestone['id'] = 12345
        self.test_milestone['namespace'] = 'bogus.milestones'
        with self.assertNumQueries(1):
            with self.assertRaises(exceptions.InvalidMilestoneException):
                api.edit_milestone(self.test_milestone)
        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidMilestoneException):
                api.edit_milestone(None)

    def test_get_milestone(self):
        """ Unit Test: test_get_milestone"""
        with self.assertNumQueries(1):
            milestone = api.get_milestone(self.test_milestone['id'])
        self.assertEqual(milestone['name'], self.test_milestone['name'])
        self.assertEqual(milestone['namespace'], self.test_milestone['namespace'])
        self.assertEqual(milestone['description'], self.test_milestone['description'])

    def test_get_milestones(self):
        """ Unit Test: test_get_milestones """
        namespace = 'test_get_milestones'
        api.add_milestone({
            'display_name': 'Local Milestone 1',
            'name': 'local_milestone_1',
            'namespace': namespace,
            'description': 'Local Milestone 1 Description'
        })
        api.add_milestone({
            'display_name': 'Local Milestone 2',
            'name': 'local_milestone_2',
            'namespace': namespace,
            'description': 'Local Milestone 2 Description'
        })
        with self.assertNumQueries(1):
            milestones = api.get_milestones(namespace=namespace)
        self.assertEqual(len(milestones), 2)

    def test_get_milestone_invalid_milestone(self):
        """ Unit Test: test_get_milestone_invalid_milestone """
        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidMilestoneException):
                api.get_milestone(None)
        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidMilestoneException):
                api.get_milestone(0)

    def test_remove_milestone(self):
        """ Unit Test: test_remove_milestone """
        with self.assertNumQueries(5):
            api.remove_milestone(self.test_milestone['id'])
        with self.assertRaises(exceptions.InvalidMilestoneException):
            api.get_milestone(self.test_milestone['id'])

    def test_remove_milestone_bogus_milestone(self):
        """ Unit Test: test_remove_milestone_bogus_milestone """
        with self.assertNumQueries(5):
            api.remove_milestone(self.test_milestone['id'])

        with self.assertRaises(exceptions.InvalidMilestoneException):
            api.get_milestone(self.test_milestone['id'])

        # Do it again with the valid id to hit the exception workflow
        with self.assertNumQueries(4):
            api.remove_milestone(self.test_milestone['id'])

        with self.assertRaises(exceptions.InvalidMilestoneException):
            api.get_milestone(self.test_milestone['id'])

    def test_add_course_milestone(self):
        """ Unit Test: test_add_course_milestone """
        with self.assertNumQueries(3):
            api.add_course_milestone(
                self.test_course_key,
                self.relationship_types['REQUIRES'],
                self.test_milestone
            )
        requirer_milestones = api.get_course_milestones(
            self.test_course_key,
            self.relationship_types['REQUIRES']
        )
        self.assertEqual(len(requirer_milestones), 1)

        with self.assertNumQueries(3):
            api.add_course_milestone(
                self.test_prerequisite_course_key,
                self.relationship_types['FULFILLS'],
                self.test_milestone
            )
        fulfiller_milestones = api.get_course_milestones(
            self.test_prerequisite_course_key,
            self.relationship_types['FULFILLS'],
        )
        self.assertEqual(len(fulfiller_milestones), 1)

    def test_add_course_milestone_active_exists(self):
        """ Unit Test: test_add_course_milestone """
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        with self.assertNumQueries(2):
            api.add_course_milestone(
                self.test_course_key,
                self.relationship_types['REQUIRES'],
                self.test_milestone
            )

    def test_add_course_milestone_inactive_to_active(self):
        """ Unit Test: test_add_course_milestone """
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        api.remove_course_milestone(self.test_course_key, self.test_milestone)
        with self.assertNumQueries(3):
            api.add_course_milestone(
                self.test_course_key,
                self.relationship_types['REQUIRES'],
                self.test_milestone
            )

    def test_add_course_milestone_bogus_course_key(self):
        """ Unit Test: test_add_course_milestone_bogus_course_key """
        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidCourseKeyException):
                api.add_course_milestone('12345667av', 'whatever', self.test_milestone)
        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidCourseKeyException):
                api.add_course_milestone(None, 'whatever', self.test_milestone)

    def test_add_course_milestone_bogus_milestone_relationship_type(self):
        """ Unit Test: test_add_course_milestone_bogus_milestone_relationship_type """
        with self.assertNumQueries(1):
            with self.assertRaises(exceptions.InvalidMilestoneRelationshipTypeException):
                api.add_course_milestone(self.test_course_key, 'whatever', self.test_milestone)

    def test_get_course_milestones(self):
        """ Unit Test: test_get_course_milestones """
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        with self.assertNumQueries(2):
            requirer_milestones = api.get_course_milestones(
                self.test_course_key,
                self.relationship_types['REQUIRES']
            )
        self.assertEqual(len(requirer_milestones), 1)

    def test_get_course_milestones_with_invalid_relationship_type(self):
        """ Unit Test: test_get_course_milestones_with_invalid_relationship_type """
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        with self.assertNumQueries(1):
            requirer_milestones = api.get_course_milestones(
                self.test_course_key,
                'INVALID RELATIONSHIP TYPE'
            )
        self.assertEqual(len(requirer_milestones), 0)

    def test_get_course_unfulfilled_milestones(self):
        """ Unit Test: test_get_course_unfulfilled_milestones """
        namespace = 'test_get_milestones'
        milestone1 = api.add_milestone({
            'name': 'localmilestone1',
            'display_name': 'Local Milestone 1',
            'namespace': namespace,
            'description': 'Local Milestone 1 Description'
        })
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            milestone1
        )

        milestone2 = api.add_milestone({
            'name': 'localmilestone2',
            'display_name': 'Local Milestone 2',
            'namespace': namespace,
            'description': 'Local Milestone 2 Description'
        })
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            milestone2
        )

        # Confirm that the course has only two milestones, and that the User still needs to collect both
        course_milestones = api.get_course_milestones(self.test_course_key)
        self.assertEqual(len(course_milestones), 2)
        with self.assertNumQueries(2):
            required_milestones = api.get_course_required_milestones(
                self.test_course_key,
                self.serialized_test_user
            )

        # Link the User to Milestone 2 (this one is now 'collected')
        api.add_user_milestone(self.serialized_test_user, milestone2)
        user_milestones = api.get_user_milestones(self.serialized_test_user, namespace=namespace)
        self.assertEqual(len(user_milestones), 1)
        self.assertEqual(user_milestones[0]['id'], milestone2['id'])

        # Only Milestone 1 should be listed as 'required' for the course at this point
        with self.assertNumQueries(2):
            required_milestones = api.get_course_required_milestones(
                self.test_course_key,
                self.serialized_test_user
            )
        self.assertEqual(len(required_milestones), 1)
        self.assertEqual(required_milestones[0]['id'], milestone1['id'])

        # Link the User to Milestone 1 (this one is now 'collected', as well)
        api.add_user_milestone(self.serialized_test_user, milestone1)
        user_milestones = api.get_user_milestones(self.serialized_test_user, namespace=namespace)
        self.assertEqual(len(user_milestones), 2)

        # And there should be no more Milestones required for this User+Course
        with self.assertNumQueries(2):
            required_milestones = api.get_course_required_milestones(
                self.test_course_key,
                self.serialized_test_user
            )
        self.assertEqual(len(required_milestones), 0)

    def test_get_courses_milestones(self):
        """ Unit Test: test_get_courses_milestones """
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        api.add_course_milestone(
            self.test_prerequisite_course_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        local_milestone = api.add_milestone({
            'display_name': 'Local Milestone',
            'name': 'local_milestone',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Local Milestone Description'
        })
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['FULFILLS'],
            local_milestone
        )
        with self.assertNumQueries(2):
            requirer_milestones = api.get_courses_milestones(
                [self.test_course_key, self.test_prerequisite_course_key],
                self.relationship_types['REQUIRES']
            )
        self.assertEqual(len(requirer_milestones), 2)

        with self.assertNumQueries(1):
            requirer_milestones = api.get_courses_milestones(
                [self.test_course_key],
            )
        self.assertEqual(len(requirer_milestones), 2)

    def test_get_courses_milestones_with_invalid_relationship_type(self):
        """ Unit Test: test_get_courses_milestones_with_invalid_relationship_type """
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        api.add_course_milestone(
            self.test_prerequisite_course_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        local_milestone = api.add_milestone({
            'display_name': 'Local Milestone',
            'name': 'local_milestone',
            'namespace': six.text_type(self.test_course_key),
            'description': 'Local Milestone Description'
        })
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['FULFILLS'],
            local_milestone
        )

        with self.assertNumQueries(1):
            requirer_milestones = api.get_courses_milestones(
                [self.test_course_key],
                'INVALID RELATIONSHIP TYPE'
            )
        self.assertEqual(len(requirer_milestones), 0)

    def test_remove_course_milestone(self):
        """ Unit Test: test_remove_course_milestone """
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        requirer_milestones = api.get_course_milestones(
            self.test_course_key,
            self.relationship_types['REQUIRES']
        )
        self.assertEqual(len(requirer_milestones), 1)
        with self.assertNumQueries(2):
            api.remove_course_milestone(self.test_course_key, self.test_milestone)
        requirer_milestones = api.get_course_milestones(self.test_course_key)
        self.assertEqual(len(requirer_milestones), 0)

    def test_remove_course_milestone_missing_milestone(self):
        """ Unit Test: test_remove_course_milestone_missing_milestone """
        with self.assertNumQueries(1):
            api.remove_course_milestone(self.test_course_key, self.test_milestone)
        requirer_milestones = api.get_course_milestones(self.test_course_key)
        self.assertEqual(len(requirer_milestones), 0)

    def test_add_course_content_milestone(self):
        """ Unit Test: test_add_course_content_milestone """
        with self.assertNumQueries(3):
            api.add_course_content_milestone(
                self.test_course_key,
                self.test_content_key,
                self.relationship_types['REQUIRES'],
                self.test_milestone
            )
        requirer_milestones = api.get_course_content_milestones(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES']
        )
        self.assertEqual(len(requirer_milestones), 1)
        with self.assertNumQueries(3):
            api.add_course_content_milestone(
                self.test_prerequisite_course_key,
                self.test_content_key,
                self.relationship_types['FULFILLS'],
                self.test_milestone,
                {'min_score': 80}
            )
        fulfiller_milestones = api.get_course_content_milestones(
            self.test_prerequisite_course_key,
            self.test_content_key,
            self.relationship_types['FULFILLS']
        )
        self.assertEqual(len(fulfiller_milestones), 1)

    def test_add_course_content_milestone_active_exists(self):
        """ Unit Test: test_add_course_content_milestone_active_exists """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        with self.assertNumQueries(2):
            api.add_course_content_milestone(
                self.test_course_key,
                self.test_content_key,
                self.relationship_types['REQUIRES'],
                self.test_milestone
            )

    def test_add_course_content_milestone_inactive_to_active(self):
        """ Unit Test: test_add_course_content_milestone_inactive_to_active """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        api.remove_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.test_milestone
        )
        with self.assertNumQueries(3):
            api.add_course_content_milestone(
                self.test_course_key,
                self.test_content_key,
                self.relationship_types['REQUIRES'],
                self.test_milestone
            )

    def test_add_course_content_milestone_invalid_requirements(self):
        """ Unit Test: test_add_course_content_milestone_invalid_requirements """
        with self.assertRaises(exceptions.InvalidCourseContentMilestoneRequirementsException):
            api.add_course_content_milestone(
                self.test_course_key,
                self.test_content_key,
                self.relationship_types['REQUIRES'],
                self.test_milestone,
                set()  # Not JSON serializable
            )

    def test_add_course_content_milestone_active_exists_update_requirements(self):
        """ Unit Test: test_add_course_content_milestone_active_exists_update_requirement """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone,
            {'min_score': 60}
        )
        with self.assertNumQueries(3):
            api.add_course_content_milestone(
                self.test_course_key,
                self.test_content_key,
                self.relationship_types['REQUIRES'],
                self.test_milestone,
                {'min_score': 80}
            )
        milestone = api.get_course_content_milestones(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES']
        )
        for m in milestone:
            self.assertEqual(m['requirements'], {'min_score': 80})

    def test_add_course_content_milestone_inactive_to_active_update_requirements(self):
        """ Unit Test: test_add_course_content_milestone_inactive_to_active_update_requirement """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone,
            {'min_score': 60}
        )
        api.remove_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.test_milestone
        )
        with self.assertNumQueries(3):
            api.add_course_content_milestone(
                self.test_course_key,
                self.test_content_key,
                self.relationship_types['REQUIRES'],
                self.test_milestone,
                {'min_score': 80}
            )
        milestone = api.get_course_content_milestones(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES']
        )
        for m in milestone:
            self.assertEqual(m['requirements'], {'min_score': 80})

    def test_add_course_content_milestone_bogus_content_key(self):
        """ Unit Test: test_add_course_content_milestone_bogus_content_key """
        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidContentKeyException):
                api.add_course_content_milestone(
                    self.test_course_key,
                    '234290jweovsu',
                    'whatever',
                    self.test_milestone
                )
        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidContentKeyException):
                api.add_course_content_milestone(
                    self.test_course_key,
                    None,
                    'whatever',
                    self.test_milestone
                )

    def test_add_course_content_milestone_bogus_milestone_relationship_type(self):
        """ Unit Test: test_add_course_content_milestone_bogus_milestone_relationship_type """
        with self.assertNumQueries(1):
            with self.assertRaises(exceptions.InvalidMilestoneRelationshipTypeException):
                api.add_course_content_milestone(
                    self.test_course_key,
                    self.test_content_key,
                    'whatever',
                    self.test_milestone
                )
        with self.assertNumQueries(1):
            with self.assertRaises(exceptions.InvalidMilestoneRelationshipTypeException):
                api.add_course_content_milestone(
                    self.test_course_key,
                    self.test_content_key,
                    None,
                    self.test_milestone
                )

    def test_get_course_content_milestones(self):
        """ Unit Test: test_get_course_content_milestones """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        with self.assertNumQueries(2):
            requirer_milestones = api.get_course_content_milestones(
                self.test_course_key,
                self.test_content_key,
                self.relationship_types['REQUIRES']
            )
        self.assertEqual(len(requirer_milestones), 1)

    def test_get_course_content_milestones_with_unfulfilled_user_milestones(self):
        """ Unit Test: test_get_course_content_milestones_with_unfulfilled_user_milestones """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        with self.assertNumQueries(2):
            requirer_milestones = api.get_course_content_milestones(
                self.test_course_key,
                self.test_content_key,
                self.relationship_types['REQUIRES'],
                {'id': self.test_user.id}
            )
        self.assertEqual(len(requirer_milestones), 1)

    def test_get_course_content_milestones_with_fulfilled_user_milestones(self):
        """ Unit Test: test_get_course_content_milestones_with_fulfilled_user_milestones """
        user = {'id': self.test_user.id}
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        api.add_user_milestone(user, self.test_milestone)
        with self.assertNumQueries(2):
            requirer_milestones = api.get_course_content_milestones(
                self.test_course_key,
                self.test_content_key,
                self.relationship_types['REQUIRES'],
                {'id': self.test_user.id}
            )
        self.assertEqual(len(requirer_milestones), 0)

    def test_get_course_content_milestones_without_course_key(self):
        """ Unit Test: test_get_course_content_milestones_without_course_key """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        api.add_course_content_milestone(
            self.test_alternate_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        with self.assertNumQueries(2):
            requirer_milestones = api.get_course_content_milestones(
                None,
                self.test_content_key,
                self.relationship_types['REQUIRES']
            )
        self.assertEqual(len(requirer_milestones), 2)

    def test_get_course_content_milestones_without_content_key(self):
        """ Unit Test: test_get_course_content_milestones_without_content_key """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_alternate_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        with self.assertNumQueries(2):
            requirer_milestones = api.get_course_content_milestones(
                self.test_course_key,
                None,
                self.relationship_types['REQUIRES']
            )
        self.assertEqual(len(requirer_milestones), 2)

    def test_get_course_content_milestones_with_invalid_relationship(self):
        """ Unit Test: test_get_course_content_milestones_with_invalid_relationship """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_alternate_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        with self.assertNumQueries(1):
            requirer_milestones = api.get_course_content_milestones(
                self.test_course_key,
                self.test_content_key,
                'INVALID RELATIONSHIP TYPE'
            )
        self.assertEqual(len(requirer_milestones), 0)

    def test_remove_course_content_milestone(self):
        """ Unit Test: test_remove_course_content_milestone """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        requirer_milestones = api.get_course_content_milestones(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['REQUIRES']
        )
        self.assertEqual(len(requirer_milestones), 1)
        with self.assertNumQueries(2):
            api.remove_course_content_milestone(
                self.test_course_key,
                self.test_content_key,
                self.test_milestone
            )
        requirer_milestones = api.get_course_content_milestones(
            self.test_course_key,
            self.test_content_key
        )
        self.assertEqual(len(requirer_milestones), 0)

    def test_remove_course_content_milestone_missing_milestone(self):
        """ Unit Test: test_remove_course_content_milestone_missing_milestone """
        with self.assertNumQueries(1):
            api.remove_course_content_milestone(
                self.test_course_key,
                self.test_content_key,
                self.test_milestone
            )
        requirer_milestones = api.get_course_content_milestones(
            self.test_course_key,
            self.test_content_key
        )
        self.assertEqual(len(requirer_milestones), 0)

    def test_add_user_milestone(self):
        """ Unit Test: test_add_user_milestone """
        with self.assertNumQueries(2):
            api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_add_user_milestone_active_exists(self):
        """ Unit Test: test_add_user_milestone """
        api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        with self.assertNumQueries(1):
            api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_add_user_milestone_inactive_to_active(self):
        """ Unit Test: test_add_user_milestone """
        api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        api.remove_user_milestone(self.serialized_test_user, self.test_milestone)
        with self.assertNumQueries(2):
            api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_add_user_milestone_bogus_user(self):
        """ Unit Test: test_add_user_milestone_bogus_user """
        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidUserException):
                api.add_user_milestone({'identifier': 'abcd'}, self.test_milestone)
        with self.assertNumQueries(0):
            with self.assertRaises(exceptions.InvalidUserException):
                api.add_user_milestone(None, self.test_milestone)

    def test_get_user_milestones(self):
        """ Unit Test: test_get_user_milestones """
        with self.assertNumQueries(2):
            api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_remove_user_milestone(self):
        """ Unit Test: test_remove_user_milestone """
        api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))
        with self.assertNumQueries(2):
            api.remove_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertFalse(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_remove_user_milestone_missing_milestone(self):
        """ Unit Test: test_remove_user_milestone_missing_milestone """
        with self.assertNumQueries(1):
            api.remove_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertFalse(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_user_has_milestone(self):
        """ Unit Test: test_user_has_milestone """
        api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        with self.assertNumQueries(1):
            self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))
        api.remove_user_milestone(self.serialized_test_user, self.test_milestone)
        with self.assertNumQueries(1):
            self.assertFalse(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_remove_course_references(self):
        """ Unit Test: test_remove_course_references """
        # Add a course dependency on the test milestone
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        self.assertEqual(len(api.get_course_milestones(self.test_course_key)), 1)

        # Add a content fulfillment for the test milestone
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['FULFILLS'],
            self.test_milestone
        )
        self.assertEqual(
            len(api.get_course_content_milestones(self.test_course_key, self.test_content_key)), 1)

        # Remove the course dependency
        with self.assertNumQueries(4):
            api.remove_course_references(self.test_course_key)
        self.assertEqual(len(api.get_course_milestones(self.test_course_key)), 0)

    def test_remove_content_references(self):
        """ Unit Test: test_remove_content_references """
        # Add a course dependency on the test milestone
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            self.test_milestone
        )
        self.assertEqual(len(api.get_course_milestones(self.test_course_key)), 1)

        # Add a content fulfillment for the test milestone
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            self.relationship_types['FULFILLS'],
            self.test_milestone
        )
        milestones = api.get_course_content_milestones(self.test_course_key, self.test_content_key)
        self.assertEqual(len(milestones), 1)

        # Remove the content dependency
        with self.assertNumQueries(2):
            api.remove_content_references(self.test_content_key)
        milestones = api.get_course_content_milestones(self.test_course_key, self.test_content_key)
        self.assertEqual(len(milestones), 0)

    def test_milestones_fulfillment_paths_contains_special_characters(self):
        """
        Unit Test: test_get_course_milestones_fulfillment_paths works correctly when milestone have some special
        characters.
        """
        namespace = six.text_type(self.test_course_key)
        name = '�ťÉśt_Àübùr�'
        local_milestone_1 = api.add_milestone({
            'display_name': 'Local Milestone 1',
            'name': name,
            'namespace': namespace,
            'description': 'Local Milestone 1 Description'
        })

        # Specify the milestone requirements
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            local_milestone_1
        )

        # Specify the milestone fulfillments (via course and content)
        api.add_course_milestone(
            self.test_prerequisite_course_key,
            self.relationship_types['FULFILLS'],
            local_milestone_1
        )
        with self.assertNumQueries(4):
            paths = api.get_course_milestones_fulfillment_paths(
                self.test_course_key,
                self.serialized_test_user
            )

        # Set up the key values we'll use to access/assert the response
        milestone_key_1 = '{}.{}'.format(local_milestone_1['namespace'], local_milestone_1['name'])
        self.assertEqual(len(paths[milestone_key_1]['courses']), 1)

    def test_get_course_milestones_fulfillment_paths(self):  # pylint: disable=too-many-statements
        """
        Unit Test: test_get_course_milestones_fulfillment_paths
        """
        # Create three milestones in order tto cover all logical branches
        namespace = six.text_type(self.test_course_key)
        local_milestone_1 = api.add_milestone({
            'display_name': 'Local Milestone 1',
            'name': 'local_milestone_1',
            'namespace': namespace,
            'description': 'Local Milestone 1 Description'
        })
        local_milestone_2 = api.add_milestone({
            'display_name': 'Local Milestone 2',
            'name': 'local_milestone_2',
            'namespace': namespace,
            'description': 'Local Milestone 2 Description'
        })
        local_milestone_3 = api.add_milestone({
            'display_name': 'Local Milestone 3',
            'name': 'local_milestone_3',
            'namespace': namespace,
            'description': 'Local Milestone 3 Description'
        })

        # Specify the milestone requirements
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            local_milestone_1
        )
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            local_milestone_2
        )
        api.add_course_milestone(
            self.test_course_key,
            self.relationship_types['REQUIRES'],
            local_milestone_3
        )

        # Specify the milestone fulfillments (via course and content)
        api.add_course_milestone(
            self.test_prerequisite_course_key,
            self.relationship_types['FULFILLS'],
            local_milestone_1
        )
        api.add_course_milestone(
            self.test_prerequisite_course_key,
            self.relationship_types['FULFILLS'],
            local_milestone_2
        )
        api.add_course_content_milestone(
            self.test_course_key,
            UsageKey.from_string('i4x://the/content/key/123456789'),
            self.relationship_types['FULFILLS'],
            local_milestone_2
        )
        api.add_course_content_milestone(
            self.test_course_key,
            UsageKey.from_string('i4x://the/content/key/123456789'),
            self.relationship_types['FULFILLS'],
            local_milestone_3
        )
        api.add_course_content_milestone(
            self.test_course_key,
            UsageKey.from_string('i4x://the/content/key/987654321'),
            self.relationship_types['FULFILLS'],
            local_milestone_3
        )

        # Confirm the starting state for this test (user has no milestones, course requires three)
        self.assertEqual(
            len(api.get_user_milestones(self.serialized_test_user, namespace=namespace)), 0)
        self.assertEqual(
            len(api.get_course_required_milestones(self.test_course_key, self.serialized_test_user)),
            3
        )
        # Check the possible fulfillment paths for the milestones for this course
        with self.assertNumQueries(8):
            paths = api.get_course_milestones_fulfillment_paths(
                self.test_course_key,
                self.serialized_test_user
            )

        # Set up the key values we'll use to access/assert the response
        milestone_key_1 = '{}.{}'.format(local_milestone_1['namespace'], local_milestone_1['name'])
        milestone_key_2 = '{}.{}'.format(local_milestone_2['namespace'], local_milestone_2['name'])
        milestone_key_3 = '{}.{}'.format(local_milestone_3['namespace'], local_milestone_3['name'])

        # First round of assertions
        self.assertEqual(len(paths[milestone_key_1]['courses']), 1)
        self.assertIsNone(paths[milestone_key_1].get('content'))
        self.assertEqual(len(paths[milestone_key_2]['courses']), 1)
        self.assertEqual(len(paths[milestone_key_2]['content']), 1)
        self.assertIsNone(paths[milestone_key_3].get('courses'))
        self.assertEqual(len(paths[milestone_key_3]['content']), 2)

        # Collect the first milestone (two should remain)
        api.add_user_milestone(self.serialized_test_user, local_milestone_1)
        self.assertEqual(
            len(api.get_user_milestones(self.serialized_test_user, namespace=namespace)), 1)
        self.assertEqual(
            len(api.get_course_required_milestones(self.test_course_key, self.serialized_test_user)),
            2
        )
        # Check the remaining fulfillment paths for the milestones for this course
        with self.assertNumQueries(6):
            paths = api.get_course_milestones_fulfillment_paths(
                self.test_course_key,
                self.serialized_test_user
            )
        self.assertIsNone(paths.get(milestone_key_1))
        self.assertEqual(len(paths[milestone_key_2]['courses']), 1)
        self.assertEqual(len(paths[milestone_key_2]['content']), 1)
        self.assertIsNone(paths[milestone_key_3].get('courses'))
        self.assertEqual(len(paths[milestone_key_3]['content']), 2)

        # Collect the second milestone (one should remain)
        api.add_user_milestone(self.serialized_test_user, local_milestone_2)
        self.assertEqual(
            len(api.get_user_milestones(self.serialized_test_user, namespace=namespace)), 2)
        self.assertEqual(
            len(api.get_course_required_milestones(self.test_course_key, self.serialized_test_user)),
            1
        )
        # Check the remaining fulfillment paths for the milestones for this course
        with self.assertNumQueries(4):
            paths = api.get_course_milestones_fulfillment_paths(
                self.test_course_key,
                self.serialized_test_user
            )
        self.assertIsNone(paths.get(milestone_key_1))
        self.assertIsNone(paths.get(milestone_key_2))
        self.assertIsNone(paths[milestone_key_3].get('courses'))
        self.assertEqual(len(paths[milestone_key_3]['content']), 2)

        # Collect the third milestone
        api.add_user_milestone(self.serialized_test_user, local_milestone_3)
        self.assertEqual(
            len(api.get_user_milestones(self.serialized_test_user, namespace=namespace)), 3)
        self.assertEqual(
            len(api.get_course_required_milestones(self.test_course_key, self.serialized_test_user)),
            0
        )
        # Check the remaining fulfillment paths for the milestones for this course
        with self.assertNumQueries(2):
            paths = api.get_course_milestones_fulfillment_paths(
                self.test_course_key,
                self.serialized_test_user
            )
        self.assertIsNone(paths.get(milestone_key_1))
        self.assertIsNone(paths.get(milestone_key_2))
        self.assertIsNone(paths.get(milestone_key_3))

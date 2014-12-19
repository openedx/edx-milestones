# pylint: disable=invalid-name
# pylint: disable=too-many-public-methods
"""
Milestones API Module Test Cases
"""
from django.contrib.auth.models import User
from django.test import TestCase

from opaque_keys.edx.keys import CourseKey, UsageKey

import milestones.api as api
import milestones.exceptions as exceptions


class MilestonesApiTestCase(TestCase):
    """
    Main Test Case module for Milestones API
    """
    def setUp(self):
        """
        Milestones API Test Case scaffolding
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
        self.test_milestone = api.add_milestone({
            'name': 'Test Milestone',
            'namespace': unicode(self.test_course_key),
            'description': 'Test Milestone Description',
        })

    def test_add_milestone(self):
        """ Unit Test: test_add_milestone"""
        milestone = api.add_milestone({
            'name': 'Local Milestone',
            'namespace': unicode(self.test_course_key),
            'description': 'Local Milestone Description'
        })
        self.assertGreater(milestone['id'], 0)

    def test_add_milestone_invalid_namespaces_throw_exceptions(self):
        """ Unit Test: test_add_milestone_invalid_namespaces_throw_exceptions"""
        try:
            api.add_milestone({
                'name': 'Local Milestone',
                'namespace': '',  # Should throw an exception
                'description': 'Local Milestone Description'
            })
            self.fail('Empty Milestone Namespace: Expected InvalidMilestoneException')  # pragma: no cover
        except exceptions.InvalidMilestoneException:
            pass

        try:
            api.add_milestone({
                'name': 'Local Milestone',  # Missing namespace should throw exception
                'description': 'Local Milestone Description'
            })
            self.fail('Missing Milestone Namespace: Expected InvalidMilestoneException')  # pragma: no cover
        except exceptions.InvalidMilestoneException:
            pass

    def test_edit_milestone(self):
        """ Unit Test: test_edit_milestone"""
        self.test_milestone['name'] = 'Edited Milestone'
        api.edit_milestone(self.test_milestone)

    def test_edit_milestone_missing_namespace(self):
        """ Unit Test """
        self.test_milestone['namespace'] = ''
        try:
            api.edit_milestone(self.test_milestone)
            self.fail('Empty Milestone Namespace: Expected InvalidMilestoneException')  # pragma: no cover
        except exceptions.InvalidMilestoneException:
            pass

    def test_edit_milestone_bogus_milestone(self):
        """ Unit Test """
        self.test_milestone['id'] = 12345
        self.test_milestone['namespace'] = 'bogus.milestones'
        try:
            api.edit_milestone(self.test_milestone)
            self.fail('Milestone Not Found: Expected InvalidMilestoneException')  # pragma: no cover
        except exceptions.InvalidMilestoneException:
            pass
        try:
            api.edit_milestone(None)
            self.fail('Milestone Not Found: Expected InvalidMilestoneException')  # pragma: no cover
        except exceptions.InvalidMilestoneException:
            pass

    def test_get_milestone(self):
        """ Unit Test: test_get_milestone"""
        milestone = api.get_milestone(self.test_milestone['id'])
        self.assertEqual(milestone['name'], self.test_milestone['name'])
        self.assertEqual(milestone['namespace'], self.test_milestone['namespace'])
        self.assertEqual(milestone['description'], self.test_milestone['description'])

    def test_get_milestones(self):
        """ Unit Test: test_get_milestones """
        namespace = 'test_get_milestones'
        api.add_milestone({
            'name': 'Local Milestone 1',
            'namespace': namespace,
            'description': 'Local Milestone 1 Description'
        })
        api.add_milestone({
            'name': 'Local Milestone 2',
            'namespace': namespace,
            'description': 'Local Milestone 2 Description'
        })
        milestones = api.get_milestones(namespace=namespace)
        self.assertEqual(len(milestones), 2)

    def test_remove_milestone(self):
        """ Unit Test: test_remove_milestone """
        api.remove_milestone(self.test_milestone['id'])
        milestone = api.get_milestone(self.test_milestone['id'])
        self.assertIsNone(milestone)

    def test_remove_milestone_bogus_milestone(self):
        """ Unit Test: test_remove_milestone_bogus_milestone """
        api.remove_milestone(self.test_milestone['id'])
        milestone = api.get_milestone(self.test_milestone['id'])
        self.assertIsNone(milestone)
        api.remove_milestone(self.test_milestone['id'])
        milestone = api.get_milestone(self.test_milestone['id'])
        self.assertIsNone(milestone)

    def test_add_course_milestone(self):
        """ Unit Test: test_add_course_milestone """
        api.add_course_milestone(self.test_course_key, 'requires', self.test_milestone)
        requirer_milestones = api.get_course_milestones(self.test_course_key, 'requires')
        self.assertEqual(len(requirer_milestones), 1)

        api.add_course_milestone(
            self.test_prerequisite_course_key,
            'fulfills',
            self.test_milestone
        )
        fulfiller_milestones = api.get_course_milestones(
            self.test_prerequisite_course_key,
            'fulfills'
        )
        self.assertEqual(len(fulfiller_milestones), 1)

    def test_add_course_milestone_bogus_course_key(self):
        """ Unit Test: test_add_course_milestone_bogus_course_key """
        try:
            api.add_course_milestone('12345667av', 'whatever', self.test_milestone)
            self.fail('Expected InvalidCourseKeyException')  # pragma: no cover
        except exceptions.InvalidCourseKeyException:
            pass
        try:
            api.add_course_milestone(None, 'whatever', self.test_milestone)
            self.fail('Expected InvalidCourseKeyException')  # pragma: no cover
        except exceptions.InvalidCourseKeyException:
            pass

    def test_add_course_milestone_bogus_milestone_relationship_type(self):
        """ Unit Test: test_add_course_milestone_bogus_milestone_relationship_type """
        try:
            api.add_course_milestone(self.test_course_key, 'whatever', self.test_milestone)
            self.fail('Expected InvalidMilestoneRelationshipTypeException')  # pragma: no cover
        except exceptions.InvalidMilestoneRelationshipTypeException:
            pass

    def test_get_course_milestones(self):
        """ Unit Test: test_get_course_milestones """
        api.add_course_milestone(self.test_course_key, 'requires', self.test_milestone)
        requirer_milestones = api.get_course_milestones(self.test_course_key, 'requires')
        self.assertEqual(len(requirer_milestones), 1)

    def test_get_course_unfulfilled_milestones(self):
        """ Unit Test: test_get_course_unfulfilled_milestones """
        namespace = 'test_get_milestones'
        milestone1 = api.add_milestone({
            'name': 'Local Milestone 1',
            'namespace': namespace,
            'description': 'Local Milestone 1 Description'
        })
        api.add_course_milestone(self.test_course_key, 'requires', milestone1)

        milestone2 = api.add_milestone({
            'name': 'Local Milestone 2',
            'namespace': namespace,
            'description': 'Local Milestone 2 Description'
        })
        api.add_course_milestone(self.test_course_key, 'requires', milestone2)

        # Confirm that the course has only two milestones, and that the User still needs to collect both
        course_milestones = api.get_course_milestones(self.test_course_key)
        self.assertEqual(len(course_milestones), 2)
        required_milestones = api.get_course_required_milestones(
            self.test_course_key,
            self.serialized_test_user
        )

        # Link the User to Milestone 2 (this one is now 'collected')
        api.add_user_milestone(self.serialized_test_user, milestone2)
        user_milestones = api.get_user_milestones(self.serialized_test_user)
        self.assertEqual(len(user_milestones), 1)
        self.assertEqual(user_milestones[0]['id'], milestone2['id'])

        # Only Milestone 1 should be listed as 'required' for the course at this point
        required_milestones = api.get_course_required_milestones(
            self.test_course_key,
            self.serialized_test_user
        )
        self.assertEqual(len(required_milestones), 1)
        self.assertEqual(required_milestones[0]['id'], milestone1['id'])

        # Link the User to Milestone 1 (this one is now 'collected', as well)
        api.add_user_milestone(self.serialized_test_user, milestone1)
        user_milestones = api.get_user_milestones(self.serialized_test_user)
        self.assertEqual(len(user_milestones), 2)

        # And there should be no more Milestones required for this User+Course
        required_milestones = api.get_course_required_milestones(
            self.test_course_key,
            self.serialized_test_user
        )
        self.assertEqual(len(required_milestones), 0)

    def test_get_courses_milestones(self):
        """ Unit Test: test_get_courses_milestones """
        api.add_course_milestone(
            self.test_course_key,
            'requires',
            self.test_milestone
        )
        api.add_course_milestone(
            self.test_prerequisite_course_key,
            'requires',
            self.test_milestone
        )
        local_milestone = api.add_milestone({
            'name': 'Local Milestone',
            'namespace': unicode(self.test_course_key),
            'description': 'Local Milestone Description'
        })
        api.add_course_milestone(
            self.test_course_key,
            'fulfills',
            local_milestone
        )
        requirer_milestones = api.get_courses_milestones(
            [self.test_course_key, self.test_prerequisite_course_key],
            'requires'
        )
        self.assertEqual(len(requirer_milestones), 2)

        requirer_milestones = api.get_courses_milestones(
            [self.test_course_key],
        )
        self.assertEqual(len(requirer_milestones), 2)

    def test_remove_course_milestone(self):
        """ Unit Test: test_remove_course_milestone """
        api.add_course_milestone(self.test_course_key, 'requires', self.test_milestone)
        requirer_milestones = api.get_course_milestones(self.test_course_key, 'requires')
        self.assertEqual(len(requirer_milestones), 1)
        api.remove_course_milestone(self.test_course_key, self.test_milestone)
        requirer_milestones = api.get_course_milestones(self.test_course_key)
        self.assertEqual(len(requirer_milestones), 0)

    def test_remove_course_milestone_missing_milestone(self):
        """ Unit Test: test_remove_course_milestone_missing_milestone """
        api.remove_course_milestone(self.test_course_key, self.test_milestone)
        requirer_milestones = api.get_course_milestones(self.test_course_key)
        self.assertEqual(len(requirer_milestones), 0)

    def test_add_course_content_milestone(self):
        """ Unit Test: test_add_course_content_milestone """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            'requires',
            self.test_milestone
        )
        requirer_milestones = api.get_course_content_milestones(
            self.test_course_key,
            self.test_content_key,
            'requires'
        )
        self.assertEqual(len(requirer_milestones), 1)

        api.add_course_content_milestone(
            self.test_prerequisite_course_key,
            self.test_content_key,
            'fulfills',
            self.test_milestone
        )
        fulfiller_milestones = api.get_course_content_milestones(
            self.test_prerequisite_course_key,
            self.test_content_key,
            'fulfills'
        )
        self.assertEqual(len(fulfiller_milestones), 1)

    def test_add_course_content_milestone_bogus_content_key(self):
        """ Unit Test """
        try:
            api.add_course_content_milestone(
                self.test_course_key,
                '234290jweovsu',
                'whatever',
                self.test_milestone
            )
            self.fail('Expected InvalidContentKeyException')  # pragma: no cover
        except exceptions.InvalidContentKeyException:
            pass
        try:
            api.add_course_content_milestone(
                self.test_course_key,
                None,
                'whatever',
                self.test_milestone
            )
            self.fail('Expected InvalidContentKeyException')  # pragma: no cover
        except exceptions.InvalidContentKeyException:
            pass

    def test_add_course_content_milestone_bogus_milestone_relationship_type(self):
        """ Unit Test: test_add_course_content_milestone_bogus_milestone_relationship_type """
        try:
            api.add_course_content_milestone(
                self.test_course_key,
                self.test_content_key,
                'whatever',
                self.test_milestone
            )
            self.fail('Expected InvalidMilestoneRelationshipTypeException')  # pragma: no cover
        except exceptions.InvalidMilestoneRelationshipTypeException:
            pass
        try:
            api.add_course_content_milestone(
                self.test_course_key,
                self.test_content_key,
                None,
                self.test_milestone
            )
            self.fail('Expected InvalidMilestoneRelationshipTypeException')  # pragma: no cover
        except exceptions.InvalidMilestoneRelationshipTypeException:
            pass


    def test_get_course_content_milestones(self):
        """ Unit Test: test_get_course_content_milestones """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            'requires',
            self.test_milestone
        )
        requirer_milestones = api.get_course_content_milestones(
            self.test_course_key,
            self.test_content_key,
            'requires'
        )
        self.assertEqual(len(requirer_milestones), 1)

    def test_remove_course_content_milestone(self):
        """ Unit Test: test_remove_course_content_milestone """
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            'requires',
            self.test_milestone
        )
        requirer_milestones = api.get_course_content_milestones(
            self.test_course_key,
            self.test_content_key,
            'requires'
        )
        self.assertEqual(len(requirer_milestones), 1)
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
        api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_add_user_milestone_bogus_user(self):
        """ Unit Test: test_add_user_milestone_bogus_user """
        try:
            api.add_user_milestone({'identifier': 'abcd'}, self.test_milestone)
            self.fail('Expected InvalidUserException')  # pragma: no cover
        except exceptions.InvalidUserException:
            pass
        try:
            api.add_user_milestone(None, self.test_milestone)
            self.fail('Expected InvalidUserException')  # pragma: no cover
        except exceptions.InvalidUserException:
            pass

    def test_get_user_milestones(self):
        """ Unit Test: test_get_user_milestones """
        api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_remove_user_milestone(self):
        """ Unit Test """
        api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))
        api.remove_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertFalse(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_remove_user_milestone_missing_milestone(self):
        """ Unit Test """
        api.remove_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertFalse(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_user_has_milestone(self):
        """ Unit Test """
        api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))
        api.remove_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertFalse(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_remove_course_references(self):
        """ Unit Test """
        api.add_course_milestone(self.test_course_key, 'requires', self.test_milestone)
        self.assertEqual(len(api.get_course_milestones(self.test_course_key)), 1)
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            'fulfills',
            self.test_milestone
        )
        self.assertEqual(
            len(api.get_course_content_milestones(self.test_course_key, self.test_content_key)), 1)
        api.remove_course_references(self.test_course_key)
        self.assertEqual(len(api.get_course_milestones(self.test_course_key)), 0)
        self.assertEqual(
            len(api.get_course_content_milestones(self.test_course_key, self.test_content_key)), 0)

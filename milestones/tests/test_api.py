from django.contrib.auth.models import User
from django.test import TestCase

from opaque_keys.edx.keys import CourseKey, UsageKey

from milestones import api, exceptions

class MilestonesApiTestCase(TestCase):

    def setUp(self):
        self.test_course_key = CourseKey.from_string('the/course/key')
        self.test_prerequisite_course_key = CourseKey.from_string('the/prerequisite/key')
        self.test_content_key = UsageKey.from_string('i4x://the/content/key/12345678')
        self.test_user = User.objects.create(first_name='Test', last_name='User', email='test_user@edx.org', username='test_user', password='ABcd12!@')
        self.serialized_test_user = self.test_user.__dict__
        self.test_milestone = api.add_milestone({
            'name': 'Test Milestone',
            'namespace': unicode(self.test_course_key),
            'description': 'Test Milestone Description',
        })

    def test_add_milestone(self):
        milestone = api.add_milestone({
            'name': 'Local Milestone',
            'namespace': unicode(self.test_course_key),
            'description': 'Local Milestone Description'
        })
        self.assertGreater(milestone['id'], 0)

    def test_add_milestone_missing_namespace(self):
        try:
            milestone = api.add_milestone({
                'name': 'Local Milestone',
                'description': 'Local Milestone Description'
            })
            self.fail('Expected InvalidMilestoneException')
        except exceptions.InvalidMilestoneException:
            pass

    def test_edit_milestone(self):
        self.test_milestone['name'] = 'Edited Milestone'
        edited_milestone = api.edit_milestone(self.test_milestone)

    def test_edit_milestone_missing_namespace(self):
        self.test_milestone['namespace'] = ''
        try:
            edited_milestone = api.edit_milestone(self.test_milestone)
            self.fail('Expected InvalidMilestoneException')
        except exceptions.InvalidMilestoneException:
            pass

    def test_get_milestone(self):
        milestone = api.get_milestone(self.test_milestone['id'])
        self.assertEqual(milestone['name'], self.test_milestone['name'])
        self.assertEqual(milestone['namespace'], self.test_milestone['namespace'])
        self.assertEqual(milestone['description'], self.test_milestone['description'])

    def test_get_milestones(self):
        milestone1 = api.add_milestone({
            'name': 'Local Milestone 1',
            'namespace': 'test_get_milestones',
            'description': 'Local Milestone 1 Description'
        })
        milestone2 = api.add_milestone({
            'name': 'Local Milestone 2',
            'namespace': 'test_get_milestones',
            'description': 'Local Milestone 2 Description'
        })
        milestones = api.get_milestones

    def test_remove_milestone(self):
        api.remove_milestone(self.test_milestone['id'])
        milestone = api.get_milestone(self.test_milestone['id'])
        self.assertIsNone(milestone)

    def test_add_course_milestone(self):
        requirer = api.add_course_milestone(self.test_course_key, 'requires', self.test_milestone)
        requirer_milestones = api.get_course_milestones(self.test_course_key, 'requires')
        self.assertEqual(len(requirer_milestones), 1)

        fulfiller = api.add_course_milestone(self.test_prerequisite_course_key, 'fulfills', self.test_milestone)
        fulfiller_milestones = api.get_course_milestones(self.test_prerequisite_course_key, 'fulfills')
        self.assertEqual(len(fulfiller_milestones), 1)

    def test_add_course_milestone_bogus_milestone_relationship_type(self):
        try:
            api.add_course_milestone(self.test_course_key, 'whatever', self.test_milestone)
            self.fail('Expected InvalidMilestoneRelationshipTypeException')
        except exceptions.InvalidMilestoneRelationshipTypeException:
            pass

    def test_get_course_milestones(self):
        requirer = api.add_course_milestone(self.test_course_key, 'requires', self.test_milestone)
        requirer_milestones = api.get_course_milestones(self.test_course_key, 'requires')
        self.assertEqual(len(requirer_milestones), 1)

    def test_get_courses_milestones(self):
        requirer = api.add_course_milestone(self.test_course_key, 'requires', self.test_milestone)
        requirer = api.add_course_milestone(self.test_prerequisite_course_key, 'requires', self.test_milestone)
        requirer_milestones = api.get_courses_milestones([self.test_course_key, self.test_prerequisite_course_key],
                                                         'requires')
        self.assertEqual(len(requirer_milestones), 2)

    def test_remove_course_milestone(self):
        requirer = api.add_course_milestone(self.test_course_key, 'requires', self.test_milestone)
        requirer_milestones = api.get_course_milestones(self.test_course_key, 'requires')
        self.assertEqual(len(requirer_milestones), 1)
        api.remove_course_milestone(self.test_course_key, self.test_milestone)
        requirer_milestones = api.get_course_milestones(self.test_course_key)
        self.assertEqual(len(requirer_milestones), 0)

    def test_remove_course_milestone_missing_milestone(self):
        api.remove_course_milestone(self.test_course_key, self.test_milestone)
        requirer_milestones = api.get_course_milestones(self.test_course_key)
        self.assertEqual(len(requirer_milestones), 0)

    def test_add_course_content_milestone(self):
        requirer = api.add_course_content_milestone(self.test_course_key, self.test_content_key, 'requires', self.test_milestone)
        requirer_milestones = api.get_course_content_milestones(self.test_course_key, self.test_content_key, 'requires')
        self.assertEqual(len(requirer_milestones), 1)

        fulfiller = api.add_course_content_milestone(self.test_prerequisite_course_key, self.test_content_key, 'fulfills', self.test_milestone)
        fulfiller_milestones = api.get_course_content_milestones(self.test_prerequisite_course_key, self.test_content_key, 'fulfills')
        self.assertEqual(len(fulfiller_milestones), 1)

    def test_add_course_content_milestone_bogus_milestone_relationship_type(self):
        try:
            api.add_course_content_milestone(self.test_course_key, self.test_content_key, 'whatever', self.test_milestone)
            self.fail('Expected InvalidMilestoneRelationshipTypeException')
        except exceptions.InvalidMilestoneRelationshipTypeException:
            pass

    def test_get_course_content_milestones(self):
        requirer = api.add_course_content_milestone(self.test_course_key, self.test_content_key, 'requires', self.test_milestone)
        requirer_milestones = api.get_course_content_milestones(self.test_course_key, self.test_content_key, 'requires')
        self.assertEqual(len(requirer_milestones), 1)

    def test_remove_course_content_milestone(self):
        requirer = api.add_course_content_milestone(self.test_course_key, self.test_content_key, 'requires', self.test_milestone)
        requirer_milestones = api.get_course_content_milestones(self.test_course_key, self.test_content_key, 'requires')
        self.assertEqual(len(requirer_milestones), 1)
        api.remove_course_content_milestone(self.test_course_key, self.test_content_key, self.test_milestone)
        requirer_milestones = api.get_course_content_milestones(self.test_course_key, self.test_content_key)
        self.assertEqual(len(requirer_milestones), 0)

    def test_remove_course_content_milestone_missing_milestone(self):
        api.remove_course_content_milestone(self.test_course_key, self.test_content_key, self.test_milestone)
        requirer_milestones = api.get_course_content_milestones(self.test_course_key, self.test_content_key)
        self.assertEqual(len(requirer_milestones), 0)

    def test_add_user_milestone(self):
        api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_get_user_milestones(self):
        api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_remove_user_milestone(self):
        user_milestone = api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))
        api.remove_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertFalse(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_remove_user_milestone_missing_milestone(self):
        api.remove_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertFalse(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_user_has_milestone(self):
        user_milestone = api.add_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertTrue(api.user_has_milestone(self.serialized_test_user, self.test_milestone))
        api.remove_user_milestone(self.serialized_test_user, self.test_milestone)
        self.assertFalse(api.user_has_milestone(self.serialized_test_user, self.test_milestone))

    def test_remove_course_references(self):
        api.add_course_milestone(self.test_course_key, 'requires', self.test_milestone)
        self.assertEqual(len(api.get_course_milestones(self.test_course_key)), 1)
        api.add_course_content_milestone(self.test_course_key, self.test_content_key, 'fulfills', self.test_milestone)
        self.assertEqual(len(api.get_course_content_milestones(self.test_course_key, self.test_content_key)), 1)
        api.remove_course_references(self.test_course_key)
        self.assertEqual(len(api.get_course_milestones(self.test_course_key)), 0)
        self.assertEqual(len(api.get_course_content_milestones(self.test_course_key, self.test_content_key)), 0)

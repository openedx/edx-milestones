# pylint: disable=invalid-name
# pylint: disable=too-many-public-methods
"""
Milestones Data Module Test Cases
"""
import milestones.api as api
import milestones.data as data
import milestones.exceptions as exceptions
import milestones.tests.utils as utils


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

    def test_fetch_courses_milestones_invalid_milestone_relationship_type(self):
        """ Unit Test: test_fetch_courses_milestones_invalid_milestone_relationship_type"""
        milestone1 = api.add_milestone({
            'name': 'Test Milestone',
            'namespace': unicode(self.test_course_key),
            'description': 'Test Milestone Description',
        })
        api.add_course_milestone(self.test_course_key, 'requires', milestone1)
        milestone2 = api.add_milestone({
            'name': 'Test Milestone 2',
            'namespace': unicode(self.test_course_key),
            'description': 'Test Milestone Description 2',
        })
        api.add_course_milestone(self.test_course_key, 'fulfills', milestone2)
        try:
            data.fetch_courses_milestones(
                [self.test_course_key, ],
                'invalid_relationshipppp',
                milestone1
            )
            self.fail('Expected InvalidMilestoneRelationshipTypeException')  # pragma: no cover
        except exceptions.InvalidMilestoneRelationshipTypeException:
            pass

    def test_fetch_course_content_milestones_invalid_milestone_relationship_type(self):
        """ Unit Test: test_fetch_courses_milestones_invalid_milestone_relationship_type"""
        milestone1 = api.add_milestone({
            'name': 'Test Milestone',
            'namespace': unicode(self.test_course_key),
            'description': 'Test Milestone Description',
        })
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            'requires',
            milestone1
        )
        milestone2 = api.add_milestone({
            'name': 'Test Milestone 2',
            'namespace': unicode(self.test_course_key),
            'description': 'Test Milestone Description 2',
        })
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            'fulfills',
            milestone2
        )
        try:
            data.fetch_course_content_milestones(
                self.test_course_key,
                self.test_content_key,
                'invalid_relationshipppp'
            )
            self.fail('Expected InvalidMilestoneRelationshipTypeException')  # pragma: no cover
        except exceptions.InvalidMilestoneRelationshipTypeException:
            pass

    def test_fetch_courses_milestones_invalid_milestone(self):
        """ Unit Test: test_fetch_courses_milestones_invalid_milestone"""
        try:
            data.fetch_milestones(milestone=None)
            self.fail('Expected InvalidMilestoneException')  # pragma: no cover
        except exceptions.InvalidMilestoneException:
            pass

    def test_fetch_milestones_invalid_milestone_namespace(self):
        """ Unit Test: test_fetch_courses_milestones_invalid_milestone"""
        milestones = data.fetch_milestones(milestone={'namespace': "some.namespace"})
        self.assertEqual(len(milestones), 0)

        milestones = data.fetch_milestones(milestone={})
        self.assertEqual(len(milestones), 0)

    def test_fetch_course_content_milestones_null_keys(self):
        """ Unit Test: test_fetch_courses_milestones_invalid_milestone"""
        namespace = '{}.entrance_exams'.format(unicode(self.test_course_key))
        milestone1 = api.add_milestone({
            'name': 'Test Milestone',
            'namespace': namespace,
            'description': 'Test Milestone Description',
        })
        api.add_course_content_milestone(
            self.test_course_key,
            self.test_content_key,
            'requires',
            milestone1
        )
        milestones = data.fetch_milestones(milestone={'namespace': namespace})
        self.assertEqual(len(milestones), 1)

        ccms = data.fetch_course_content_milestones(None, self.test_content_key, relationship=None)
        self.assertEqual(len(ccms), 1)

        ccms = data.fetch_course_content_milestones(self.test_course_key, None, relationship=None)
        self.assertEqual(len(ccms), 1)

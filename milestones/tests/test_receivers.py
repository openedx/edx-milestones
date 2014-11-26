from django.conf import settings
from django.test import TestCase

from opaque_keys.edx.keys import CourseKey

from mocks.signals import course_deleted, course_prerequisite_course_added
from milestones import api


class ReceiverTestCase(TestCase):

    def setUp(self):
        truth = True

    def test_on_course_prequisite_course_added(self):
        course_key = CourseKey.from_string('the/course/key')
        prerequisite_course_key = CourseKey.from_string('prerequisite/course/key')
        course_prerequisite_course_added.send(
            sender=self,
            course_key=course_key,
            prerequisite_course_key=prerequisite_course_key,
        )

        # Confirm that the prerequisite course fulfills its generic milestone
        # The namespace for generic course milestones is the course identifier
        prereq_milestones = api.get_course_milestones(course_key=prerequisite_course_key, type='fulfills')
        self.assertEqual(unicode(prerequisite_course_key), prereq_milestones[0]['namespace'])

        # Confirm that the main course requires the prerequisite course's generic milestone
        course_milestones = api.get_course_milestones(course_key=course_key, type='requires')
        self.assertEqual(unicode(prerequisite_course_key), course_milestones[0]['namespace'])


    # def test_on_course_deleted(self):
    #     course_deleted.send(
    #         sender=self,
    #         course_key='foo/bar/baz',
    #     )

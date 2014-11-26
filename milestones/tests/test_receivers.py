from django.conf import settings
from django.dispatch import receiver
from django.test import TestCase

from opaque_keys.edx.keys import CourseKey

from milestones import api
from milestones.signals import course_milestone_added

from mocks.signals import course_deleted, course_prerequisite_course_added

class ReceiverTestCase(TestCase):

    def setUp(self):
        truth = True

    def test_on_course_prequisite_course_added(self):
        self.signal_broadcasts = []

        # Define and connect the local signal listener before doing anything
        @receiver(course_milestone_added)
        def signal_listener(sender, signal, course_key, milestone, milestone_relationship_type):
            self.signal_broadcasts.append(
                {
                    'course_key': course_key,
                    'milestone': milestone,
                    'milestone_relationship_type': milestone_relationship_type
                }
            )

        # Broaccast the event to the application
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

        # Confirm the workflow events were properly emitted
        self.assertEqual(len(self.signal_broadcasts), 2)
        self.assertEqual(self.signal_broadcasts[0]['course_key'], course_key)
        self.assertEqual(self.signal_broadcasts[0]['milestone'].namespace, unicode(prerequisite_course_key))
        self.assertEqual(self.signal_broadcasts[0]['milestone_relationship_type'], 'requires')

        self.assertEqual(self.signal_broadcasts[1]['course_key'], prerequisite_course_key)
        self.assertEqual(self.signal_broadcasts[1]['milestone'].namespace, unicode(prerequisite_course_key))
        self.assertEqual(self.signal_broadcasts[1]['milestone_relationship_type'], 'fulfills')


    # def test_on_course_deleted(self):
    #     course_deleted.send(
    #         sender=self,
    #         course_key='foo/bar/baz',
    #     )

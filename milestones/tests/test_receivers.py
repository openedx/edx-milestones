from django.conf import settings
from django.dispatch import receiver
from django.test import TestCase

from opaque_keys.edx.keys import CourseKey

from milestones import api
from milestones.signals import course_milestone_added, course_milestone_removed

from mocks import signals as mock_signals

class ReceiverTestCase(TestCase):

    def setUp(self):
        self.signal_log = []
        self.test_course_key = CourseKey.from_string('the/course/key')
        self.test_prerequisite_course_key = CourseKey.from_string('prerequisite/course/key')

    # def test_on_course_deleted(self):
    #     course_deleted.send(
    #         sender=self,
    #         course_key='foo/bar/baz',
    #     )

    def test_on_course_prequisite_course_added(self):

        # Define and connect the local signal listener before doing anything
        @receiver(course_milestone_added)
        def signal_listener(sender, signal, course_key, relationship, milestone):
            self.signal_log.append(
                {
                    'course_key': course_key,
                    'relationship': relationship,
                    'milestone': milestone
                }
            )

        # Broadcast the event to the application
        mock_signals.course_prerequisite_course_added.send(
            sender=self,
            course_key=self.test_course_key,
            prerequisite_course_key=self.test_prerequisite_course_key,
        )

        # Confirm the prerequisite course fulfills its generic milestone
        # The namespace for generic course milestones is the course identifier
        prereq_milestones = api.get_course_milestones(course_key=self.test_prerequisite_course_key, relationship='fulfills')
        self.assertEqual(unicode(self.test_prerequisite_course_key), prereq_milestones[0]['namespace'])

        # Confirm the main course requires the prerequisite course's generic milestone
        course_milestones = api.get_course_milestones(course_key=self.test_course_key, relationship='requires')
        self.assertEqual(unicode(self.test_prerequisite_course_key), course_milestones[0]['namespace'])

        # Confirm the workflow events were properly emitted
        self.assertEqual(len(self.signal_log), 2)
        self.assertEqual(self.signal_log[0]['course_key'], self.test_course_key)
        self.assertEqual(self.signal_log[0]['relationship'], 'requires')
        self.assertEqual(self.signal_log[0]['milestone'].namespace, unicode(self.test_prerequisite_course_key))

        self.assertEqual(self.signal_log[1]['course_key'], self.test_prerequisite_course_key)
        self.assertEqual(self.signal_log[1]['relationship'], 'fulfills')
        self.assertEqual(self.signal_log[1]['milestone'].namespace, unicode(self.test_prerequisite_course_key))

    def test_on_course_prerequisite_course_removed(self):

        # Define and connect the local signal listener before doing anything
        @receiver(course_milestone_removed)
        def signal_listener(sender, signal, course_key, relationship, milestone):
            self.signal_log.append(
                {
                    'course_key': course_key,
                    'relationship': relationship,
                    'milestone': milestone
                }
            )

        # Broadcast the events to the application
        mock_signals.course_prerequisite_course_added.send(
            sender=self,
            course_key=self.test_course_key,
            prerequisite_course_key=self.test_prerequisite_course_key,
        )

        # Confirm the prerequisite course fulfills its generic milestone
        prereq_milestones = api.get_course_milestones(course_key=self.test_prerequisite_course_key, relationship='fulfills')
        self.assertEqual(unicode(self.test_prerequisite_course_key), prereq_milestones[0]['namespace'])

        # Confirm the main course requires the prerequisite course's generic milestone
        course_milestones = api.get_course_milestones(course_key=self.test_course_key, relationship='requires')
        self.assertEqual(len(course_milestones), 1)


        mock_signals.course_prerequisite_course_removed.send(
            sender=self,
            course_key=self.test_course_key,
            prerequisite_course_key=self.test_prerequisite_course_key,
        )

        # Confirm the prerequisite course still fulfills its generic milestone
        prereq_milestones = api.get_course_milestones(course_key=self.test_prerequisite_course_key, relationship='fulfills')
        self.assertEqual(unicode(self.test_prerequisite_course_key), prereq_milestones[0]['namespace'])

        # Confirm the main course no longer requires the prerequisite course's generic milestone
        course_milestones = api.get_course_milestones(course_key=self.test_course_key, relationship='requires')
        self.assertEqual(len(course_milestones), 0)

        # Confirm the workflow events were properly emitted
        self.assertEqual(len(self.signal_log), 1)
        self.assertEqual(self.signal_log[0]['course_key'], self.test_course_key)
        self.assertEqual(self.signal_log[0]['milestone'].namespace, unicode(self.test_prerequisite_course_key))

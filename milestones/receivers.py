"""
Receivers are listeners connected to the Django pub/sub signal
pipeline.  When they observe a signal they run the decorated operation.

In this particular application, the receivers simply hand-off to the
orchestration layer, which manages the application's workflows.
"""
from django.conf import settings
from django.dispatch import receiver

from .manager import MilestoneManager

if not settings.TEST_MODE:
    import util.signals as signals
else:
    import tests.mocks.signals as signals

@receiver(signals.course_deleted)
def on_course_deleted(sender, signal, **kwargs):
    """
    Listens for a 'course_deleted' signal and when observed
    hands off the event data to the MilestoneManager for processing
    """
    MilestoneManager.delete_course_references(**kwargs)


@receiver(signals.course_prerequisite_course_added)
def on_course_prerequisite_course_added(sender, signal, **kwargs):
    """
    Listens for a 'prerequisite_course_added' signal and when observed
    hands off the event data to the MilestoneManager for processing
    """
    MilestoneManager.add_prerequisite_course_to_course(**kwargs)


@receiver(signals.course_prerequisite_course_removed)
def on_course_prerequisite_course_removed(sender, signal, **kwargs):
    """
    Listens for a 'prerequisite_course_deleted' signal and when observed
    hands off the event data to the MilestoneManager for processing
    """
    MilestoneManager.remove_prerequisite_course_from_course(**kwargs)

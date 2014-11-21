"""
Receivers are listeners connected to the Django pub/sub signal
pipeline.  When they observe a signal they run the decorated operation.

In this particular application, the receivers simply hand-off to the
orchestration layer, which manages the application's workflows.
"""
from django.dispatch import receiver

from .manager import MilestoneManager


@receiver(course_deleted)
def on_course_deleted(sender, **kwargs):
    """
    Listens for a 'course_deleted' signal and when observed
    hands off the event data to the MilestoneManager for processing
    """
    MilestoneManager.delete_course_references(**kwargs)


@receiver(prerequisite_course_added)
def on_prerequisite_course_added(sender, **kwargs):
    """
    Listens for a 'prerequisite_course_added' signal and when observed
    hands off the event data to the MilestoneManager for processing
    """
    MilestoneManager.add_prerequisite_course_to_course(**kwargs)

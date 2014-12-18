"""
Receivers are listeners connected to the Django pub/sub signal
pipeline.  When they observe a signal they run the decorated operation.

In this particular application, the receivers simply hand-off to the
orchestration layer, which manages the application's workflows.
"""
from django.conf import settings
from django.dispatch import receiver

import milestones.api as api


if hasattr(settings, 'TEST_MODE') and settings.TEST_MODE:
    import tests.mocks.signals as signals
else:
    import util.signals as signals


@receiver(signals.course_deleted)
def on_course_deleted(sender, signal, **kwargs):
    """
    Listens for a 'course_deleted' signal and when observed
    hands off the event data to the MilestoneManager for processing
    """
    api.remove_course_references(**kwargs)

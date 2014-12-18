"""
Receivers are listeners connected to the Django pub/sub signal
pipeline.  When they observe a signal they run the decorated operation.

In this particular application, the receivers simply hand-off to the
orchestration layer, which manages the application's workflows.
"""
import os

from django.conf import settings
from django.dispatch import receiver

import milestones.api as api


# TEST_MODE is a local app setting, TRAVIS_MODE is for Travis CI builds
print 'TEST_MODE: {}'.format(getattr(settings, 'TEST_MODE'))
print 'TRAVIS_MODE: {}'.format(os.getenv('TRAVIS_MODE'))

try:
    import util.signals as signals
except ImportError:
    if getattr(settings, 'TEST_MODE', False) or os.getenv('TRAVIS_MODE', False):
        import  milestones.tests.mocks.signals as signals
    else:
        raise ImportError

@receiver(signals.course_deleted)
def on_course_deleted(sender, signal, **kwargs):  # pylint: disable=unused-argument
    """
    Listens for a 'course_deleted' signal and when observed
    hands off the event data to the MilestoneManager for processing
    """
    api.remove_course_references(**kwargs)

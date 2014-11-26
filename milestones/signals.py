"""
Signals are outbound messages broadcast by this app.  We define the
signals in this module and then submit them to the dispatcher, typically
in the orchestration layer (ie, the Manager) as part of a workflow.
"""

from django.dispatch import Signal

# SIGNALS BROADCAST BY THIS APP
course_milestone_added = Signal(providing_args=["course_key", "milestone"])

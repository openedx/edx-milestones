"""
Signals are outbound messages broadcast by this app.  We define the
signals in this module and then submit them to the dispatcher, typically
in the orchestration layer (ie, the Manager) as part of a workflow.
"""

from django.dispatch import Signal

# SIGNALS BROADCAST BY THIS APP

# MOCK SIGNALS USED FOR STANDALONE TESTING
course_completed(providing_args=["course_key", "student"])
course_deleted(providing_args=["course_key"])
course_entrance_exam_added(providing_args=["course_key", "content_key", "milestone"])
course_prequisite_course_added(providing_args=["course_key", "prerequisite_course_key", "milestone"])

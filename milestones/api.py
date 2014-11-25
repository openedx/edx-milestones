"""
api.py is an interface module for Python-level integration with the
Milestones app.

In this particular application, the operations simply hand-off to the
orchestration layer, which manages the application's workflows.

This module is designed primarily for read access, and is helpful for
unit test assertions.  If you are considering adding write operations
to this API, please review receivers.py and consider using or adding
new Django event signals instead!!!
"""
from manager import MilestoneManager


def get_course_milestones(**kwargs):
    return MilestoneManager.get_course_milestones(**kwargs)

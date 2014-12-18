"""
Mock signals module -- use these to trick Milestones into thinking the system
has broadcast a signal that it is listening for in receivers.py
"""
from django.dispatch import Signal

# MOCK SIGNALS USED FOR STANDALONE TESTING
course_deleted = Signal(providing_args=["course_key"])

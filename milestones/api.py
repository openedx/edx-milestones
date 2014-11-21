"""
api.py is an nterface module for Python-level integration with the
Milestones app.

In this particular application, the operations simply hand-off to the
orchestration layer, which manages the application's workflows.

This module is helpful for unit testing.  For 'real' use cases, however,
please consider integrating via Django signals instead!
"""

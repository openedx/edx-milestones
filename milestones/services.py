"""
A wrapper class around requested methods exposed in api.py
"""

from __future__ import absolute_import, unicode_literals
import types

from milestones import api as milestones_api


class MilestonesService:  # pylint: disable=too-few-public-methods
    """
    An xBlock service for xBlocks to talk to the Milestones subsystem.

    NOTE: This is a Singleton class. We should only have one instance of it!
    """

    _instance = None

    REQUESTED_FUNCTIONS = [
        'get_course_content_milestones',
    ]

    def __new__(cls, *args, **kwargs):
        """
        This is the class factory to make sure this is a Singleton
        """
        if not cls._instance:
            cls._instance = super(MilestonesService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """
        Class initializer, which just inspects the libraries and exposes the same functions
        listed in REQUESTED_FUNCTIONS
        """
        self._bind_to_requested_functions()

    def _bind_to_requested_functions(self):
        """
        bind module functions. Since we use underscores to mean private methods, let's exclude those.
        """
        for attr_name in self.REQUESTED_FUNCTIONS:
            attr = getattr(milestones_api, attr_name, None)
            if isinstance(attr, types.FunctionType) and not attr_name.startswith('_'):
                if not hasattr(self, attr_name):
                    setattr(self, attr_name, attr)

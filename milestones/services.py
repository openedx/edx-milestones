"""
A wrapper class around all methods exposed in api.py
"""

import types


class MilestonesService(object):
    """
    An xBlock service for xBlocks to talk to the Milestones subsystem.*

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
        """
        from util import milestones_helpers as milestones_api
        self._bind_to_module_functions(milestones_api)

    def _bind_to_module_functions(self, module):
        """
        bind module functions. Since we use underscores to mean private methods, let's exclude those.
        """
        # for attr_name in dir(module):
        #     attr = getattr(module, attr_name, None)
        #     if (isinstance(attr, types.FunctionType) and not attr_name.startswith('_') and attr_name in self.REQUESTED_FUNCTIONS):
        #         if not hasattr(self, attr_name):
        #             setattr(self, attr_name, attr)

        for attr_name in self.REQUESTED_FUNCTIONS:
            attr = module.get_service(attr_name)
            if not hasattr(self, attr_name):
                setattr(self, attr_name, attr)
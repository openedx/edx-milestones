"""
Test for the xBlock service
"""

from __future__ import absolute_import, unicode_literals
import unittest
import types

from milestones.services import MilestonesService
from milestones import api as milestones_api


class TestMilestonesService(unittest.TestCase):  # pylint: disable=too-many-public-methods
    """
    Tests for MilestonesService
    """
    def test_basic(self):
        """
        See if the MilestonesService exposes the expected methods
        """

        service = MilestonesService()

        for attr_name in dir(milestones_api):
            attr = getattr(milestones_api, attr_name, None)
            if isinstance(attr, types.FunctionType) and not attr_name.startswith('_'):
                if attr_name in MilestonesService.REQUESTED_FUNCTIONS:
                    self.assertTrue(hasattr(service, attr_name))
                else:
                    self.assertFalse(hasattr(service, attr_name))

    def test_singleton(self):
        """
        Test to make sure the MilestonesService is a singleton.
        """
        service1 = MilestonesService()
        service2 = MilestonesService()
        self.assertIs(service1, service2)

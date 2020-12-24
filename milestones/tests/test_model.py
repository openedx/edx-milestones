# pylint: disable=no-member,too-many-public-methods
"""
Models test cases
"""

from django.test import TestCase
from milestones.models import MilestoneRelationshipType, Milestone


class MilestonesTestCaseMixin(TestCase):
    """
    TestCase for models
    """

    def test_check_model_str(self):
        """
        checking model str methods
        """
        milestone_relation_ship = MilestoneRelationshipType.objects.create(name='milestone_relation_ship')
        milestone = Milestone.objects.create(namespace='milestone')

        self.assertEqual(milestone_relation_ship.__str__(), 'milestone_relation_ship')
        self.assertEqual(milestone.__str__(), 'milestone')

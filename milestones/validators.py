"""
Validators are used by the MilestoneManager to confirm the validity of
inbound information prior to a data.py handoff
"""
import data

def milestone_exists(milestone):
    milestone = data.get_milestone(milestone)
    if milestone is None:
        return False
    return True


def milestone_is_valid(milestone):
    if milestone is None:
        return False
    if not len(milestone.namespace):
        return False
    return True

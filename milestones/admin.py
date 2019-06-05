"""
Admin module for milestones app
"""
from __future__ import absolute_import, unicode_literals
from django.contrib import admin

from milestones.models import (
    CourseContentMilestone,
    CourseMilestone,
    Milestone,
    MilestoneRelationshipType,
    UserMilestone,
)


admin.site.register(CourseContentMilestone)
admin.site.register(CourseMilestone)
admin.site.register(Milestone)
admin.site.register(MilestoneRelationshipType)
admin.site.register(UserMilestone)

"""
Database ORM models managed by this Django app
Please do not integrate directly with these models!!!  This app currently
offers two APIs -- api.py for direct Python integration and receivers.py,
which leverages Django's signal framework.
"""

from django.db import models
from model_utils.models import TimeStampedModel


class Milestone(TimeStampedModel):
    """
    A Milestone is a representation of an accomplishment which can be
    attained by a user. Milestones have a base set of meta data
    describing the milestone, including id, name, and description.
    Milestones can be used to drive functionality and behavior 'behind
    the scenes' in Open edX, such as with the Pre-Requisite Course and
    Course Pre-Assessment use cases.
    """
    namespace = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    active = models.BooleanField(default=True)


class MilestoneRelationshipType(TimeStampedModel):
    """
    A MilestoneRelationshipType represents a category of link available
    between a Milestone and a particular learning object (such as a
    Course). In addition to learning objects, a MilestoneRelationshipType
    can also represent the link between a Milestone and other platform
    entities (such as a Student).  For example, a Course Author may
    indicate that Course 101 "fulfills" Milestone A, creating a new
    CourseMilestone record in the process. When a Student completes
    Course 101, a new StudentMilestone record is created reflecting the
    newly-attained Milestone A.  The Course Author may also indicate
    that Course 102 "requires" Milestone A, yielding a second
    CourseMilestone record.  Because the Student has gained Milestone A
    (via Course 101), they can access Course 102.

    This same process of indicating MilestoneRelationshipTypes can be
    applied to other learning objects as well, such as course content
    (XBlocks/modules).
    """
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)


class CourseMilestone(TimeStampedModel):
    """
    A CourseMilestone represents the link between a Course and a
    Milestone. Because Courses are not true Open edX entities (in the
    Django/ORM sense) the modeling and integrity will be limited to that
    of specifying CourseKeyFields in this model, as well as related ones
    below. In addition, a MilestoneRelationshipType specifies the
    particular sort of relationship that exists between the Course and
    the Milestone, such as "Pre-Requisite".
    """
    course_id = models.CharField(max_length=255, db_index=True)
    milestone = models.ForeignKey(Milestone, db_index=True)
    milestone_relationship_type = models.ForeignKey(MilestoneRelationshipType, db_index=True)
    active = models.BooleanField(default=True)

    class Meta:
        """ Meta class for this Django model """
        unique_together = (("course_id", "milestone"),)
        # index_together = [
        #     ["course_id", "milestone"],
        #     ["course_id", "milestone", "milestone_relationship_type"],
        # ]


class CourseContentMilestone(TimeStampedModel):
    """
    A CourseContentMilestone represents the link between a specific
    Course module (such as an XBlock) and a Milestone. Because
    CourseContent objects are not true Open edX entities (in the
    Django/ORM sense) the modeling and integrity will be limited to that
    of specifying LocationKeyFields in this model, as well as related
    ones. In addition, a MilestoneRelationshipType specifies the
    particular sort of relationship that exists between the Milestone
    and the CourseContent, such as "Pre-Assessment" or "Entrance Exam".
    """
    course_id = models.CharField(max_length=255, db_index=True)
    content_id = models.CharField(max_length=255, db_index=True)
    milestone = models.ForeignKey(Milestone, db_index=True)
    milestone_relationship_type = models.ForeignKey(MilestoneRelationshipType, db_index=True)
    active = models.BooleanField(default=True)

    class Meta:
        """ Meta class for this Django model """
        unique_together = (("course_id", "content_id", "milestone"),)
        # index_together = [
        #     ["course_id", "content_id"],
        #     ["course_id", "content_id", "milestone"],
        #     ["course_id", "content_id", "milestone", "milestone_relationship_type"],
        # ]


class UserMilestone(TimeStampedModel):
    """
    A UserMilestone represents an stage reached or event experienced
    by a User during their interactions with the Open edX platform.
    The addition of a MilestoneRelationshipType field in this model
    allows for use cases such as "Goals", in which a User might keep
    a list of Milestones they are interested in attaining. Side Note: In
    the Mozilla Open Badges world, this collection concept is referred
    to as the user's "backpack".
    """
    user_id = models.IntegerField(db_index=True)
    milestone = models.ForeignKey(Milestone, db_index=True)
    source = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        """ Meta class for this Django model """
        unique_together = ("user_id", "milestone")
        # index_together = [
        #     ["user_id", "milestone"],
        # ]

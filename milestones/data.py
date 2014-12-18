# pylint: disable=no-member
"""
Application data management/abstraction layer.  Responsible for:

1) Accessing information from various resources:
* Internal application state  (through local models in models.py)
* External application state  (ORM bindings with other apps, yuck)
* Remote data services (through service adapters in resources.py)

2) Calculating derivative information from existing state:
* Algorithms and data manipulations
* Aggregations
* Annotations
* Alternative data representations

Accepts and returns standard Python data structures (dicts, arrays of dicts)
for easy consumption and manipulation by callers -- the queryset stops here!

Note the terminology difference at this layer vs. API -- create/fetch/update/delete/

When the time comes for remote resources, import the module like so:
if getattr(settings, 'TEST_MODE', False) or os.getenv('TRAVIS_MODE', False):
    import milestones.tests.mocks.resources as remote
else:
    import milestones.resources as remote
"""
import milestones.models as internal
import milestones.serializers as serializers


# PRIVATE/INTERNAL METHODS
def _get_relationship_type(relationship):
    """
    Retrieves milestone relationship type object from backend
    """
    mrt = None
    if relationship:
        try:
            mrt = internal.MilestoneRelationshipType.objects.get(
                name=relationship,
                active=True
            )
        except internal.MilestoneRelationshipType.DoesNotExist:
            mrt = None
    return mrt


# PUBLIC METHODS
def create_milestone(milestone):
    """
    Inserts a new milestone into app/local state
    Returns a dictionary representation of the object
    """
    milestone_obj = serializers.deserialize_milestone(milestone)
    milestone, __ = internal.Milestone.objects.get_or_create(
        namespace=milestone_obj.namespace,
        name=milestone_obj.name,
        active=True,
        defaults={
            'description': milestone_obj.description,
        }
    )
    return serializers.serialize_milestone(milestone)


def update_milestone(milestone):
    """
    Updates an existing milestone in app/local state
    Returns a dictionary representation of the object
    """
    milestone_obj = serializers.deserialize_milestone(milestone)
    try:
        milestone = internal.Milestone.objects.get(id=milestone_obj.id)
        milestone.name = milestone_obj.name
        milestone.namespace = milestone_obj.namespace
        milestone.description = milestone_obj.description
        milestone.active = milestone_obj.active
    except internal.Milestone.DoesNotExist:
        return None
    return serializers.serialize_milestone(milestone)


def delete_milestone(milestone):
    """
    Deletes an existing milestone from app/local state
    No return currently defined for this operation
    """
    milestone_obj = serializers.deserialize_milestone(milestone)
    try:
        milestone_obj = internal.Milestone.objects.get(
            id=milestone_obj.id,
            active=True
        )
        milestone_obj.active = False
        milestone_obj.save()
    except internal.Milestone.DoesNotExist:
        pass


def fetch_milestones(milestone):
    """
    Retrieves a set of matching milestones from app/local state
    Returns a list-of-dicts representation of the object
    """
    if milestone is None:
        return None
    milestone_obj = serializers.deserialize_milestone(milestone)
    if milestone_obj.id is not None:
        milestones = internal.Milestone.objects.filter(
            id=milestone_obj.id,
            active=True,
        )
    elif milestone_obj.namespace is not None:
        milestones = internal.Milestone.objects.filter(
            namespace=milestone_obj.namespace,
            active=True
        )
    return serializers.serialize_milestones(milestones)


def create_course_milestone(course_key, relationship, milestone):
    """
    Inserts a new course-milestone into app/local state
    No response currently defined for this operation
    """
    mrt, __ = internal.MilestoneRelationshipType.objects.get_or_create(
        name=relationship,
        active=True
    )
    milestone_obj = serializers.deserialize_milestone(milestone)
    internal.CourseMilestone.objects.get_or_create(
        course_id=unicode(course_key),
        milestone=milestone_obj,
        milestone_relationship_type=mrt,
        active=True,
    )


def delete_course_milestone(course_key, milestone):
    """
    Removes an existing course-milestone from app/local state
    No response currently defined for this operation
    """
    try:
        internal.CourseMilestone.objects.get(
            course_id=unicode(course_key),
            milestone=milestone['id'],
            active=True,
        ).delete()
    except internal.CourseMilestone.DoesNotExist:
        pass


def fetch_courses_milestones(course_keys, relationship=None, user=None):
    """
    Retrieves the set of milestones currently linked to the specified courses
    Optionally pass in 'relationship' (ex. 'fulfills') to filter down the set
    """
    queryset = internal.CourseMilestone.objects.filter(
        course_id__in=course_keys,
        active=True
    ).select_related('milestone')

    # if milestones relationship type found then apply the filter
    mrt = _get_relationship_type(relationship)
    if mrt:
        queryset = queryset.filter(
            milestone_relationship_type=mrt.id,
        )

    # To pull the list of milestones a user HAS, use get_user_milestones
    # Use fetch_courses_milestones to pull the list of milestones that a user does not yet
    # have for the specified course
    if relationship == 'requires' and user and user.get('id', 0) > 0:
        queryset = queryset.exclude(milestone__usermilestone__user_id=user['id'])

    # Assemble the response container
    course_milestones = []
    if len(queryset):
        for milestone in queryset:
            course_milestones.append(serializers.serialize_milestone_with_course(milestone))

    return course_milestones


def create_course_content_milestone(course_key, content_key, relationship, milestone):
    """
    Inserts a new course-content-milestone into app/local state
    No response currently defined for this operation
    """
    mrt, __ = internal.MilestoneRelationshipType.objects.get_or_create(
        name=relationship,
        active=True
    )
    milestone_obj = serializers.deserialize_milestone(milestone)
    internal.CourseContentMilestone.objects.get_or_create(
        course_id=unicode(course_key),
        content_id=unicode(content_key),
        milestone=milestone_obj,
        milestone_relationship_type=mrt,
        active=True,
    )


def delete_course_content_milestone(course_key, content_key, milestone):
    """
    Removes an existing course-content-milestone from app/local state
    No response currently defined for this operation
    """
    try:
        internal.CourseContentMilestone.objects.get(
            course_id=unicode(course_key),
            content_id=unicode(content_key),
            milestone=milestone['id'],
            active=True,
        ).delete()
    except internal.CourseContentMilestone.DoesNotExist:
        pass


def fetch_course_content_milestones(course_key, content_key, relationship=None):
    """
    Retrieves the set of milestones currently linked to the specified course
    Optionally pass in 'relationship' (ex. 'fulfills') to filter down the set
    """
    if relationship is None:
        queryset = internal.Milestone.objects.filter(
            coursecontentmilestone__course_id=unicode(course_key),
            coursecontentmilestone__content_id=unicode(content_key),
            active=True
        )
    else:
        try:
            mrt = internal.MilestoneRelationshipType.objects.get(
                name=relationship,
                active=True
            )
        except internal.MilestoneRelationshipType.DoesNotExist:
            # If the relationship type doesn't exist then we can't do much more
            return None
        queryset = internal.Milestone.objects.filter(
            coursecontentmilestone__course_id=unicode(course_key),
            coursecontentmilestone__content_id=unicode(content_key),
            coursecontentmilestone__milestone_relationship_type=mrt.id,
            active=True,
        )
    course_content_milestones = []
    if len(queryset):
        for milestone in queryset:
            course_content_milestones.append(serializers.serialize_milestone(milestone))
    return course_content_milestones


def create_user_milestone(user, milestone):
    """
    Inserts a new user-milestone into app/local state
    No response currently defined for this operation
    """
    milestone_obj = serializers.deserialize_milestone(milestone)
    internal.UserMilestone.objects.get_or_create(
        user_id=user['id'],
        milestone=milestone_obj,
        active=True,
    )


def delete_user_milestone(user, milestone):
    """
    Removes an existing user-milestone from app/local state
    No response currently defined for this operation
    """
    try:
        internal.UserMilestone.objects.get(
            user_id=user['id'],
            milestone=milestone['id'],
            active=True,
        ).delete()
    except internal.UserMilestone.DoesNotExist:
        pass


def fetch_user_milestones(user, milestone=None):
    """
    Retrieves the set of milestones currently linked to the specified user
    """
    if milestone is None:
        queryset = internal.Milestone.objects.filter(
            usermilestone__user_id=user['id'],
            active=True,
        )
    else:
        queryset = internal.Milestone.objects.filter(
            id=milestone['id'],
            usermilestone__user_id=user['id'],
            active=True,
        )
    user_milestones = []
    if len(queryset):
        for milestone in queryset:
            user_milestones.append(serializers.serialize_milestone(milestone))
    return user_milestones


def delete_course_references(course_key):
    """
    Removes references to course keys within this app (ref: receivers.py and api.py)
    """
    internal.CourseMilestone.objects.filter(course_id=unicode(course_key)).delete()
    internal.Milestone.objects.filter(namespace=unicode(course_key)).delete()

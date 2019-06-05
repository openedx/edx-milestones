# pylint: disable=no-member,expression-not-assigned
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
from __future__ import absolute_import, unicode_literals

import six

from . import exceptions
from . import models as internal
from . import serializers


# PRIVATE/INTERNAL METHODS (public methods located further down)
def _get_milestone_relationship_type(relationship):
    """
    Retrieves milestone relationship type object from backend datastore
    """
    try:
        return internal.MilestoneRelationshipType.objects.get(
            name=relationship,
            active=True
        )
    except internal.MilestoneRelationshipType.DoesNotExist:
        exceptions.raise_exception(
            "MilestoneRelationshipType",
            {'name': relationship},
            exceptions.InvalidMilestoneRelationshipTypeException
        )


def _activate_record(record):
    """
    Enables database records by setting the 'active' attribute to True
    The queries in this module filter out inactive records as part of their criteria
    This effectively allows us to soft-delete records so they are not lost forever
    """
    record.active = True
    record.save()


def _inactivate_record(record):
    """
    Disables database records by setting the 'active' attribute to False
    The queries in this module filter out inactive records as part of their criteria
    This effectively allows us to soft-delete records so they are not lost forever
    """
    record.active = False
    record.save()


def _activate_milestone(milestone, propagate=True):
    """
    Activates an inactivated (soft-deleted) milestone as well as any inactive relationships
    """
    if propagate:
        [_activate_record(record) for record
         in internal.CourseMilestone.objects.filter(milestone_id=milestone.id, active=False)]

        [_activate_record(record) for record
         in internal.CourseContentMilestone.objects.filter(milestone_id=milestone.id, active=False)]

        [_activate_record(record) for record
         in internal.UserMilestone.objects.filter(milestone_id=milestone.id, active=False)]

    [_activate_record(record) for record
     in internal.Milestone.objects.filter(id=milestone.id, active=False)]


def _inactivate_milestone(milestone):
    """
    Inactivates an activated milestone as well as any active relationships
    """
    [_inactivate_record(record) for record
     in internal.CourseMilestone.objects.filter(milestone_id=milestone.id, active=True)]

    [_inactivate_record(record) for record
     in internal.CourseContentMilestone.objects.filter(milestone_id=milestone.id, active=True)]

    [_inactivate_record(record) for record
     in internal.UserMilestone.objects.filter(milestone_id=milestone.id, active=True)]

    [_inactivate_record(record) for record
     in internal.Milestone.objects.filter(id=milestone.id, active=True)]


# PUBLIC METHODS
def create_milestone(milestone, propagate=True):
    """
    Inserts a new milestone into app/local state given the following dictionary:
    {
        'name': string,
        'display_name': string,
        'namespace': string,
        'description': string
    }
    Returns an updated dictionary including a new 'id': integer field/value
    """
    # Trust, but verify...
    if not milestone.get('name'):
        exceptions.raise_exception("Milestone", milestone, exceptions.InvalidMilestoneException)
    if not milestone.get('namespace'):
        exceptions.raise_exception("Milestone", milestone, exceptions.InvalidMilestoneException)
    milestone_obj = serializers.deserialize_milestone(milestone)
    try:
        milestone = internal.Milestone.objects.get(
            namespace=milestone_obj.namespace,
            name=milestone_obj.name,
        )
        # If the milestone exists, but was inactivated, we can simply turn it back on
        if not milestone.active:
            _activate_milestone(milestone, propagate)
    except internal.Milestone.DoesNotExist:
        milestone = internal.Milestone.objects.create(
            namespace=milestone_obj.namespace,
            name=milestone_obj.name,
            description=milestone_obj.description,
            display_name=milestone_obj.display_name,
            active=True
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
        exceptions.raise_exception("Milestone", milestone, exceptions.InvalidMilestoneException)
    return serializers.serialize_milestone(milestone)


def delete_milestone(milestone):
    """
    Inactivates an existing milestone from app/local state
    No return currently defined for this operation
    """
    milestone_obj = serializers.deserialize_milestone(milestone)
    _inactivate_milestone(milestone_obj)


def fetch_milestone(milestone_id):
    """
    Retrieves a specific milestone from app/local state
    Returns a dictionary representation of the object
    """
    if not milestone_id:
        exceptions.raise_exception("Milestone", {'id': milestone_id}, exceptions.InvalidMilestoneException)
    milestone = {'id': milestone_id}
    milestones = fetch_milestones(milestone)
    if not milestones:
        exceptions.raise_exception("Milestone", milestone, exceptions.InvalidMilestoneException)
    return milestones[0]


def fetch_milestones(milestone):
    """
    Retrieves a set of matching milestones from app/local state
    Returns a list-of-dicts representation of the object
    """
    if milestone is None:
        exceptions.raise_exception("Milestone", milestone, exceptions.InvalidMilestoneException)
    milestone_obj = serializers.deserialize_milestone(milestone)
    if milestone_obj.id is not None:
        return serializers.serialize_milestones(internal.Milestone.objects.filter(
            id=milestone_obj.id,
            active=True,
        ))
    if milestone_obj.namespace:
        return serializers.serialize_milestones(internal.Milestone.objects.filter(
            namespace=six.text_type(milestone_obj.namespace),
            active=True
        ))

    # If we get to this point the caller is attempting to match on an unsupported field
    exceptions.raise_exception("Milestone", milestone, exceptions.InvalidMilestoneException)


def fetch_milestone_relationship_types():
    """
    Model accessor method to return supported milestone relationship types
    """
    return internal.MilestoneRelationshipType.get_supported_milestone_relationship_types()


def create_course_milestone(course_key, relationship, milestone):
    """
    Inserts a new course-milestone into app/local state
    No response currently defined for this operation
    """
    relationship_type = _get_milestone_relationship_type(relationship)
    milestone_obj = serializers.deserialize_milestone(milestone)
    try:
        relationship = internal.CourseMilestone.objects.get(
            course_id=six.text_type(course_key),
            milestone=milestone_obj,
            milestone_relationship_type=relationship_type
        )
        # If the relationship exists, but was inactivated, we can simply turn it back on
        if not relationship.active:
            _activate_record(relationship)
    except internal.CourseMilestone.DoesNotExist:
        relationship = internal.CourseMilestone.objects.create(
            course_id=six.text_type(course_key),
            milestone=milestone_obj,
            milestone_relationship_type=relationship_type,
            active=True
        )


def delete_course_milestone(course_key, milestone):
    """
    Removes an existing course-milestone from app/local state
    No response currently defined for this operation
    """
    try:
        relationship = internal.CourseMilestone.objects.get(
            course_id=six.text_type(course_key),
            milestone=milestone['id'],
            active=True,
        )
        _inactivate_record(relationship)
    except internal.CourseMilestone.DoesNotExist:
        # If we're being asked to delete a course-milestone link
        # that does not exist in the database then our work is done
        pass


def fetch_courses_milestones(course_keys, relationship=None, user=None):
    """
    Retrieves the set of milestones currently linked to the specified courses
    Optionally pass in 'relationship' (ex. 'fulfills') to filter down the set
    Optionally pass in 'user' to constrain the set to those which the user has collected
    """
    queryset = internal.CourseMilestone.objects.filter(
        course_id__in=course_keys,
        active=True
    ).select_related('milestone')

    # if milestones relationship type found then apply the filter
    if relationship is not None:
        mrt = _get_milestone_relationship_type(relationship)
        queryset = queryset.filter(
            milestone_relationship_type=mrt.id,
        )

    # To pull the list of milestones a user HAS, use get_user_milestones
    # Use fetch_courses_milestones to pull the list of milestones that a user does not yet
    # have for the specified course
    relationships = fetch_milestone_relationship_types()
    if relationship == relationships['REQUIRES'] and user and user.get('id', 0) > 0:
        queryset = queryset.exclude(
            milestone__usermilestone__in=internal.UserMilestone.objects.filter(user_id=user['id'], active=True)
        )

    return [serializers.serialize_milestone_with_course(milestone) for milestone in queryset]


def create_course_content_milestone(course_key, content_key, relationship, milestone, requirements=None):
    """
    Inserts a new course-content-milestone into app/local state
    No response currently defined for this operation
    """
    relationship_type = _get_milestone_relationship_type(relationship)
    milestone_obj = serializers.deserialize_milestone(milestone)
    requirements = serializers.serialize_requirements(requirements)
    try:
        relationship = internal.CourseContentMilestone.objects.get(
            course_id=six.text_type(course_key),
            content_id=six.text_type(content_key),
            milestone=milestone_obj,
            milestone_relationship_type=relationship_type
        )
        # If the relationship exists, but was inactivated, we can simply turn it back on
        if not relationship.active:
            relationship.requirements = requirements
            _activate_record(relationship)
        elif relationship.requirements != requirements:
            # Update requirements field if necessary
            relationship.requirements = requirements
            relationship.save()
    except internal.CourseContentMilestone.DoesNotExist:
        relationship = internal.CourseContentMilestone.objects.create(
            course_id=six.text_type(course_key),
            content_id=six.text_type(content_key),
            milestone=milestone_obj,
            milestone_relationship_type=relationship_type,
            requirements=requirements,
            active=True
        )


def delete_course_content_milestone(course_key, content_key, milestone):
    """
    Removes an existing course-content-milestone from app/local state
    No response currently defined for this operation
    """
    try:
        relationship = internal.CourseContentMilestone.objects.get(
            course_id=six.text_type(course_key),
            content_id=six.text_type(content_key),
            milestone=milestone['id'],
            active=True,
        )
        _inactivate_record(relationship)
    except internal.CourseContentMilestone.DoesNotExist:
        # If we're being asked to delete a course-content-milestone link
        # that does not exist in the database then our work is done
        pass


def fetch_course_content_milestones(content_key=None, course_key=None, relationship=None, user=None):
    """
    Retrieves the set of milestones currently linked to the specified course content
    Optionally pass in 'relationship' (ex. 'fulfills') to filter down the set
    Optionally pass in 'user' to further-filter the set (ex. for retrieving unfulfilled milestones)
    """
    queryset = internal.CourseContentMilestone.objects.filter(
        active=True
    ).select_related('milestone')

    if course_key is not None:
        queryset = queryset.filter(course_id=six.text_type(course_key))

    if content_key is not None:
        queryset = queryset.filter(content_id=six.text_type(content_key))

    if relationship is not None:
        mrt = _get_milestone_relationship_type(relationship)
        queryset = queryset.filter(milestone_relationship_type=mrt.id)

        # Filter for unfulfilled milestones for the given user
        if relationship == 'requires' and user and user.get('id'):
            queryset = queryset.exclude(
                milestone__usermilestone__in=internal.UserMilestone.objects.filter(user_id=user['id'], active=True)
            )

    return [serializers.serialize_milestone_with_course_content(ccm) for ccm in queryset]


def fetch_milestone_courses(milestone, relationship=None):
    """
    Retrieves the set of courses currently linked to the specified milestone
    Optionally pass in 'relationship' (ex. 'fulfills') to filter down the set
    """
    milestone_obj = serializers.deserialize_milestone(milestone)
    queryset = internal.CourseMilestone.objects.filter(
        milestone=milestone_obj,
        active=True
    ).select_related('milestone')

    # if milestones relationship type found then apply the filter
    if relationship is not None:
        queryset = queryset.filter(
            milestone_relationship_type__name=relationship,
        )

    return [serializers.serialize_milestone_with_course(milestone) for milestone in queryset]


def fetch_milestone_course_content(milestone, relationship=None):
    """
    Retrieves the set of course content modules currently linked to the specified milestone
    Optionally pass in 'relationship' (ex. 'fulfills') to filter down the set
    """
    milestone_obj = serializers.deserialize_milestone(milestone)
    queryset = internal.CourseContentMilestone.objects.filter(
        milestone=milestone_obj,
        active=True
    ).select_related('milestone')

    # if milestones relationship type found then apply the filter
    if relationship is not None:
        queryset = queryset.filter(
            milestone_relationship_type__name=relationship,
        )

    return [serializers.serialize_milestone_with_course_content(milestone) for milestone in queryset]


def create_user_milestone(user, milestone):
    """
    Inserts a new user-milestone into app/local state
    No response currently defined for this operation
    """
    milestone_obj = serializers.deserialize_milestone(milestone)
    try:
        relationship = internal.UserMilestone.objects.get(
            user_id=user['id'],
            milestone=milestone_obj.id,
        )
        # If the relationship exists, but was inactivated, we can simply turn it back on
        if not relationship.active:
            _activate_record(relationship)
    except internal.UserMilestone.DoesNotExist:
        relationship = internal.UserMilestone.objects.create(
            user_id=user['id'],
            milestone=milestone_obj,
            active=True
        )


def delete_user_milestone(user, milestone):
    """
    Removes an existing user-milestone from app/local state
    No response currently defined for this operation
    """
    try:
        record = internal.UserMilestone.objects.get(
            user_id=user['id'],
            milestone=milestone['id'],
            active=True,
        )
        _inactivate_record(record)
    except internal.UserMilestone.DoesNotExist:
        # If we're being asked to delete a user-milestone link
        # that does not exist in the database then our work is done
        pass


def fetch_user_milestones(user, milestone_data):
    """
    Retrieves the set of milestones currently linked to the specified user
    """
    queryset = internal.Milestone.objects.filter(
        usermilestone__user_id=user['id'],
        usermilestone__active=True,
    )

    # We don't currently support a 'fetch all' use case -- must supply at least one filter
    if not milestone_data.get('id') and not milestone_data.get('namespace'):
        exceptions.raise_exception("Milestone", milestone_data, exceptions.InvalidMilestoneException)

    if milestone_data.get('id'):
        queryset.filter(id=milestone_data['id'])

    if milestone_data.get('namespace'):
        queryset.filter(namespace=milestone_data['namespace'])

    return [serializers.serialize_milestone(milestone) for milestone in queryset]


def delete_content_references(content_key):
    """
    Inactivates references to content keys within this app (ref: api.py)
    Supports the 'delete entrance exam' Studio use case, when Milestones is enabled
    """
    [_inactivate_record(record) for record in internal.CourseContentMilestone.objects.filter(
        content_id=six.text_type(content_key),
        active=True
    )]


def delete_course_references(course_key):
    """
    Inactivates references to course keys within this app (ref: receivers.py and api.py)
    """
    [_inactivate_record(record) for record in internal.CourseMilestone.objects.filter(
        course_id=six.text_type(course_key),
        active=True
    )]

    [_inactivate_record(record) for record in internal.CourseContentMilestone.objects.filter(
        course_id=six.text_type(course_key),
        active=True
    )]

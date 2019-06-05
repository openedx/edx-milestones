"""
api.py is an interface module for Python-level integration with the
Milestones app.

In the current incarnation of this particular application, the API
operations are equivalent to the orchestration layer, which manages
the application's workflows.

Helplful Hint:  When modeling Milestones, I've found that it's helpful
to first consider the process for fulfilling the Milestone, and then
consider the process for requiring the Milestone.

Note the terminology difference at this layer vs. Data -- add/edit/get/remove
"""
from __future__ import absolute_import, unicode_literals
from . import data
from . import exceptions
from . import validators


# PRIVATE/INTERNAL FUNCTIONS

def _validate_course_key(course_key):
    """ Validation helper """
    if not validators.course_key_is_valid(course_key):
        exceptions.raise_exception(
            "CourseKey",
            course_key,
            exceptions.InvalidCourseKeyException
        )


def _validate_content_key(content_key):
    """ Validation helper """
    if not validators.content_key_is_valid(content_key):
        exceptions.raise_exception(
            "ContentKey",
            content_key,
            exceptions.InvalidContentKeyException
        )


def _validate_course_content_milestone_requirements(requirements):
    """ CourseContentMilestone.requirements field validation helper """
    if not validators.course_content_milestone_requirements_is_valid(requirements):
        exceptions.raise_exception(
            "CourseContentMilestone.requirements",
            requirements,
            exceptions.InvalidCourseContentMilestoneRequirementsException
        )


def _validate_milestone_data(milestone):
    """ Validation helper """
    if not validators.milestone_data_is_valid(milestone):
        exceptions.raise_exception(
            "Milestone",
            milestone,
            exceptions.InvalidMilestoneException
        )


def _validate_user(user):
    """ Validation helper """
    if not validators.user_is_valid(user):
        exceptions.raise_exception(
            "User",
            user,
            exceptions.InvalidUserException
        )


# PUBLIC FUNCTIONS
def get_milestone_relationship_types():
    """
    Exposes the available relationship type choices without exposing the data layer
    """
    return data.fetch_milestone_relationship_types()


def add_milestone(milestone, propagate=True):
    """
    Passes a new milestone to the data layer for storage

    Arguments:
        milestone (dict): The milestone to persist
        propagate (bool): False to prevent reactivation of soft-deleted milestone relationships

    Returns:
        dict: The persisted milestone dict
    """
    _validate_milestone_data(milestone)
    milestone = data.create_milestone(milestone, propagate)
    return milestone


def edit_milestone(milestone):
    """
    Passes an updated milestone to the data layer for storage
    """
    _validate_milestone_data(milestone)
    return data.update_milestone(milestone)


def get_milestone(milestone_id):
    """
    Retrieves the specified milestone
    """
    return data.fetch_milestone(milestone_id)


def get_milestones(namespace):
    """
    Retrieves a set of milestones by namespace
    (no other way to really do it right now)
    """
    milestone = {
        'namespace': namespace,
    }
    return data.fetch_milestones(milestone)


def remove_milestone(milestone_id):
    """
    Removes the specified milestone
    """
    milestone = {
        'id': milestone_id,
    }
    data.delete_milestone(milestone)


def add_course_milestone(course_key, relationship, milestone):
    """
    Adds a course-milestone link to the system
    'relationship': string value (eg: 'requires')
    """
    _validate_course_key(course_key)
    _validate_milestone_data(milestone)
    data.create_course_milestone(
        course_key=course_key,
        relationship=relationship,
        milestone=milestone
    )


def get_course_milestones(course_key, relationship=None):
    """
    Retrieves the set of milestones for a given course
    'relationship': optional filter on milestone relationship type (string, eg: 'requires')
    Returns an array of dicts containing milestones
    """
    _validate_course_key(course_key)

    try:
        milestones = data.fetch_courses_milestones(course_keys=[course_key], relationship=relationship)
    except exceptions.InvalidMilestoneRelationshipTypeException:
        milestones = []

    return milestones


def get_course_required_milestones(course_key, user):
    """
    Retrieves the set of required milestones for a given course that a user has not yet collected
    """
    _validate_course_key(course_key)
    _validate_user(user)
    required_milestones = data.fetch_courses_milestones(
        [course_key],
        get_milestone_relationship_types()['REQUIRES'],
        user
    )
    return required_milestones


def get_course_milestones_fulfillment_paths(course_key, user):
    """
    Returns a collection composed of the possible fulfillment/collection options/opportunites
    Inputs:
        course_key: string representation of a CourseKey -- eg, unicode(course.id)
        user: dictionary representation of a User object ('id' field is required)
    Output:
        A complex dict-of-dicts containing the currently-required milestones for the
        specified course+user combo, and the options for collecting them
        (courses and/or content to complete which leads to their fulfillment)
        {
            'milestone_1': {
                'content': [
                    u'i4x://the/content/key/123456789',
                    u'i4x://the/content/key/987654321'
                ]
            },
            'milestone_2': {
                'courses': [
                    u'the/prerequisite/course_key'
                ]
            },
            'milestone_3': {
                'content': [
                    u'i4x://the/content/key/123456789'
                ],
                'courses': [
                    u'the/prerequisite/course_key'
                ]
            }
        }
    """
    _validate_course_key(course_key)
    _validate_user(user)

    # Retrieve the outstanding milestones for this course, for this user
    required_milestones = data.fetch_courses_milestones(
        [course_key],
        get_milestone_relationship_types()['REQUIRES'],
        user
    )

    # Build the set of fulfillment paths for the outstanding milestones
    fulfillment_paths = {}
    for milestone in required_milestones:
        dict_key = '{}.{}'.format(milestone['namespace'], milestone['name'])
        fulfillment_paths[dict_key] = {}
        milestone_courses = data.fetch_milestone_courses(
            milestone,
            get_milestone_relationship_types()['FULFILLS']
        )
        if milestone_courses:
            fulfillment_paths[dict_key]['courses'] = [
                milestone['course_id'] for milestone in milestone_courses]
        milestone_course_content = data.fetch_milestone_course_content(
            milestone,
            get_milestone_relationship_types()['FULFILLS']
        )
        if milestone_course_content:
            fulfillment_paths[dict_key]['content'] = [
                milestone['content_id'] for milestone in milestone_course_content]
    return fulfillment_paths


def get_courses_milestones(course_keys, relationship=None, user=None):
    """
    Retrieves the set of milestones for list of courses
    'relationship': optional filter on milestone relationship type (string, eg: 'requires')
    'user': optional filter to constrain the set to those milestones which a user has already collected
    Returns an array of dicts containing milestones
    """
    [_validate_course_key(course_key) for course_key in course_keys]  # pylint: disable=expression-not-assigned
    try:
        milestones = data.fetch_courses_milestones(
            course_keys=course_keys,
            relationship=relationship,
            user=user
        )
    except exceptions.InvalidMilestoneRelationshipTypeException:
        milestones = []

    return milestones


def remove_course_milestone(course_key, milestone):
    """
    Removes the specfied milestone from the specified course
    """
    _validate_course_key(course_key)
    _validate_milestone_data(milestone)
    return data.delete_course_milestone(course_key=course_key, milestone=milestone)


def add_course_content_milestone(course_key, content_key, relationship, milestone, requirements=None):
    """
    Adds a course-content-milestone link to the system

    Arguments:
        course_key (CourseKey|str): CourseKey of the course containing the content
        content_key (UsageKey|str): UsageKey of the content
        relationship (str): The type of relationship that the content shares with the milestone (e.g. 'requires')
        milestone (dict): The milestone which the given content relates to
        requirements (dict): Data that is used to determine user fulfillment of the milestone

    Returns:
        None
    """
    _validate_course_key(course_key)
    _validate_content_key(content_key)
    _validate_milestone_data(milestone)
    _validate_course_content_milestone_requirements(requirements)
    data.create_course_content_milestone(
        course_key=course_key,
        content_key=content_key,
        relationship=relationship,
        milestone=milestone,
        requirements=requirements
    )


def get_course_content_milestones(course_key=None, content_key=None, relationship=None, user=None):
    """
    Retrieves the set of milestones related to course content

    Arguments:
        course_key (CourseKey|str): CourseKey of the course containing the content
        content_key (UsageKey|str): UsageKey of the content
        relationship (str): The type of relationship that the content shares with the milestone (e.g. 'requires')
        user (dict): Dict containing at least an 'id' key mapped to a user id

    Returns:
        list: List of milestone dicts
    """
    if course_key is not None:
        _validate_course_key(course_key)
    if content_key is not None:
        _validate_content_key(content_key)
    try:
        milestones = data.fetch_course_content_milestones(
            course_key=course_key,
            content_key=content_key,
            relationship=relationship,
            user=user
        )
    except exceptions.InvalidMilestoneRelationshipTypeException:
        milestones = []

    return milestones


def remove_course_content_milestone(course_key, content_key, milestone):
    """
    Removes the specified milestone from the specified course content module
    """
    _validate_course_key(course_key)
    _validate_content_key(content_key)
    _validate_milestone_data(milestone)
    return data.delete_course_content_milestone(
        course_key=course_key,
        content_key=content_key,
        milestone=milestone
    )


def add_user_milestone(user, milestone):
    """
    Adds a new User-Milestone relationship to the system
    """
    _validate_user(user)
    _validate_milestone_data(milestone)
    data.create_user_milestone(user, milestone)


def get_user_milestones(user, namespace):
    """
    Retrieves the set of milestones for a given user
    Returns an array of dicts -- must provide the 'namespace' filter (or else!!!)
    """
    _validate_user(user)
    milestone = {'namespace': namespace}
    return data.fetch_user_milestones(user, milestone)


def user_has_milestone(user, milestone):
    """
    A helper/convenience method to check for a specific user-milestone link
    """
    _validate_user(user)
    _validate_milestone_data(milestone)
    return True if data.fetch_user_milestones(user, milestone) else False


def remove_user_milestone(user, milestone):
    """
    Removes the specified User-Milestone link from the system
    """
    _validate_user(user)
    _validate_milestone_data(milestone)
    return data.delete_user_milestone(user, milestone)


def remove_course_references(course_key):
    """
    Removes course references from application state
    See edx-platform/lms/djangoapps/courseware/management/commands/delete_course_references.py
    """
    _validate_course_key(course_key)
    data.delete_course_references(course_key)


def remove_content_references(content_key):
    """
    Removes content references from application state
    See edx-platform/cms/djangoapps/contentstore/views/entrance_exam.py:_delete_entrance_exam
    """
    _validate_content_key(content_key)
    data.delete_content_references(content_key)

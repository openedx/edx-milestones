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
import milestones.data as data
import milestones.exceptions as exceptions
import milestones.validators as validators


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


def _validate_milestone(milestone):
    """ Validation helper """
    if not validators.milestone_is_valid(milestone):
        exceptions.raise_exception(
            "Milestone",
            milestone,
            exceptions.InvalidMilestoneException
        )


def _validate_milestone_relationship_type(name):
    """ Validation helper """
    if not validators.milestone_relationship_type_is_valid(name):
        exceptions.raise_exception(
            "MilestoneRelationshipType",
            name,
            exceptions.InvalidMilestoneRelationshipTypeException
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
def add_milestone(milestone):
    """
    Passes a new milestone to the data layer for storage
    """
    _validate_milestone(milestone)
    milestone = data.create_milestone(milestone)
    return milestone


def edit_milestone(milestone):
    """
    Passes an updated milestone to the data layer for storage
    """
    _validate_milestone(milestone)
    try:
        return data.update_milestone(milestone)
    except exceptions.InvalidMilestoneException:
        raise


def get_milestone(milestone_id):
    """
    Retrieves the specified milestone
    """
    milestone = {
        'id': milestone_id,
    }
    milestones = data.fetch_milestones(milestone)
    if not len(milestones):
        return None
    return milestones[0]


def get_milestones(namespace):
    """
    Retrieves the specified milestone by namespace
    (no other way to really do it right now)
    """
    milestone = {
        'namespace': namespace,
    }
    _validate_milestone(milestone)
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
    _validate_milestone_relationship_type(relationship)
    _validate_milestone(milestone)
    data.create_course_milestone(course_key=course_key, relationship=relationship, milestone=milestone)


def get_course_milestones(course_key, relationship=None):
    """
    Retrieves the set of milestones for a given course
    'relationship': optional filter on milestone relationship type (string, eg: 'requires')
    Returns an array of dicts containing milestones
    """
    _validate_course_key(course_key)

    if relationship is not None:
        _validate_milestone_relationship_type(relationship)
    return data.fetch_courses_milestones(course_keys=[course_key], relationship=relationship)


def get_course_required_milestones(course_key, user):
    """
    Retrieves the set of required milestones for a given course that a user has not yet collected
    """
    _validate_course_key(course_key)
    _validate_user(user)
    required_milestones = data.fetch_courses_milestones([course_key], 'requires', user)
    return required_milestones


def get_course_milestones_fulfillment_paths(course_key, user):
    """
    Returns a collection composed of the possible fulfillment/collection opportunites
    """
    _validate_course_key(course_key)
    _validate_user(user)
    # Retrieve the outstanding milestones for this course, for this user
    required_milestones = data.fetch_courses_milestones([course_key], 'requires', user)

    # Build the set of fulfillment paths for the outstanding milestones
    fulfillment_paths = {}
    for milestone in required_milestones:
        dict_key = 'milestone_{}'.format(milestone['id'])
        fulfillment_paths[dict_key] = {}
        fulfillment_paths[dict_key]['courses'] = \
            data.fetch_milestone_courses(milestone, 'fulfills')
        fulfillment_paths[dict_key]['content'] = \
            data.fetch_milestone_course_content(milestone, 'fulfills')
    print fulfillment_paths
    return fulfillment_paths


def get_courses_milestones(course_keys, relationship=None, user=None):
    """
    Retrieves the set of milestones for list of courses
    'relationship': optional filter on milestone relationship type (string, eg: 'requires')
    Returns an array of dicts containing milestones
    """
    [_validate_course_key(course_key) for course_key in course_keys]  # pylint: disable=expression-not-assigned

    if relationship is not None:
        _validate_milestone_relationship_type(relationship)

    return data.fetch_courses_milestones(
        course_keys=course_keys,
        relationship=relationship,
        user=user)


def remove_course_milestone(course_key, milestone):
    """
    Removes the specfied milestone from the specified course
    """
    _validate_course_key(course_key)
    _validate_milestone(milestone)
    return data.delete_course_milestone(course_key=course_key, milestone=milestone)


def add_course_content_milestone(course_key, content_key, relationship, milestone):
    """
    Adds a course-content-milestone link to the system
    'relationship': string value (eg: 'requires')
    """
    _validate_course_key(course_key)
    _validate_content_key(content_key)
    _validate_milestone_relationship_type(relationship)
    _validate_milestone(milestone)
    data.create_course_content_milestone(
        course_key=course_key,
        content_key=content_key,
        relationship=relationship,
        milestone=milestone)


def get_course_content_milestones(course_key, content_key, relationship=None):
    """
    Retrieves the set of milestones for a given course module
    'relationship': optional filter on milestone relationship type (string, eg: 'requires')
    Returns an array of dicts containing milestones
    """
    _validate_course_key(course_key)
    _validate_content_key(content_key)

    if relationship is not None:
        _validate_milestone_relationship_type(relationship)

    return data.fetch_course_content_milestones(
        course_key=course_key,
        content_key=content_key,
        relationship=relationship
    )


def remove_course_content_milestone(course_key, content_key, milestone):
    """
    Removes the specfied milestone from the specified course module
    """
    _validate_course_key(course_key)
    _validate_content_key(content_key)
    _validate_milestone(milestone)
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
    _validate_milestone(milestone)
    data.create_user_milestone(user, milestone)


def get_user_milestones(user):
    """
    Retrieves the set of milestones for a given user
    Returns an array of dicts
    """
    _validate_user(user)
    return data.fetch_user_milestones(user)


def remove_user_milestone(user, milestone):
    """
    Removes the specified User-Milestone link from the system
    """
    _validate_user(user)
    _validate_milestone(milestone)
    return data.delete_user_milestone(user, milestone)


def user_has_milestone(user, milestone):
    """
    A helper/convenience method to check for a specific user-milestone link
    """
    _validate_user(user)
    _validate_milestone(milestone)
    return len(data.fetch_user_milestones(user, milestone))


def remove_course_references(course_key):
    """
    Removes orphaned course references from application state
    See lms/djangoapps/courseware/management/commands/delete_course_references.py
    """
    _validate_course_key(course_key)
    data.delete_course_references(course_key)

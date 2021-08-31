edx-milestones [![Build Status](https://github.com/edx/edx-milestones/workflows/Python%20CI/badge.svg?branch=master)](https://github.com/edx/edx-milestones/actions?query=workflow%3A%22Python+CI%22) [![Coverage Status](https://img.shields.io/coveralls/edx/edx-milestones.svg)](https://coveralls.io/r/edx/edx-milestones?branch=master)
===================

edx-milestones (`milestones`) is a Django application which manages significant Course and/or Student events in the Open edX platform.

Usage
-----
*  A Milestone represents an event which can occur for a student while interacting with the Open edX platform.

*  Relationships can be created between courses or individual sections of course content (referred to collectively as course entities going forward) and a Milestone. A relationship can indicate that a course entity either requires or fulfills a given Milestone.

*  Student milestone fulfillment status can be recorded and queried.

*  An example feature which Milestones supports is Pre-requisite Courses:
    * Course author selects Course 101 in Studio as a pre-requisite of Course 102
        * Studio:
            * Makes call to Milestones service API
        * Milestones:
            * Creates a new generic Milestone A for Course 101
            * Indicates that Course 101 fulfills Milestone A
            * Indicates that Course 102 requires Milestone A
    * Student Smith completes Course 101
        * LMS:
            * Makes call to Milestones service API
        * Milestones:
            * Pulls the list of milestones fulfilled by Course 101 (set includes Milestone A)
            * Indicates that Student Smith has accomplished Milestone A
    * Student Smith attempts to access Course 102
        * LMS:
            * Uses Milestones service API to compare Course 102 milestone requirements against Student Smith's milestones
            * Grants Student Smith access to Course 102

Standalone Testing and Quality Check
------------------------------------

        $ make quality
        $ make test

Open edX Platform Integration
-----------------------------
* This package is included in the [base](https://github.com/edx/edx-platform/blob/master/requirements/edx/base.in#L85) requirements of [edx-platform](https://github.com/edx/edx-platform/)
* `milestones` is included in the list of installed apps for edx-platform:
* These documents outline the feature flags required to enable the features that use edx-milestones.
  * [Course Run prerequisites](https://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/configuration/enable_prerequisites.html#enable-course-prerequisites)
  * [Subsection prerequisites](https://edx-partner-course-staff.readthedocs.io/en/latest/developing_course/controlling_content_visibility.html#prerequisite-course-subsections)


How to Contribute
-----------------
Contributions are very welcome please see our
[CONTRIBUTING](https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst)
file for more information -- it also contains guidelines for how to maintain
high code quality, which will make your contribution more likely to be accepted.

Getting Help
------------
If you're having trouble, we have discussion forums at
https://discuss.openedx.org where you can connect with others in the community.

Our real-time conversations are on Slack. You can request a [Slack
invitation](https://openedx-slack-invite.herokuapp.com/), then join our [community Slack team](http://openedx.slack.com/).

For more information about these options, see the [Getting Help](https://openedx.org/getting-help) page.

Reporting Security Issues
-------------------------
Please do not report security issues in public. Please email security@edx.org.

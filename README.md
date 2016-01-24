edx-milestones [![Build Status](https://travis-ci.org/edx/edx-milestones.svg?branch=master)](https://travis-ci.org/edx/edx-milestones) [![Coverage Status](https://img.shields.io/coveralls/edx/edx-milestones.svg)](https://coveralls.io/r/edx/edx-milestones?branch=master)
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
* Add desired tag from github code repository
    * edx-platform/requirements/github.txt
    * "Our libraries" section
* Add 'milestones' to the list of installed apps:
    * common.py
    * Feature flag convention is preferred
* In edx-platform devstack:
    * pip install -r requirements
    * paver test_system -s lms


How to Contribute
-----------------
Contributions are very welcome, but please note that edx-milestones is currently an
early stage work-in-progress and is changing frequently at this time.

See our
[CONTRIBUTING](https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst)
file for more information -- it also contains guidelines for how to maintain
high code quality, which will make your contribution more likely to be accepted.


Reporting Security Issues
-------------------------
Please do not report security issues in public. Please email security@edx.org.


Mailing List and IRC Channel
----------------------------
You can discuss this code on the [edx-code Google Group](https://groups.google.com/forum/#!forum/edx-code) or in the
`edx-code` IRC channel on Freenode.

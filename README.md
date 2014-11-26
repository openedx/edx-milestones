edx-milestones [![Build Status](https://travis-ci.org/edx/edx-milestones.svg?branch=master)](https://travis-ci.org/edx/edx-milestones) [![Coverage Status](https://coveralls.io/repos/edx/edx-milestones/badge.png?branch=master)](https://coveralls.io/r/edx/edx-milestones?branch=master)
===================

edx-milestones (`milestones`) is a Django application which manages significant Course and/or Student events in the Open edX platform.

Usage
-----
*  Milestones was originally designed to support the use case for 'pre-requisite courses'.  Rather than simply linking two courses together, the edX team took the opportunity to create a more flexible feature which could cover multiple scenarios going forward.

*  Milestones listens for Django system events (signals), such as 'added a prerequisite course' and modifies its internal state/models accordingly.  Signals can be defined/emitted from any location in Open edX.  Specific event listeners can be found in receivers.py.  In addition, a read-specific query interface is available in api.py for integration into platform views and other apps.

*  Milestones supports the 'pre-requisite course' use case in the following way:
    * Course author selects Course 101 in Studio as a pre-requisite of Course 102
        * Studio: 
            * Emits an 'added_course_prerequisite_course' signal
        * Milestones:
            * Observes the signal
            * Creates a new generic Milestone A for Course 101
            * Indicates that Course 101 fulfills Milestone A
            * Indicates that Course 102 requires Milestone A
    * Student Smith completes Course 101
        * LMS:
            * Emits a 'course_completed' signal
        * Milestones:
            * Observes the signal
            * Pulls the list of milestones fulfilled by Course 101 (set includes Milestone A)
            * Indicates that Student Smith has accomplished Milestone A
    * Student Smith attempts to access Course 102
        * LMS:
            * Compares Course 102 milestone requirements against Student Smith's milestones
            * Grants Student Smith access to Course 102

Standalone Testing
------------------

        $ ./run_tests


Open edX Platform Integration
-----------------------------
* Add desired commit hash from github code repository
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

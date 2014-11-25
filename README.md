edx-milestones [![Build Status](https://travis-ci.org/edx/edx-milestones.svg?branch=master)](https://travis-ci.org/edx/edx-milestones) [![Coverage Status](https://coveralls.io/repos/edx/edx-milestones/badge.png?branch=master)](https://coveralls.io/r/edx/edx-milestones?branch=master)
===================

edx-milestones (`milestones`) is a Django application which manages significant Course and/or Student events in the Open edX platform.

Usage
-----
*  Milestones was originally designed to support the use case for 'pre-requisite courses'.  Rather than simply linking two courses together, the edX team took the opportunity to create a more flexible feature which could cover multiple scenarios going forward.
*  Milestones listens for Django system events (signals), such as 'added a prerequisite course' and modifies its internal state/models accordingly.  Event listeners can be found in receivers.py.  In addition, a read-specific query interface is available in api.py for integration into platform views and other apps.

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

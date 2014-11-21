"""
Application data management/abstraction layer.  Responsible for:

1) Accessing information/state from internal and external resources
* Internal app models  (through models.py)
* External app models  (through direct ORM integrations, yuck)
* Remote data services (through resources.py)

2) Calculating derivative information from existing state
* Algorithms and data manipulations
* Aggregations
* Annotations
* Alternative data representations

Returns standard Python data structures for easy consumption by callers
"""

from django.dispatch import Signal

# MOCK SIGNALS USED FOR STANDALONE TESTING
course_deleted = Signal(providing_args=["course_key"])


### THESE TWO SIGNALS ARE NOW OBSOLETE ###
course_prerequisite_course_added = Signal(providing_args=["course_key", "prerequisite_course_key", "milestone"])
course_prerequisite_course_removed = Signal(providing_args=["course_key", "prerequisite_course_key"])

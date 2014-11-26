from django.dispatch import Signal

# MOCK SIGNALS USED FOR STANDALONE TESTING
course_completed = Signal(providing_args=["course_key", "student"])
course_deleted = Signal(providing_args=["course_key"])
course_entrance_exam_added = Signal(providing_args=["course_key", "content_key", "milestone"])
course_prerequisite_course_added = Signal(providing_args=["course_key", "prerequisite_course_key", "milestone"])
course_prerequisite_course_removed = Signal(providing_args=["course_key", "prerequisite_course_key"])

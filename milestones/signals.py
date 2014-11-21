from django.dispatch import Signal

# SIGNAL MOCKS USED FOR TESTING
course_completed(providing_args=["course", "student"])
course_deleted(providing_args=["course"])
course_entrance_exam_added(providing_args=)
course_prequisite_course_added(providing_args=["course", "prerequisite_course"])

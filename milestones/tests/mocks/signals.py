from django.dispatch import Signal

# MOCK SIGNALS USED FOR STANDALONE TESTING
course_deleted = Signal(providing_args=["course_key"])

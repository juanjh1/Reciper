from .models import ClassSpace

def create_class_space(space_type, day, start_time, end_time):
    new_class_space = ClassSpace(space_type=space_type, day=day, start_time=start_time, end_time=end_time)
    new_class_space.save()
    return new_class_space

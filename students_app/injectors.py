from config.filenames import STUDENT_FILENAME, COURSE_FILENAME, ENROLLMENT_FILENAME
from course.course_manager import CourseManager
from course.course_repository import CourseRepository
from enrollment.enrollment_manager import EnrollmentManager
from enrollment.enrollment_repository import EnrollmentRepository
from student.student_repository import StudentRepository
from student.students_manager import StudentManager


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class RepositoryInjectors(metaclass=SingletonMeta):
    student_repository = StudentRepository(STUDENT_FILENAME)
    course_repository = CourseRepository(COURSE_FILENAME)
    enrollment_repository = EnrollmentRepository(ENROLLMENT_FILENAME)

class ManagerInjectors(metaclass=SingletonMeta):
    repository_injectors = RepositoryInjectors()
    student_manager = StudentManager(repository_injectors.student_repository)
    course_manager = CourseManager(repository_injectors.course_repository)
    enrollment_manager = EnrollmentManager(
        course_manager,
        student_manager,
        repository_injectors.enrollment_repository
    )
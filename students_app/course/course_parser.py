from config.ids import COURSE_ID_PREFIX
from course.course import Course
from inputs import Inputs

class CourseParser:
    @staticmethod
    def from_course_to_dict(course: Course) -> dict:
        return {
            "id": course.course_id,
            "description": course.description,
            "max_students": course.max_students,
        }

    @staticmethod
    def from_dict_to_course(course: dict) -> Course:
        return Course(
            course_id=course['id'],
            description=course['description'],
            max_students=course['max_students'],
        )

class CourseFactory:
    @staticmethod
    def create_course(last_db_course_id: str) -> Course:
        course_id = f'{COURSE_ID_PREFIX}{last_db_course_id}'
        description = Inputs.get_non_empty_input("Cual es la descripcion del curso: ")
        max_students = Inputs.get_valid_number("Cual es la cantidad de maxima de matriculas: ")
        return Course(
            course_id,
            description,
            max_students,
        )
from config.ids import COURSE_ID_PREFIX
from course.course import Course
from inputs import Inputs


class CourseFactory:
    @staticmethod
    def create_course(last_course_db_id: str) -> Course:
        print("\n--------- Agregando Curso -------------")
        description = Inputs.get_non_empty_input("Descripcion del curso: ")
        max_students_for_course = Inputs.get_valid_number("Cual es el maximo de estudiantes en el curso?: ")

        course_id = f'{COURSE_ID_PREFIX}{last_course_db_id}'

        return Course(
            course_id,
            description,
            max_students_for_course,
        )
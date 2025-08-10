from enrollment.enrollment import Enrollment
from inputs import Inputs

class EnrollmentFactory:
    @staticmethod
    def create_enrollment() -> Enrollment:
        print("\n--------- Matriculando Estudiante -------------")
        student_id = Inputs.get_non_empty_input("Cual es el ID del estudiante: ")
        course_id = Inputs.get_non_empty_input("Cual es el ID del curso: ")
        return Enrollment(student_id, course_id)
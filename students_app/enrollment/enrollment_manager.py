from typing import Optional

from course.course_manager import CourseManager
from enrollment.enrollment import Enrollment
from enrollment.enrollment_repository import EnrollmentRepository
from enrollment.enrollment_validator import EnrollmentValidator
from student.students_manager import StudentManager

class EnrollmentManager:
    def __init__(
            self,
            course_manager: CourseManager,
            student_manager: StudentManager,
            enrollment_repository: EnrollmentRepository,
    ):
        self.course_manager = course_manager
        self.student_manager = student_manager
        self.enrollment_repository = enrollment_repository
        self.enrollments = []
        self.load_data()

    def enroll_student(self, student_id: str, course_id: str) -> Optional[Enrollment]:
        student = self.student_manager.get_student_by_id(student_id)
        course = self.course_manager.get_course(course_id)
        if course is None or student is None:
            print("Curso o estudiante no se encuentra registrados en nuestra base de datos.")
            return None
        if EnrollmentValidator.validate_student_has_not_enrolled_to_course(
                student,
                course,
                self.enrollments
        ):
            print("El estudiante ya se encuentra matriculado en el curso.")
            return None
        if EnrollmentValidator.validate_course_available(
                course,
                self.enrollment_repository.get_enrollments_by_course_id(course_id)
        ):
            print("EL curso ya no se encuentra habilitado para matricular.")
            return None
        return Enrollment(student_id, course_id)

    def save_enrollment(self, enrollment: Enrollment):
        self.enrollments.append(enrollment)
        self.save_data()
        print("El estudiante ha sido matriculado!")

    def save_data(self):
        self.enrollment_repository.save_enrollments(self.enrollments)
        self.load_data()

    def load_data(self):
        self.enrollments = self.enrollment_repository.get_enrollments()


    def show_enrollments(self):
        if not self.enrollments:
            print("No hay matriculas actualmente.")
            return

        for enrollment in self.enrollments:
            student = self.student_manager.get_student_by_id(enrollment.student_id)
            course = self.course_manager.get_course(enrollment.course_id)
            if course is None or student is None:
                continue
            print(f"Curso {course.course_id} - {course.description}. Estudiante: {student.name} {student.last_name}.")


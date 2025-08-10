from course.course import Course
from enrollment.enrollment import Enrollment
from typing import List

from student.student import Student


class EnrollmentValidator:
    @staticmethod
    def validate_course_available(course: Course, course_enrollments: List[Enrollment]) -> bool:
        return course.validate_new_student(len(course_enrollments))

    @staticmethod
    def validate_student_has_not_enrolled_to_course(
            student: Student,
            course: Course,
            course_enrollments: List[Enrollment]
    ) -> bool:
        enrollment = Enrollment(student.student_id, course.course_id)
        for course_enrollment in course_enrollments:
            if course_enrollment == enrollment:
                return True
        return False


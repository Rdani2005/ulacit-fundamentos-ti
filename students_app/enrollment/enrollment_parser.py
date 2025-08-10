from enrollment.enrollment import Enrollment

class EnrollmentParser:
    @staticmethod
    def enrollment_to_dict(enrollment: Enrollment) -> dict:
        return {
            'student_id': enrollment.student_id,
            'course_id': enrollment.course_id,
        }

    @staticmethod
    def dict_to_enrollment(enrollment: dict) -> Enrollment:
        return Enrollment(enrollment['student_id'], enrollment['course_id'])
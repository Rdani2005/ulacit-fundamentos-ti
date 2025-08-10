import os
import json

from typing import List
from enrollment.enrollment import Enrollment
from enrollment.enrollment_parser import EnrollmentParser


class EnrollmentRepository:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def save_enrollments(self, enrollments: List[Enrollment]) -> None:
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([EnrollmentParser.enrollment_to_dict(enrollment) for enrollment in enrollments], f, indent=4)

    def get_enrollments(self) -> List[Enrollment]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [EnrollmentParser.dict_to_enrollment(enrollment) for enrollment in data]

    def get_enrollments_by_course_id(self, course_id: str) -> List[Enrollment]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            enrollments = [EnrollmentParser.dict_to_enrollment(enrollment) for enrollment in data]
            return [enrollment for enrollment in enrollments if enrollment.course_id == course_id]

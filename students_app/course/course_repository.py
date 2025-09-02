import json
import os

from typing import List, Optional
from course.course import Course
from course.course_parser import CourseParser


class CourseRepository:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def save_courses(self, courses: List[Course]) -> None:
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([CourseParser.from_course_to_dict(course) for course in courses], f, indent=4)

    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            courses = [CourseParser.from_dict_to_course(course) for course in data]
            for course in courses:
                if course.course_id == course_id:
                    return course
            return None

    def get_courses(self) -> List[Course]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [CourseParser.from_dict_to_course(course) for course in data]


    def get_last_course_id(self) -> str:
        if not os.path.exists(self.filename):
            return "000"
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not data:
                return "000"
            return data[-1]['id']
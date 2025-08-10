from typing import List, Optional

from config.ids import COURSE_ID_PREFIX
from course.course import Course
from course.course_repository import CourseRepository


class CourseManager:
    @property
    def courses(self) -> List[Course]:
        return self.__courses

    def __init__(self, course_repository: CourseRepository) -> None:
        self.__course_repository = course_repository
        self.__courses: List[Course] = []
        self.load_data()

    def load_data(self) -> None:
        self.__courses = self.__course_repository.get_courses()

    def get_course(self, id: str) -> Optional[Course]:
        return self.__course_repository.get_course_by_id(id)

    def add_course(self, course: Course) -> None:
        self.__courses.append(course)
        self.save_data()

    def save_data(self) -> None:
        self.__course_repository.save_courses(self.__courses)
        self.load_data()

    def build_new_course_id(self) -> str:
        last_student_id = self.__course_repository.get_last_course_id()
        return str(
            int(last_student_id.replace(COURSE_ID_PREFIX, "")) + 1
        ).zfill(3)

    def show_all_courses(self) -> None:
        if not self.__courses:
            print('No hay cursos disponibles.')
            return

        for course in self.__courses:
            print(course)
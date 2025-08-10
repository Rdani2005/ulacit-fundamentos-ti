from typing import List, Optional

from config.ids import STUDENT_ID_PREFIX
from student.student import Student
from student.student_repository import StudentRepository

class StudentManager(object):
    def __init__(self, student_repository: StudentRepository) -> None:
        self.__student_repository = student_repository
        self.__students: List[Student] = []
        self.load_data()

    def get_student_by_id(self, id: str) -> Optional[Student]:
        return self.__student_repository.get_student_by_id(id)

    def add_student(self, student: Student) -> None:
        self.__students.append(student)
        self.save_data()

    def show_students(self) -> None:
        if not self.__students:
            print('No students')
            return

        for student in self.__students:
            print(student)

    def save_data(self) -> None:
        self.__student_repository.save_students(self.__students)
        self.load_data()

    def load_data(self) -> None:
         self.__students = self.__student_repository.get_students()

    def build_new_student_id(self) -> str:
        last_student_id = self.__student_repository.get_last_student_id()
        return str(
            int(last_student_id.replace(STUDENT_ID_PREFIX, "")) + 1
        ).zfill(3)
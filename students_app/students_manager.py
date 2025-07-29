import json
import os
from typing import List

from student import Student, StudentParser

class StudentManager(object):
    def __init__(self, filename: str) -> None:
        self.__student_repository = StudentRepository(filename)
        self.__students: List[Student] = []
        self.load_data()

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

class StudentRepository:
    @property
    def filename(self) -> str:
        return self.__filename

    def __init__(self, filename: str) -> None:
        self.__filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def save_students(self, students: List[Student]) -> None:
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([StudentParser.from_student_to_dict(student) for student in students], f, indent=4)

    def get_students(self) -> List[Student]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [StudentParser.from_dict_to_student(student) for student in data]
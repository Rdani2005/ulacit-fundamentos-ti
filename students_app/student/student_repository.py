import os
import json

from typing import List, Optional

from student.student_parser import StudentParser
from student.student import Student

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

    def get_last_student_id(self) -> str:
        if not os.path.exists(self.filename):
            return "000"
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data[-1]['id']

    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            students = [StudentParser.from_dict_to_student(student) for student in data]
            for student in students:
                if student.student_id == student_id:
                    return student
            return None
from student.student import Student

class StudentParser:
    @staticmethod
    def from_dict_to_student(data: dict) -> Student:
        return Student(
            student_id=data['id'],
            name=data['name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            email=data['email'],
        )

    @staticmethod
    def from_student_to_dict(student: Student) -> object:
        return {
            'id': student.student_id,
            'name': student.name,
            'last_name': student.last_name,
            'phone_number': student.phone_number,
            'email': student.email,
        }


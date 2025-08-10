from config.ids import STUDENT_ID_PREFIX
from inputs import Inputs
from student.student import Student

class StudentFactory:
    @staticmethod
    def create_student(last_db_student_id: str) -> Student:
        print("\n--------- Agregando Estudiante -------------")
        name = Inputs.get_non_empty_input("Nombre del estudiante: ")
        last_name = Inputs.get_non_empty_input("Apellido del estudiante: ")
        phone_number = Inputs.get_non_empty_input("Numero del estudiante: ")
        email = Inputs.get_non_empty_input("Email del estudiante: ")
        address = Inputs.get_non_empty_input("Direccion del estudiante: ")
        student_id = f'{STUDENT_ID_PREFIX}{last_db_student_id}'

        return Student(
            student_id,
            name,
            last_name,
            phone_number,
            email,
            address
        )
from inputs import Inputs
from student.student import Student

class StudentFactory:
    """
    Factory class responsible for creating `Student` objects.

    This class handles user input to collect student information
    and returns a fully initialized `Student` instance.

    Methods
    -------
    create_student(last_db_student_id: int) -> Student
        Prompts the user for student details and returns a new Student instance.
    """
    @staticmethod
    def create_student(last_db_student_id: int) -> Student:
        """
        Prompt the user for student details and create a Student instance.

        Parameters
        ----------
        last_db_student_id : int
            The ID to assign to the new student. Usually the next available
            ID based on the database or repository.

        Returns
        -------
        Student
            A new Student object populated with user-provided data.

        Notes
        -----
        - Uses `Inputs.get_non_empty_input` to ensure no empty fields.
        - The student ID is assigned from the provided `last_db_student_id`.

        Example
        -------
        >>> new_student = StudentFactory.create_student(5)
        --------- Adding Student -------------
        Nombre del estudiante: John
        Apellido del estudiante: Doe
        Numero del estudiante: 12345678
        Email del estudiante: john.doe@email.com
        >>> print(new_student)
        ID: 5 - Name: John Doe - Phone: 12345678 - Email: john.doe@email.com
        """
        print("\n--------- Agregando Estudiante -------------")
        name = Inputs.get_non_empty_input("Nombre del estudiante: ")
        last_name = Inputs.get_non_empty_input("Apellido del estudiante: ")
        phone_number = Inputs.get_non_empty_input("Numero del estudiante: ")
        email = Inputs.get_non_empty_input("Email del estudiante: ")
        student_id = last_db_student_id

        return Student(
            student_id,
            name,
            last_name,
            phone_number,
            email
        )
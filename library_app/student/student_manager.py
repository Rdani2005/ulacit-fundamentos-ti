from typing import List, Optional

from student.student import Student
from student.student_repository import StudentRepository

class StudentManager(object):
    """
    Manages the collection of Student objects in memory
    and coordinates persistence with a StudentRepository.

    Attributes
    ----------
    __student_repository : StudentRepository
        Repository used for reading and writing student data to persistent storage.
    __students : List[Student]
        In-memory list of Student objects.

    Methods
    -------
    get_student_by_id(id: str) -> Optional[Student]
        Retrieve a student from the repository by their ID.
    add_student(student: Student) -> None
        Add a new student to the in-memory list and persist changes.
    show_students() -> None
        Display the list of students in memory.
    save_data() -> None
        Persist the in-memory list to the repository and reload it.
    load_data() -> None
        Load students from the repository into memory.
    build_new_student_id() -> int
        Generate a new unique student ID based on the last ID in the repository.
    """
    def __init__(self, student_repository: StudentRepository) -> None:
        """
           Initialize the StudentManager with a StudentRepository.

           Parameters
           ----------
           student_repository : StudentRepository
               The repository used for persistent storage operations.
           """
        self.__student_repository = student_repository
        self.__students: List[Student] = []
        self.load_data()

    def get_student_by_id(self, id: int) -> Optional[Student]:
        """
        Retrieve a student from the repository by their ID.

        Parameters
        ----------
        id : str
            The ID of the student to retrieve.

        Returns
        -------
        Optional[Student]
            The Student instance if found, otherwise None.
        """
        return self.__student_repository.get_student_by_id(id)

    def add_student(self, student: Student) -> None:
        """
         Add a new student to the in-memory list and save changes.

         Parameters
         ----------
         student : Student
             The student to add.
         """
        self.__students.append(student)
        self.save_data()
        print("El estudiante ha sido agregado correctamente.")

    def show_students(self) -> None:
        """
        Print all students in the in-memory list to the console.

        Notes
        -----
        - If there are no students, prints "No students".
        """
        if not self.__students:
            print('No students')
            return

        for student in self.__students:
            print(student)

    def save_data(self) -> None:
        """
        Persist the current in-memory student list to the repository
        and reload the data into memory.
        """
        self.__student_repository.save_students(self.__students)
        self.load_data()

    def load_data(self) -> None:
        """
        Load the list of students from the repository into memory.
        """
        self.__students = self.__student_repository.get_students()

    def build_new_student_id(self) -> int:
        """
        Generate a new student ID by incrementing the repository's last ID.

        Returns
        -------
        int
            A unique student ID for a new entry.
        """
        last_student_id = self.__student_repository.get_last_student_id()
        return last_student_id + 1
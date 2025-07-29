from student import StudentFactory, Student
from inputs import Inputs
from students_manager import StudentManager

FILE_NAME = "data/students.txt"

class Main:
    def __init__(self):
        self.__students_manager = StudentManager(FILE_NAME)

    def add_student(self):
        student: Student = StudentFactory.create_student()
        self.__students_manager.add_student(student)

    def show_students(self):
        self.__students_manager.show_students()

    def exit_application(self):
        print("Saliendo...")
        exit(0)

    def menu(self):
        print("\n------- Menu Principal ------")
        print("1.Add student")
        print("2.Show students")
        print("3.Exit")
        option = Inputs.get_valid_number("Seleccione una opcion: ")
        if option == 1:
            self.add_student()
        elif option == 2:
            self.show_students()
        elif option == 3:
            self.exit_application()
        else:
            print("Opcion invalida. Intente nuevamente.")
        self.menu()

Main().menu()
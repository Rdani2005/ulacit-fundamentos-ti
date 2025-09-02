from book.book_factory import BookFactory
from book.book_manager import BookManager
from inputs import Inputs
from loan.loan_manager import LoanManager
from student import student_manager
from student.student_factory import StudentFactory
from student.student_manager import StudentManager


class Menu:
    loan_manager: LoanManager
    book_manager: BookManager
    student_manager: StudentManager
    def __init__(self, loan_manager: LoanManager, book_manager: BookManager, student_manager: StudentManager):
        self.loan_manager = loan_manager
        self.book_manager = book_manager
        self.student_manager = student_manager

    def add_student(self):
        student_id = self.student_manager.build_new_student_id()
        student = StudentFactory.create_student(student_id)
        self.student_manager.add_student(student)

    def add_book(self):
        book_id = self.book_manager.build_new_book_id()
        book = BookFactory.create_book(book_id)
        self.book_manager.add_book(book)

    def show_students(self):
        self.student_manager.show_students()

    def show_books(self):
        self.book_manager.show_books()

    def show_loans(self):
        self.loan_manager.show_current_loans()

    def create_loan(self):
        self.loan_manager.create_loan()

    def menu(self):
        print("\n")
        print("===================================")
        print("|--------- Menu Principal --------|")
        print("===================================")
        print("1. Agregar Estudiante")
        print("2. Mostrar Estudiantes")
        print("3. Agregar Libro")
        print("4. Mostrar Libros")
        print("5. Realizar un Prestamo")
        print("6. Mostrar Prestamos")
        print("7. Salir")

        option = Inputs.get_valid_number("Seleccione una opcion: ")
        if option == 1:
            self.add_student()
        elif option == 2:
            self.show_students()
        elif option == 3:
            self.add_book()
        elif option == 4:
            self.show_books()
        elif option == 5:
            self.create_loan()
        elif option == 6:
            self.show_loans()
        elif option == 7:
            exit(0)
        else:
            print("Opcion no valida. Intente de nuevo")
        self.menu()

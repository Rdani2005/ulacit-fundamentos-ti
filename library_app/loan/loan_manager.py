import datetime

from book.book_manager import BookManager
from inputs import Inputs
from loan.loan_repository import LoanRepository
from typing import List
from loan.loan import Loan
from student.student_manager import StudentManager


class LoanManager:
    loan_repository: LoanRepository
    book_manager: BookManager
    student_manager: StudentManager
    loans: List[Loan]

    def __init__(self, loan_repository: LoanRepository, book_manager: BookManager, student_manager: StudentManager) -> None:
        self.loans = []
        self.book_manager = book_manager
        self.student_manager = student_manager
        self.loan_repository = loan_repository
        self.load_data()

    def create_loan(self):
        student_id = Inputs.get_valid_number("Cual es el ID del estudiante: ")
        student = self.student_manager.get_student_by_id(student_id)
        if student is None:
            print("No se encontro el estudiante")
            return
        book_id = Inputs.get_valid_number("Cual es el ID del libro: ")
        book = self.book_manager.get_book_by_id(book_id)
        if book is None or book.available == False:
            print("No se encontro el libro o no se encuentra disponible.")
            return
        loan = Loan(
            self.build_loan_id(),
            student_id,
            book_id,
            datetime.datetime.now(),
            datetime.datetime.now() + datetime.timedelta(days=10),
        )
        self.loans.append(loan)
        self.save_data()
        self.book_manager.deactivate_book(book.id)
        print("El prestamo se ha hecho correctamente.")


    def show_current_loans(self):
        if len(self.loans) == 0:
            print("No hay prestamos activos.")
            return

        print("|============================================================================================|")
        print("|                                        Prestamos Activos                                   |")
        print("=============================================================================================|")
        print("|     id     |     estudiante     |     libro     |     fecha     |     fecha devolucion     |")
        for loan in self.loans:
            student = self.student_manager.get_student_by_id(loan.student_id)
            book = self.book_manager.get_book_by_id(loan.book_id)
            if book is None or student is None:
                continue
            print(f"| {loan.id} | {student.name} | {book.title} | {loan.date} | {loan.return_date} |")

    def load_data(self) -> None:
        self.loans = self.loan_repository.get_loans()

    def save_data(self) -> None:
        self.loan_repository.save_loans(self.loans)
        self.load_data()

    def build_loan_id(self) -> int:
        if len(self.loans) == 0:
            return 1
        return self.loans[-1].id + 1
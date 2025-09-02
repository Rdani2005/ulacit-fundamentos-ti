from datetime import datetime

from loan.loan import Loan

class LoanParser:
    @staticmethod
    def loan_to_dict(loan: Loan) -> object:
        return {
            "id": loan.id,
            "book_id": loan.book_id,
            "date": loan.date.isoformat(),
            "return_date": loan.return_date.isoformat(),
            "student_id": loan.student_id,
        }

    @staticmethod
    def dict_to_loan(loan_dict: dict) -> Loan:
        return Loan(
            int(loan_dict["id"]),
            int(loan_dict["student_id"]),
            int(loan_dict["book_id"]),
            datetime.fromisoformat(loan_dict["date"]),
            datetime.fromisoformat(loan_dict["return_date"]),
        )
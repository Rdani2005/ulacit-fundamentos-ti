from typing import List
from loan.loan import Loan
from loan.loan_parser import LoanParser
import os
import json

class LoanRepository:
    filename: str

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def get_loans(self) -> List[Loan]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [LoanParser.dict_to_loan(loan) for loan in data]

    def save_loans(self, loans: List[Loan]) -> None:
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([LoanParser.loan_to_dict(loan) for loan in loans], f, indent=4)

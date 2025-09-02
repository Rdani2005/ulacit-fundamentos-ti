from datetime import datetime


class Loan:
    id: int
    student_id: int
    book_id: int
    date: datetime
    return_date: datetime

    def __init__(self, id: int, student_id: int, book_id: int, date: datetime, return_date: datetime):
        self.id = id
        self.student_id = student_id
        self.book_id = book_id
        self.date = date
        self.return_date = return_date



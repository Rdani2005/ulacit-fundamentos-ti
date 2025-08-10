class Enrollment:
    @property
    def student_id(self):
        return self.__student_id

    @property
    def course_id(self):
        return self.__course_id

    def __init__(self, student_id: str, course_id: str) -> None:
        self.__student_id = student_id
        self.__course_id = course_id

    def __eq__(self, other):
        if isinstance(other, Enrollment):
            return self.__student_id == other.__student_id and self.__course_id == other.__course_id
        return False
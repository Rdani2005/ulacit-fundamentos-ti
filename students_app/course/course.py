class Course:
    @property
    def description(self) -> str:
        return self.__description

    @property
    def course_id(self) -> str:
        return self.__id

    @property
    def max_students(self) -> int:
        return self.__max_students

    def __init__(self,
                 course_id: str,
                description: str,
                max_students: int
        ) -> None:
        self.__id = course_id
        self.__description = description
        self.__max_students = max_students

    def validate_new_student(self, current_enrollment_amounts: int) -> bool:
        return current_enrollment_amounts >= self.__max_students

    def __str__(self):
        return f'ID del curso: {self.course_id} - descripcion: {self.description} - maximo de matriculas: {self.__max_students}'

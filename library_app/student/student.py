class Student:
    """
    Represents a student with personal and contact information.

    Attributes
    ----------
    __id : int
        Unique identifier for the student.
    __name : str
        First name of the student.
    __last_name : str
        Last name of the student.
    __phone_number : str
        Student's phone number.
    __email : str
        Student's email address.

    Methods
    -------
    __init__(student_id, name, last_name, phone_number, email, address)
        Initialize a Student instance with the provided data.
    __str__()
        Return a formatted string representation of the student.
    """
    @property
    def student_id(self) -> int:
        return self.__id
    @property
    def name(self) -> str:
        return self.__name
    @property
    def last_name(self) -> str:
        return self.__last_name
    @property
    def phone_number(self) -> str:
        return self.__phone_number
    @property
    def email(self) -> str:
        return self.__email

    def __init__(self,
                 student_id: int,
                 name: str,
                 last_name: str,
                 phone_number: str,
                 email: str
                 ) -> None:
        """
        Initialize a Student instance.

        Parameters
        ----------
        student_id : int
            Unique identifier for the student.
        name : str
            First name of the student.
        last_name : str
            Last name of the student.
        phone_number : str
            Phone number of the student.
        email : str
            Email address of the student.
        address : str
            Physical address of the student.
        """
        self.__id = student_id
        self.__name = name
        self.__last_name = last_name
        self.__phone_number = phone_number
        self.__email = email


    def __str__(self) -> str:
        """
        Return a formatted string representation of the student.

        Returns
        -------
        str
            Formatted string with all student information.
        """
        return f'ID: {self.student_id} - Nombre: {self.name} {self.last_name} - Telefono: {self.phone_number} - Email: {self.email}'

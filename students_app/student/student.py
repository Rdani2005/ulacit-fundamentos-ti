class Student:
    @property
    def student_id(self) -> str:
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
    @property
    def address(self) -> str:
        return self.__address

    def __init__(self,
                 student_id: str,
                 name: str,
                 last_name: str,
                 phone_number: str,
                 email: str,
                 address: str
                 ) -> None:
        self.__id = student_id
        self.__name = name
        self.__last_name = last_name
        self.__phone_number = phone_number
        self.__email = email
        self.__address = address

    def __str__(self) -> str:
        return f'ID: {self.student_id} - Nombre: {self.name} {self.last_name} - Telefono: {self.phone_number} - Email: {self.email} - Direccion: {self.address}'

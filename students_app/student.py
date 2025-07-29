from inputs import Inputs

class Student:
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
                 name: str,
                 last_name: str,
                 phone_number: str,
                 email: str,
                 address: str
                 ) -> None:
        self.__name = name
        self.__last_name = last_name
        self.__phone_number = phone_number
        self.__email = email
        self.__address = address

    def __str__(self) -> str:
        return f'Nombre: {self.name} {self.last_name} - Telefono: {self.phone_number} - Email: {self.email} - Direccion: {self.address}'

    def to_dict(self):
        return {
            'name': self.name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'address': self.address,
        }

class StudentParser:
    @staticmethod
    def from_dict_to_student(data: dict) -> Student:
        return Student(
            name=data['name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            email=data['email'],
            address=data['address'],
        )

    @staticmethod
    def from_student_to_dict(student: Student) -> object:
        return {
            'name': student.name,
            'last_name': student.last_name,
            'phone_number': student.phone_number,
            'email': student.email,
            'address': student.address,
        }

class StudentFactory:
    @staticmethod
    def create_student() -> Student:
        print("\nAgregando Estudiante")
        name = Inputs.get_non_empty_input("Nombre del estudiante: ")
        last_name = Inputs.get_non_empty_input("Apellido del estudiante: ")
        phone_number = Inputs.get_non_empty_input("Numero del estudiante: ")
        email = Inputs.get_non_empty_input("Email del estudiante: ")
        address = Inputs.get_non_empty_input("Direccion del estudiante: ")

        return Student(
            name,
            last_name,
            phone_number,
            email,
            address
        )
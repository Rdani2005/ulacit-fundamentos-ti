from course.course import Course
from course.course_factory import CourseFactory
from enrollment.enrollment import Enrollment
from enrollment.enrollment_factory import EnrollmentFactory
from injectors import ManagerInjectors
from student.student import Student
from inputs import Inputs
from student.student_factory import StudentFactory

class Main:
    def __init__(self):
        manager_injectors = ManagerInjectors()
        self.__students_manager = manager_injectors.student_manager
        self.__courses_manager = manager_injectors.course_manager
        self.__enrollment_manager = manager_injectors.enrollment_manager

    def add_student(self):
        student: Student = StudentFactory.create_student(
            self.__students_manager.build_new_student_id()
        )
        self.__students_manager.add_student(student)

    def show_students(self):
        self.__students_manager.show_students()

    def exit_application(self):
        print("Saliendo...")
        exit(0)

    def add_course(self):
        course: Course = CourseFactory.create_course(
            self.__courses_manager.build_new_course_id()
        )
        self.__courses_manager.add_course(course)

    def show_available_curses(self):
        self.__courses_manager.show_all_courses()

    def add_enrollment(self):
        possible_enrollment: Enrollment = EnrollmentFactory.create_enrollment()
        enrollment = self.__enrollment_manager.enroll_student(possible_enrollment.student_id, possible_enrollment.course_id)
        if enrollment is None:
            print("No se ha podido realizar la matricula.")
            return
        self.__enrollment_manager.save_enrollment(enrollment)


    def show_enrollments(self):
        self.__enrollment_manager.show_enrollments()


    def menu(self):
        print("\n------- Menu Principal ------")
        print("1.Agregar un nuevo estudiante.")
        print("2.Mostrar estudiantes almacenados.")
        print("3.Agregar un nuevo curso.")
        print("4.Mostrar cursos almacenados.")
        print("5. Matricular estudiantes.")
        print("6.Mostrar matriculas actuales.")
        print("7.salir")
        option = Inputs.get_valid_number("Seleccione una opcion: ")
        if option == 1:
            self.add_student()
        elif option == 2:
            self.show_students()
        elif option == 3:
            self.add_course()
        elif option == 4:
            self.show_available_curses()
        elif option == 5:
            self.add_enrollment()
        elif option == 6:
            self.show_enrollments()
        elif option == 7:
            self.exit_application()
        else:
            print("Opcion invalida. Intente nuevamente.")
        self.menu()

Main().menu()
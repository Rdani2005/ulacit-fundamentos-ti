"""
    This code defines a Calculator class that performs basic arithmetic operations.
"""
class Calculator:
    """
        A simple calculator class to perform basic arithmetic operations.
    """
    def __init__(self, operator1: float, operator2: float):
        self.__operator1 = operator1
        self.__operator2 = operator2

    def __str__(self) -> str:
        return f"calculadora con operadores {self.__operator1} y {self.__operator2}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Calculator):
            return False
        return (self.__operator1 == other.__operator1 and
                self.__operator2 == other.__operator2)

    """
        Adds two numbers and returns the result.
    """
    def add(self) -> float:
        return self.__operator1 + self.__operator2

    """
        Subtracts the second number from the first and returns the result.
    """
    def subtract(self) -> float:
        return self.__operator1 - self.__operator2

    """
        Multiplies two numbers and returns the result.
    """
    def multiply(self) -> float:
        return self.__operator1 * self.__operator2

    """
        Divides the first number by the second and returns the result. Raises an error if the second number is zero.
    """
    def divide(self) -> float:
        if self.__operator2 == 0:
            raise ValueError("Cannot divide by zero")
        return self.__operator1 / self.__operator2

    """
        Getters and Setters for the operator attributes.
    """
    def get_operator1(self) -> float:
        return self.__operator1

    def get_operator2(self) -> float:
        return self.__operator2

    def set_operator1(self, operator1: float) -> None:
        self.__operator1 = operator1

    def set_operator2(self, operator2: float) -> None:
        self.__operator2 = operator2


"""
    Main program
"""
if __name__ == "__main__":
    # Create an instance of the Calculator class
    calc: Calculator = Calculator(10, 5)
    
    # Print the calculator object
    print(calc)
    
    # Perform operations and print results
    print(f'El Resultado de la suma es: {calc.add()}')
    print(f'El Resultado de la resta es: {calc.subtract()}')
    print(f'El Resultado de la multiplicación es: {calc.multiply()}')
    print(f'El Resultado de la división es: {calc.divide()}')


    calc2: Calculator = Calculator(10, 5)
    print(calc2)
    print(f'El Resultado de la suma es: {calc2.add()}')
    print(f'El Resultado de la resta es: {calc2.subtract()}')
    print(f'El Resultado de la multiplicación es: {calc2.multiply()}')
    print(f'El Resultado de la división es: {calc2.divide()}')











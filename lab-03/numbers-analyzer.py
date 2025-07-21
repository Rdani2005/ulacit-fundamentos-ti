"""
    Program that prompts the user to input 10 numbers (which may include duplicates) and stores them in a list.
    
    Then, it displays:
    - The original list
    - A new list with unique elements sorted in ascending order

    Author: Daniel Sequeira
    Date: July 21, 2025
"""
from typing import List

class NumbersAnalyzer:
    """
        A class to analyze a list of numbers.
    """
    def __init__(self, numbers: List[int]) -> None:
        self.numbers = numbers

    def get_numbers(self) -> List[int]:
        return self.numbers

    def get_sorted_list(self) -> List[int]:
        """
            Get the sorted list of numbers.
            
            Returns:
                List[int]: The sorted list of numbers.
        """
        return sorted(set(self.numbers))


class Main:
    @staticmethod
    def run() -> None:
        """
            Run the program: collect input, analyze numbers, and display results.
        """
        numbers: List[int] = []
        for index in range(10):
            while True:
                try:
                    number = int(input(f"Ingrese el numero #{index + 1} para agregarlo a la lista: "))
                    numbers.append(number)
                    break
                except ValueError:
                    print("Por favor, ingrese un numero entero valido.")



        analyzer = NumbersAnalyzer(numbers)
        sorted_numbers = analyzer.get_sorted_list()

        print("Lista Completa de numeros:", analyzer.get_numbers())
        print("Lista con numeros ordenados y unicos:", sorted_numbers)


if __name__ == "__main__":
    Main.run()

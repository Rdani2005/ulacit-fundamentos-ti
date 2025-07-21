"""
    Program that prompts the user to input the ages of 5 people and stores them in a list.
    
    Then, it displays:
        - The complete list of ages
        - The average age
        - The number of people who are adults (age ≥ 18)

    Author: Daniel Sequeira
    Date: July 21, 2025
"""


from typing import List

class AgeAnalyzer:
    """
        A class to analyze a list of ages.

        Attributes:
            ages (List[int]): A list of integers representing ages.
    """
    def __init__(self, ages: List[int]) -> None:
        self.ages: List[int] = ages

    def get_age_list(self) -> List[int]:
        """
            Get the list of ages.

            Returns:
                List[int]: The list of ages.
        """
        return self.ages

    def get_average_age(self) -> float:
        """
            Calculate the average age.

            Returns:
                float: The average of the ages.
        """
        return sum(self.ages) / len(self.ages)
    def count_adults(self) -> int:
        """
            Count how many people are adults (18 or older).

            Returns:
                int: Number of people 18 or older.
        """
        return len([age for age in self.ages if age >= 18])

class Main:
    """
        Main execution class to run the age analyzer program.
    """

    @staticmethod
    def run() -> None:
        """
            Run the program: collect input, analyze ages, and display results.
        """
        ages: List[int] = []

        for i in range(5):
            while True:
                try:
                    age_input = int(input(f"Ingrese la edad de la persona #{i + 1}: "))
                    ages.append(age_input)
                    break
                except ValueError:
                    print("Por favor, ingrese un numero entero valido.")


        analyzer = AgeAnalyzer(ages)
        print(f"\nLista de las edades: {analyzer.get_age_list()}")
        print(f"Promedio de edad: {analyzer.get_average_age()}")
        print(f"Numero de adultos (18 o mas): {analyzer.count_adults()}")

if __name__ == "__main__":
    Main.run()

"""
    Program that allows the user to create a list with the names of their friends.
    
    Then, it asks for a name and checks if it is in the list, displaying an appropriate message.

    Author: Daniel Sequeira  
    Date: July 21, 2025
"""

from typing import List

STOP_SIGNAL: str = "listo"

class Friend:
    def __init__(self, name: str) -> None:
        self.__name: str = name

    def get_name(self) -> str:
        """
            Get the name of the friend.
            
            Returns:
                str: The name of the friend.
        """
        return self.__name

    def say_hello(self) -> str:
        """
            Generate a greeting message for the friend.
            
            Returns:
                str: A greeting message.
        """
        return f"Hola, yo soy {self.get_name()}!"

    def __str__(self) -> str:
        """
            String representation of the Friend object.
            
            Returns:
                str: The name of the friend.
        """
        return self.get_name().strip()

    def __eq__(self, other: object):
        """
            Check equality with another Friends object.
            
            Args:
                other (object): The object to compare with.
                
            Returns:
                bool: True if the names are the same, False otherwise.
        """
        if not isinstance(other, Friend):
            return False
        return self.get_name().strip() == other.get_name().strip()



class FriendsAnalyzer:
    """
        A class to analyze a list of friends.
        
        Attributes:
            friends (List[Friends]): A list of Friends objects.
    """
    def __init__(self, friends: List[Friend]) -> None:
        self.__friends: List[Friend] = friends

    def get_friends(self) -> List[Friend]:
        """
            Get the list of friends.
            
            Returns:
                List[Friends]: The list of Friends objects.
        """
        return self.__friends

    def greet_friends(self) -> List[str]:
        """
            Generate greetings for all friends.
            
            Returns:
                List[str]: A list of greeting messages.
        """
        return [friend.say_hello() for friend in self.get_friends()]

    def is_friend_on_list(self, friend: Friend) -> bool:
        """
            Check if a specific friend is in the list.
            
            Args:
                friend (Friend): The friend to check.
                
            Returns:
                bool: True if the friend is in the list, False otherwise.
        """
        return friend in self.get_friends()

class FriendsAnalyzerFactory:
    """
        Factory class to create FriendsAnalyzer instances.
    """
    @staticmethod
    def create_analyzer() -> FriendsAnalyzer:
        """
            Create a FriendsAnalyzer instance with the provided list of friends.
            
            Args:
                friends (List[Friends]): The list of Friends objects.
                
            Returns:
                FriendsAnalyzer: An instance of FriendsAnalyzer.
        """
        print(f"Ingrese el nombre de sus amigos. Escriba '{STOP_SIGNAL}' cuando termine:")
        friends: List[Friend] = []
        continue_input: boolean = True

        while continue_input:
            name = input(f"Ingrese el nombre del amigo (o '{STOP_SIGNAL}' para terminar): ")
            if name.lower().strip() == STOP_SIGNAL:
                continue_input = False
            else:
                friends.append(Friend(name.strip()))

        return FriendsAnalyzer(friends)

class Main:
    """
        Main execution class to run the friends analyzer program.
    """

    @staticmethod
    def run() -> None:
        """
            Run the program: collect input, analyze friends, and display results.
        """
        analyzer: FriendsAnalyzer = FriendsAnalyzerFactory.create_analyzer()

        print("\nLista de amigos:")
        for friend in analyzer.get_friends():
            print(friend)

        print("\nSaludos por parte de los amigos:")
        for greeting in analyzer.greet_friends():
            print(greeting)

        print("\nVerificando si un amigo está en la lista:")
        name_to_check = input("Ingrese el nombre del amigo a verificar: ").strip()

        friend_to_check = Friend(name_to_check)

        if analyzer.is_friend_on_list(friend_to_check):
            print(f"{friend_to_check.get_name()} está en la lista de amigos.")
        else:
            print(f"{friend_to_check.get_name()} no está en la lista de amigos.")



if __name__ == "__main__":
    Main.run()

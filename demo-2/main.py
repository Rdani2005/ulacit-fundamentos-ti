# Gestor de correos electronicos:

# receive name, lastName, and domain.
# print the new email.


# name = input("cual es tu nombre?: ")
# firstLastName = input("cual es tu primer apellido?: ")
# secondLastName = input("cual es tu segundo apellido?: ")
# domain = input("What is the domain for your email?: ")
#
# name = name.replace(" ", ".")
# firstLastName = firstLastName.replace(" ", ".")
# secondLastName = secondLastName.replace(" ", ".")
#
#
# print(f"Tu email es: {name.lower()}.{firstLastName.lower()}.{secondLastName.lower()}@{domain.lower()}")




name = input("cual es tu nombre?: ")
lastName = input("cual es tu apellido?: ")
domain = input("What is the domain for your email?: ")

name = name.replace(" ", ".")
lastName = lastName.replace(" ", ".")


print(f"Tu email es: {name.lower()[:2]}{lastName.lower()[:4]}@{domain.lower()}")


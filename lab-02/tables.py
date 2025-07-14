'''
    Escribe un programa que solicite al usuario un número del 1 al 10 y muestra su tabla de multiplicar del 1 al 10
'''

# Ask the user for a number between 1 and 10
number = int(input("Inserte un numero entre 1 y 10: "))

# Check if the number is in the valid range
if 1 <= number <= 10:
    print(f"La tabla de multiplicacion para el numero {number} es:")
    for i in range(1, 11):
        result = number * i
        print(f"{number} x {i} = {result}")
else:
    print("Numero invalido. Por favor ingrese un numero entre 1 y 10.")

# Escribe un programa que solicite dos números enteros (inicio y fin) y calcule la suma de todos los números pares en ese rango (inclusive).

# Input Variables
start = int(input("Ingresa el número de inicio: "))
end = int(input("Ingresa el número de fin: "))

# Inicializar la suma
even_sum = 0

# Recorrer el rango e ir sumando solo los pares
for number in range(start, end + 1):
    if number % 2 == 0:
        even_sum += number

# Mostrar el resultado
print(f"La suma de los números pares entre {start} y {end} es: {even_sum}")

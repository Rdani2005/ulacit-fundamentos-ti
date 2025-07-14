'''
Escribe un programa que le permite al usuario ingresar "n" números. Al final, muestra cuántos fueron:
    - Positivos
    - Negativos
    - Iguales a cero
'''
# Ask the user how many numbers they want to enter
reading_number_amounts = int(input("cuantos numeros desea ingresar? "))

# Initialize counters
positive_count = 0
negative_count = 0
zero_count = 0

# Loop to read 'n' numbers
for i in range(reading_number_amounts):
    number = float(input(f"Ingrese el numero #{i + 1}: "))
    
    if number > 0:
        positive_count += 1
    elif number < 0:
        negative_count += 1
    else:
        zero_count += 1

# Display the results
print("Resultados:")
print(f"Cantidad de numeros positivos: {positive_count}")
print(f"Cantidad de numeros negativos: {negative_count}")
print(f"Cantidad de 0 ingresados: {zero_count}")

'''
Escribe un programa que solicite 5 calificaciones, guardelas en una lista, y muestra:

    1. El promedio

    2. Cuántas son mayores o iguales a 70

    3. La calificación más alta y más baja

'''

# Create an empty list to store the grades
grades = []

# Ask the user to input 5 grades
for i in range(5):
    grade = float(input(f"Ingrese la nota #{i + 1}: "))
    grades.append(grade)

# Calculate the average
average = sum(grades) / len(grades)

# Count how many grades are greater than or equal to 70
passing_count = sum(1 for grade in grades if grade >= 70)

# Find the highest and lowest grade
highest = max(grades)
lowest = min(grades)

# Display the results
print(f"Promedio de las notas: {average:.2f}")
print(f"Cantidad de notas >= 70: {passing_count}")
print(f"Nota mas alta: {highest}")
print(f"Nota mas baja: {lowest}")

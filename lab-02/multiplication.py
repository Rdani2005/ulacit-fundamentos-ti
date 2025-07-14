# Ask the user for two integers
a = int(input("Ingrese el primer numero: "))
b = int(input("Ingrese el segundo numero: "))

# Initialize result
result = 0

# Handle negative values
negative = False
if b < 0:
    b = -b
    negative = True

# Add 'a' to result 'b' times
for _ in range(b):
    result += a

# Adjust sign if necessary
if negative:
    result = -result

# Display the result
print(f"El resultado de la multiplicacion es: {result}")

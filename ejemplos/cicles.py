numero = -1  # Inicializamos con un valor que garantice entrar al ciclo 
 
while numero <= 0: 
    numero = int(input("Por favor ingrese un número positivo: ")) 
    if numero <= 0: 
        print("¡El número debe ser positivo!") 
         
print(f"Has ingresado: {numero}") 

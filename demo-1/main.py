# This is a Python Comment
# Demo01 - first Hello World Program
# Author: Danny Sequeira
# Date: 2025-06-16


print("Hello World!")  # This prints Hello World to the console

# VARIABLES - keep information in memory
# rules for variable names:
# 1. Must start with a letter or underscore
# 2. Can contain letters, numbers, and underscores
# 3. Cannot use reserved keywords (like 'if', 'else', 'while', etc.)


# ::::::::::::::: Convention ::::::::::::::::
# 4. Use descriptive names (e.g., full_name, age, is_active)
# 5. Use snake_case for variable names (e.g., full_name, user_age)
# 6. Use ALL_CAPS for constants (e.g., MAX_VALUE, PI)

full_name = "Danny Sequeira"
print(full_name)
age = 30

print(":::::::::::::::::::::::::::::::")

client_name = "John Doe"
client_age = 25
is_active = True
client_address = "123 Main St"
client_phone = "555-1234"


print(f"Client Name: {client_name}")
print(f"Client Age: {client_age}")
print(f"Is Active: {is_active}")
print(f"Client Address: {client_address}")
print(f"Client Phone: {client_phone}")





# ::::::::::::::: Hotel Booking Example ::::::::::::::::

hotel_client_name = "Alice Smith"
hotel_client_booking_days = 5
hotel_booking_price = 1200.0
hotel_ocean_view = True


print(f"╔════════════════════════════════╗")
print(f"║       Hotel Booking Info       ║")
print(f"╠════════════════════╦═══════════╣")
print(f"║ Client's Name     ║ {hotel_client_name:<10}║")
print(f"║ Booking Days      ║ {hotel_client_booking_days:<10} ║")
print(f"║ Price Per Day ($) ║ {hotel_booking_price:<10.2f} ║")
print(f"║ Ocean View        ║ {str(hotel_ocean_view):<10} ║")
print(f"╚════════════════════╩═══════════╝")



# ::::::::::::::: Ecommerce ::::::::::::::::
ecommerce_product_name = "Wireless Headphones"
ecommerce_product_price = 99.99
ecommerce_product_stock = 20
ecommerce_product_available = True

print(f"╔════════════════════════════════════════════╗")
print(f"║          Ecommerce Product Info            ║")
print(f"╠═══════════════════════╦════════════════════╣")
print(f"║ Product Name         ║ {ecommerce_product_name:<15} ║")
print(f"║ Product Price ($)    ║ {ecommerce_product_price:<15.2f}     ║")
print(f"║ Product Stock        ║ {ecommerce_product_stock:<15}     ║")
print(f"║ Product Available    ║ {str(ecommerce_product_available):<15}     ║")
print(f"╚═══════════════════════╩════════════════════╝")








class Inputs:
    @staticmethod
    def get_non_empty_input(prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Este campo es obligatorio. Intenta de nuevo.")

    @staticmethod
    def get_valid_number(prompt):
        while True:
            value = input(prompt).strip()
            if value.isdigit():
                return int(value)
            print("Debes ingresar un número válido (solo dígitos).")

    @staticmethod
    def get_boolean(prompt):
        while True:
            value = input(f"{prompt} (si o no):").strip()
            if value.lower() in ("si", "s", "yes", "y", "true", "t", "1"):
                return True
            if value.lower() in ("no", "n", "false", "f", "0"):
                return False
            print("")
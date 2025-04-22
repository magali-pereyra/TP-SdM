class Persona:
    def __init__(self, nombre, apellido, cedula):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser una cadena no vacía.")

        if not isinstance(apellido, str) or not apellido.strip():
            raise ValueError("El apellido debe ser una cadena no vacía.")

        try:
            cedula = int(cedula)
        except (ValueError, TypeError):
            raise ValueError("La cédula debe ser un número entero válido.")

        self.nombre = nombre.strip().title()
        self.apellido = apellido.strip().title()
        self._cedula = cedula

    @property
    def cedula(self):
        return self._cedula

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
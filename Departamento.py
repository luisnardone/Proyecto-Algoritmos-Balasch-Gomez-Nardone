class Departamento:
    def __init__(self, idx, display_name):
        """
        Inicializa una instancia del departamento.

        Args:
            idx (int): ID del departamento.
            display_name (str): Nombre del departamento.
        """
        self.idx = idx
        self.display_name = display_name

    def mostrar(self):
        """
        Devuelve una cadena con los atributos del departamento.

        Returns:
            str: Cadena con el ID y nombre del departamento.
        """
        return f'''ID: {self.idx} - Departamento: {self.display_name}'''

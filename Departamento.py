class Departamento:
    def __init__(self, idx, display_name):
        self.idx = idx
        self.display_name = display_name

    def mostrar(self):
        return f'''ID: {self.idx} - Departamento: {self.display_name}'''

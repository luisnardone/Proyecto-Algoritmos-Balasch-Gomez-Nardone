class Artista:
    def __init__(self, display_name, nationality, begin_date, end_date):
        self.display_name = display_name
        self.nationality = nationality
        self.begin_date = begin_date
        self.end_date = end_date

    def mostrar(self):
        return f'''
Nombre: {self.display_name} - Nacionalidad: {self.nationality}
Año de:
    Nacimiento: {self.begin_date}
    Fallecimiento: {self.end_date}
'''
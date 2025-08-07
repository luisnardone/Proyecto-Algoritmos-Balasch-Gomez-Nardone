class Artista:
    def __init__(self, display_name, nationality, begin_date, end_date):
        """
        Inicializa una instancia de la clase Artista.

        Args:
            display_name (str): Nombre del artista.
            nationality (str): Nacionalidad del artista.
            begin_date (str): Año de nacimiento.
            end_date (str): Año de fallecimiento.
        """
        self.display_name = display_name
        self.nationality = nationality
        self.begin_date = begin_date
        self.end_date = end_date

    def mostrar(self):
        """
        Devuelve una cadena con la información del artista.

        Returns:
            str: Nombre, nacionalidad y fechas de nacimiento y fallecimiento.
        """
        return f'''
Nombre: {self.display_name} - Nacionalidad: {self.nationality}
Año de:
    Nacimiento: {self.begin_date}
    Fallecimiento: {self.end_date}
'''
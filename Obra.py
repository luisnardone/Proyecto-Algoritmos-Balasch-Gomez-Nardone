class Obra:
    def __init__(self, idx, title, artist, date, classification, department, primary_image):
        """
        Inicializa una instancia de la clase Obra.

        Args:
            idx (int): ID de la obra.
            title (str): Título de la obra.
            artist (Artista): Instancia de la clase Artista.
            date (str): Fecha de creación de la obra.
            classification (str): Clasificación de la obra.
            department (str): Departamento al que pertenece la obra.
            primary_image (str): URL de la imagen principal de la obra.
        """
        self.idx = idx
        self.title = title
        self.artist = artist
        self.date = date
        self.classification = classification
        self.department = department
        self.primary_image = primary_image

    def mostrar_general(self):
        """
        Devuelve una cadena con la información general de la obra.

        Returns:
            str: Cadena con el ID, título y nombre del artista.
        """
        return f'''ID: {self.idx} - Titulo de la Obra: {self.title} - Nombre del Artista: {self.artist.display_name}'''
    
    def mostrar_detalles(self):
        """
        Devuelve una cadena con los detalles completos de la obra, incluyendo información del artista.

        Returns:
            str: Detalles extendidos de la obra y del artista asociado.
        """
        return f'''
ID: {self.idx} - Titulo de la Obra: {self.title} - Clasificación: {self.classification}
Fecha de Creación: {self.date}
Departamento: {self.department}

Informacion del Artista: {self.artist.mostrar()}
'''

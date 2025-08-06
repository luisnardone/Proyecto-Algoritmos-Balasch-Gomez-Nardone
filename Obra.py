class Obra:
    def __init__(self, idx, title, artist, date, classification, department, primary_image):
        self.idx = idx
        self.title = title
        self.artist = artist
        self.date = date
        self.classification = classification
        self.department = department
        self.primary_image = primary_image

    def mostrar_general(self):
        return f'''ID: {self.idx} - Titulo de la Obra: {self.title} - Nombre del Artista: {self.artist.display_name}'''
    
    def mostrar_detalles(self):
        return f'''
ID: {self.idx} - Titulo de la Obra: {self.title} - Clasificación: {self.classification}
Fecha de Creación: {self.date}
Departamento: {self.department}

Informacion del Artista: {self.artist.mostrar()}
'''

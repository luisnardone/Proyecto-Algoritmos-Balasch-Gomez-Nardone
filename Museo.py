import requests
from PIL import Image

import csv

from Obra import Obra
from Artista import Artista
from Departamento import Departamento

class Museo():
    def __init__(self):
        self.departamentos = []
        self.obras = []

    def obtener_departamentos(self):
        api = 'https://collectionapi.metmuseum.org/public/collection/v1/departments'
        try:
            departamentos = requests.get(api).json()['departments']
        except:
            print('No se ha podido cargar los departamentos correctamente... Intente mas tarde\n')
            return None
        return departamentos

    def cargar_departamentos(self):
        departamentos = self.obtener_departamentos()
        if not departamentos:
            return
        for departamento in departamentos:
            idx = departamento['departmentId']
            display_name = departamento['displayName']
            nuevo_departamento = Departamento(idx,display_name)
            self.departamentos.append(nuevo_departamento)
        print('Datos Cargados Exitosamente')

    def obra_a_objeto(self, obra):
        idx = obra['objectID']
        title = obra['title']
        date = obra['objectDate']
        classification = obra['classification']
        department = obra['department']
        primary_image = obra['primaryImage']

        if obra['artistDisplayName'] == "":
            artistDisplayName = "Desconocido"
        else:
            artistDisplayName = obra['artistDisplayName']

        if obra['artistNationality'] == "":
            artistNationality = "Desconocido"
        else:
            artistNationality = obra['artistNationality']

        if obra['artistBeginDate'] == "":
            artistBeginDate = "Desconocido"
        else:
            artistBeginDate = obra['artistBeginDate']

        if obra['artistEndDate'] == "":
            artistEndDate = "Desconocido"
        else:
            artistEndDate = obra['artistEndDate']

        artist = Artista(artistDisplayName,artistNationality,artistBeginDate,artistEndDate)

        return Obra(idx, title, artist, date, classification, department, primary_image)
    
    def buscar_obra_por_idx(self,idx):
        print('Buscando LOCAL...')
        for obra in self.obras:
            if obra.idx == idx:
                return obra
        return None
    
    def obtener_obra(self, idx):
        print('Buscando en API...')
        api = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{idx}'
        try:
            obra_dict = requests.get(api).json()
        except Exception as e:
            print(f'Error al obtener la obra de ID {idx}.\nError: {e}')
            return None
        obra = self.obra_a_objeto(obra_dict)
        self.obras.append(obra)

        return obra

    def obtener_obras_por_departamentos(self):
        pass

    def buscar_por_departamento(self):
        pass


    def obtener_obras_por_nacionalidad(self):
        pass

    def buscar_por_nacionalidad(self):
        pass


    def obtener_obras_por_nombre_autor(self):
        pass

    def buscar_por_autor(self):
        pass


    def mostrar_detalles(self):
        pass

    def mostrar_imagen(self):
        pass

    def buscar_obras(self):
        while True:
            print('\nBÚSQUEDA DE OBRAS ')
            print('''MENÚ
    1. Buscar por Departamento
    2. Buscar por Nacionalidad del Autor
    3. Buscar por Nombre del Autor
    4. Volver''')

            ans = input('Ingrese el número de la opción deseada:  ')

            while not ans.isnumeric() or int(ans) not in range(1,5):
                print('Debe ingresar una opción válida')
                ans = input('Ingrese el número de la opción deseada: ')

            if ans == '4':
                print('Saliendo del menú de búsqueda...\n')
                break
            elif ans == '1':
                self.buscar_por_departamento()
            elif ans == '2':
                self.buscar_por_nacionalidad()
            elif ans == '3':
                self.buscar_por_autor()


    def menu(self):
        self.cargar_departamentos()
        if len(self.departamentos) == 0:
            print('No se han logrado cargar los datos necesarios...')
            return
        
        print('\nBIENVENIDO/A AL MUSEO METROPOLITANO')
        print('''Integrantes:
1. Luis Nardone
2. Erick Balasch
3. Isabel Gomez
''')
        while True:
            print('''
MENÚ PRINCIPAL
1. Búsqueda de Obras
2. Salir''')
                
            ans = input('Ingrese el número de la opción deseada: ')

            while not ans.isnumeric() or int(ans) not in range(1,4):
                print('Debe ingresar una opción válida')
                ans = input('Ingrese el número de la opción deseada: ')

            if ans == '1':
                self.buscar_obras()
            else:
                print('HASTA LUEGO')
                break

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


    def buscar_obras(self):
        pass


    def mostrar_detalles(self):
        pass

    def mostrar_imagen(self):
        pass


    def menu(self):
        self.cargar_departamentos()
        if len(self.cargar_departamentos) == 0:
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

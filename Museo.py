import requests
from PIL import Image

import csv

from Obra import Obra
from Artista import Artista
from Departamento import Departamento

class Museo():
    def __init__(self):
        """
        Inicializa una instancia de la clase Museo
        """
        self.departamentos = []
        self.obras = []


    # CARGA DE DATOS DE DEPARTAMENTOS ##

    def obtener_departamentos(self):
        """
        Obtiene la lista de departamentos del museo desde la API del MET.

        Returns:
            list: Lista de diccionarios con los departamentos si la solicitud es exitosa, None si falla.
        """

        api = 'https://collectionapi.metmuseum.org/public/collection/v1/departments'
        try:
            departamentos = requests.get(api).json()['departments']
        except:
            print('No se ha podido cargar los departamentos correctamente... Intente mas tarde\n')
            return None
        return departamentos

    def cargar_departamentos(self):
        """
        Carga los departamentos obtenidos desde la API en la lista interna `self.departamentos`.
        """
        departamentos = self.obtener_departamentos()
        if not departamentos:
            return
        for departamento in departamentos:
            idx = departamento['departmentId']
            display_name = departamento['displayName']
            nuevo_departamento = Departamento(idx,display_name)
            self.departamentos.append(nuevo_departamento)
        print('Datos Cargados Exitosamente')

    # CARGA DE DATOS DE DEPARTAMENTOS ##



    # MANEJO DE OBJETOS ##

    def obra_a_objeto(self, obra):
        """
        Convierte un diccionario obtenido desde la API del MET en una instancia de la clase `Obra`.

        Args:
            obra (dict): Diccionario con los datos de una obra.

        Returns:
            Obra: Objeto de tipo `Obra` con los atributos cargados.
        """
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
        """
        Busca una obra previamente almacenada por su ID.

        Args:
            idx (int): ID de la obra.

        Returns:
            Obra or None: La obra si está almacenada, None si no se encuentra.
        """
        for obra in self.obras:
            if obra.idx == idx:
                print(f'\nObra {idx} encontrada. Fue previamente almacenada...')
                return obra
        
        return None
    
    def obtener_obra(self, idx):
        """
        Obtiene una obra desde la API del MET por su ID, la convierte en objeto y la almacena.

        Args:
            idx (int): ID de la obra.

        Returns:
            Obra or None: La obra obtenida si existe, None si hay error en la solicitud.
        """
        api = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{idx}'
        try:
            obra_dict = requests.get(api).json()
        except Exception as e:
            print(f'Error al obtener la obra de ID {idx}.\nError: {e}')
            return None
        obra = self.obra_a_objeto(obra_dict)
        self.obras.append(obra)

        print(f'\nObra {idx} encontrada. Obtenida de la API...')
        return obra

    # MANEJO DE OBJETOS ##



    # BUSQUEDA POR DEPARTAMENTO ##

    def obtener_obras_por_departamentos(self, dpto):
        """
        Obtiene y selecciona obras pertenecientes a un departamento específico.
        Obtiene la información de 10 en 10, de acuerdo a la solicitud del usuario
        Args:
            dpto (Departamento): Instancia del departamento del cual obtener obras.

        Returns:
            list: Lista de objetos `Obra` obtenidas desde la API.
        """
        api_url = f'https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds={dpto.idx}'

        respuesta = requests.get(api_url).json()
        print(f"Se han obtenido {respuesta['total']} obras")
        print('\nObteniendo las primeras 10...')

        obras_seleccionadas = []
        contador = 0

        for idx in respuesta['objectIDs']:
            obra = self.buscar_obra_por_idx(idx)
            if obra is None:
                obra = self.obtener_obra(idx)
                if obra is None:
                    continue

            if obra not in self.obras:
                self.obras.append(obra)

            obras_seleccionadas.append(obra)
            print(f'Obra {idx} obtenida...')
            contador += 1

            if contador % 10 == 0:
                print('\nOBRAS OBTENIDAS:')
                for obra in obras_seleccionadas[contador-10:contador]:
                    print(f'{obra.idx} - Titulo: {obra.title}')
                print(f'Se han logrado guardar {len(obras_seleccionadas)} obras')
                ans = input('¿Desea obtener otras 10 obras? Si (s)/No (n): ').lower()
                while ans not in ['s', 'n']:
                    ans = input('Debe ingresar s o n: ')
                if ans == 'n':
                    return obras_seleccionadas

        return obras_seleccionadas
    
    def buscar_por_departamento(self):
        """
        Interfaz interactiva para seleccionar un departamento y visualizar obras correspondientes.
        """
        print('\nBÚSQUEDA POR DEPARTAMENTO ')

        for i, departamento in enumerate(self.departamentos):
            print(f'{i+1}) {departamento.mostrar()}')

        ans = input('Ingrese el número (no ID) deseado: ')
        while not ans.isnumeric() or int(ans) not in range(1, len(self.departamentos) + 1):
            print('Ingrese una opción válida...')
            ans = input('Ingrese el número deseado: ')

        dpto = self.departamentos[int(ans) - 1]
        print(f'DEPARTAMENTO SELECCIONADO: {dpto.display_name}')
        obras_seleccionadas = self.obtener_obras_por_departamentos(dpto)

        if len(obras_seleccionadas) == 0:
            print('No se han encontrado obras en el departamento seleccionado...')
        else:
            for obra in obras_seleccionadas:
                print(obra.mostrar_general())

            self.mostrar_detalles(obras_seleccionadas)

    # BUSQUEDA POR DEPARTAMENTO ##


    # BUSQUEDA POR NACIONALIDAD ##

    def buscar_por_nacionalidad(self):
        """
        Interfaz interactiva para buscar obras según la nacionalidad del artista.
        """
        print('\nBÚSQUEDA POR NACIONALIDAD DEL ARTISTA')

        nacionalidades = []
        with open('Nacionalidades.csv', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                nacionalidades.append(fila['Nationality'])
        
        num = 1
        for nacionalidad in nacionalidades:
            print(f'{num}) {nacionalidad.capitalize()}')
            num+=1
            if num%100 == 0:
                input('ENTER para ver más...')

        ans = input('Ingrese el número deseado: ')
        while not ans.isnumeric() or int(ans) not in range(1,num):
            print('Ingrese una opción válida...')
            ans = input('Ingrese el número deseado: ')
        
        nacionalidad_seleccionado = nacionalidades[int(ans)-1]

        print(f'NACIONALIDAD SELECCIONADA: {nacionalidad_seleccionado}')

        obras_seleccionadas = self.obtener_obras_por_nacionalidad(nacionalidad_seleccionado)
        print(f'\nOBRAS POR NACIONALIDAD DEL ARTISTA: {nacionalidad_seleccionado.upper()}')
        if len(obras_seleccionadas) == 0:
            print('No se han encontrado obras con la nacionalidad seleccionada...')
        else:
            for obra in obras_seleccionadas:
                print(obra.mostrar_general())
            
            self.mostrar_detalles(obras_seleccionadas)

    def obtener_obras_por_nacionalidad(self, nacionalidad):
        """
        Busca obras según la nacionalidad del artista usando la API.

        Args:
            nacionalidad (str): Nacionalidad a buscar.

        Returns:
            list: Lista de obras que coinciden con la nacionalidad del artista.
        """
        api_url = f'https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q={nacionalidad}'

        respuesta = requests.get(api_url).json()
        print(f"Se han obtenido {respuesta['total']} obras")
        print('\nObteniendo las primeras 10...')

        obras_seleccionadas = []
        contador = 0

        for idx in respuesta['objectIDs']:
            obra = self.buscar_obra_por_idx(idx)
            if obra == None:
                obra = self.obtener_obra(idx)
                if obra == None:
                    continue

            if nacionalidad.lower() in obra.artist.nationality.lower():
                obras_seleccionadas.append(obra)
                print(f'Obra {idx} obtenida...')
            else:
                print(f'Obra {idx} no fue almacenada porque no coincide con el criterio de búsqueda.')
            contador += 1

            if contador % 10 == 0:
                print('\nOBRAS OBTENIDAS:')
                for obra in obras_seleccionadas[contador-10:contador]:
                    print(f'{obra.idx} - Titulo: {obra.title}')
                ans = input('¿Desea obtener otras 10 obras? Si (s)/No (n): ').lower()
                while ans not in ['s', 'n']:
                    ans = input('Debe ingresar s o n: ')
                if ans == 'n':
                    return obras_seleccionadas
                

        return obras_seleccionadas

    # BUSQUEDA POR NACIONALIDAD ##


    # BUSQUEDA POR NOMBRE DE AUTOR ##

    def obtener_obras_por_nombre_autor(self,nombre):
        """
        Obtiene obras según el nombre del artista desde la API del MET.

        Args:
            nombre (str): Nombre del artista.

        Returns:
            list: Lista de obras que coinciden con el nombre del artista.
        """
        api_url = f'https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q={nombre}'
        respuesta = requests.get(api_url).json()
        print(f"Se han obtenido {respuesta['total']} obras")
        print('\nObteniendo las primeras 10...')

        obras_seleccionadas = []
        contador = 0

        for idx in respuesta['objectIDs']:
            obra = self.buscar_obra_por_idx(idx)
            if obra == None:
                obra = self.obtener_obra(idx)
                if obra == None:
                    continue

            if nombre.lower() in obra.artist.display_name.lower():
                obras_seleccionadas.append(obra)
                print(f'Obra {idx} obtenida...')
            else:
                print(f'Obra {idx} no fue almacenada porque no coincide con el criterio de búsqueda.')
            contador += 1

            if contador % 10 == 0:
                print('\nOBRAS OBTENIDAS:')
                for obra in obras_seleccionadas[contador-10:contador]:
                    print(f'{obra.idx} - Titulo: {obra.title}')
                ans = input('\n¿Desea obtener otras 10 obras? Si (s)/No (n): ').lower()
                while ans not in ['s', 'n']:
                    ans = input('Debe ingresar s o n: ')
                if ans == 'n':
                    return obras_seleccionadas

        return obras_seleccionadas

    def buscar_por_autor(self):
        """
        Interfaz interactiva para buscar obras por nombre de autor.
        """
        print('\nBÚSQUEDA POR NOMBRE DEL ARTISTA')

        artista_seleccionado = input('Ingrese el nombre del artista (minimo 3 caracteres): ').capitalize()

        if len(artista_seleccionado.strip()) < 3 or artista_seleccionado.strip() == "":
            print('Debe ingresar al menos 3 caracteres para el nombre del artista.')
            artista_seleccionado = input('Ingrese el nombre del artista (minimo 3 caracteres): ').capitalize()

        print(f'ARTISTA SELECCIONADO: {artista_seleccionado.upper()}')
        obras_seleccionadas = self.obtener_obras_por_nombre_autor(artista_seleccionado)
        print(f'\nOBRAS POR ARTISTA: {artista_seleccionado.upper()}')

        if len(obras_seleccionadas) == 0:
            print('No se han encontrado obras con el artista seleccionado...')
        else:
            for obra in obras_seleccionadas:
                print(obra.mostrar_general())
            
            self.mostrar_detalles(obras_seleccionadas)

    # BUSQUEDA POR NOMBRE DE AUTOR ##



    # ADICIONALES ##

    def mostrar_detalles(self, lista_obras):
        """
        Muestra los detalles de una obra seleccionada de una lista y permite visualizar su imagen si está disponible.

        Args:
            lista_obras (list): Lista de obras de las cuales seleccionar para ver detalles.
        """
        print('\n¿Desea ver los detalles de alguna de las obras?')
        ans = input('Si (s)/No (n): ').lower()

        while ans not in ['s','n']:
            print('Debe ingresar una opción válida: ')
            ans = input('Si (s)/No (n): ').lower()

        if ans == 'n':
            return

        while True:
            print('\nVER DETALLES DE LAS OBRAS')
            for i,obra in enumerate(lista_obras):
                print(f'{i+1}. {obra.mostrar_general()}')

            print(f'{len(lista_obras)+1}. Volver al menú')

            ans = input('\nIngrese el número de la opción deseada: ')
            while not ans.isnumeric() or int(ans) not in range(1,len(lista_obras)+2):
                print('\nDebe ingresar una opción válida')
                ans = input('Ingrese el número de la opción deseada: ')
            
            if int(ans) == len(lista_obras)+1:
                break
            else:
                obra_seleccionada = lista_obras[int(ans)-1]
                print(obra_seleccionada.mostrar_detalles())
                
                if obra_seleccionada.primary_image == "":
                    print('No se ha podido encontrar una imagen de la obra...')
                else:
                    print('¿Desea ver una imagen de la obra?')
                    ans = input('Si (s)/No (n): ').lower()
                    while ans not in ['s','n']:
                        print('Debe ingresar una opción válida: ')
                        ans = input('Si (s)/No (n): ').lower()
                    if ans == 's':
                        self.mostrar_imagen(obra_seleccionada.primary_image, obra_seleccionada.title)

    def mostrar_imagen(self, url, nombre_base):
        """
        Descarga y muestra la imagen de una obra desde la URL proporcionada.

        Args:
            url (str): URL de la imagen.
            nombre_base (str): Nombre base para guardar el archivo.
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            content_type = response.headers.get('Content-Type')
            extension = '.png'  # Valor por defecto
            if content_type:
                if 'image/png' in content_type:
                    extension = '.png'
                elif 'image/jpeg' in content_type:
                    extension = '.jpg'
                elif 'image/svg+xml' in content_type:
                    extension = '.svg'

            nombre_archivo_final = f"{nombre_base}{extension}"

            with open(nombre_archivo_final, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f'Imagen guardada exitosamente como "{nombre_archivo_final}"')

            img = Image.open(nombre_archivo_final)
            img.show()

        except Exception as e:
            print(f"Err: {e}")
        except IOError as e:
            print(f"Error al manejar el archivo: {e}")

    # ADICIONALES ##


    # MENU ##
    def buscar_obras(self):
        """
        Muestra un menú interactivo para elegir entre las diferentes formas de buscar obras.
        """
        while True:
            print('\nBÚSQUEDA DE OBRAS ')
            print('''
Seleccione el criterio de búsqueda que prefiera
Obtenga la cantidad de obras deseadas y revise sus detalles.
Si la obra cuenta con imagen disponible, también podrá visualizarla.
''')
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
        """
        Menú principal del programa que permite iniciar la búsqueda o salir.
        """
        self.cargar_departamentos()
        if len(self.departamentos) == 0:
            print('No se han logrado cargar los datos necesarios...')
            return
        
        print('\nBIENVENIDO/A AL MUSEO METROPOLITANO')
        print('\nIntegrantes: Erick Balasch - Isabel Gomez - Luis Nardone\n')
        while True:
            print('''
MENÚ PRINCIPAL
------------------------
1. Búsqueda de Obras
2. Salir
------------------------''')
                
            ans = input('Ingrese el número de la opción deseada: ')

            while not ans.isnumeric() or int(ans) not in range(1,4):
                print('Debe ingresar una opción válida')
                ans = input('Ingrese el número de la opción deseada: ')

            if ans == '1':
                self.buscar_obras()
            else:
                print('HASTA LUEGO')
                break
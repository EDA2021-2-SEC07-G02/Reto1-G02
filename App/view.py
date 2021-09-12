"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar cronológicamente los artistas")
    print("3- Listar cronológicamente las adquisiciones")
    print("4- Clasificar las obras de un artista por técnica")
    print("5- Clasificar las obras por la nacionalidad de sus creadores")
    print("6- Transportar obras de un departamento")
    print("7- Proponer una nueva exposición en el museo")
    print("0- Salir")

def printRepLista():
    """
    Opciones de representación de lista que se pueden escoger
    al seleccionar la opción (1) de cargar información al catálogo.
    La representación de lista posibles son: (1) ARRAY_LIST o (2)LINKED_LIST
    """
    print("\n¿Qué representación de lista desea para la carga del catálogo?")
    print("1- ARRAY_LIST")
    print("2- LINKED_LIST")

def initCatalog(ListType):
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog(ListType)



def loadData(catalog):
    """
    Carga los artistas en la estructura de datos
    """
    controller.loadData(catalog)


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        
        printRepLista()
        Tipo_Lista=int(input("Seleccione el tipo de representación de la lista: "))
        ListType="ARRAY_LIST" #Opción número 1. Asimismo, queda por defecto ARRAY_LIST en caso de que se haya digitado otra opción por equivocación
        if Tipo_Lista==2:
            ListType="LINKED_LIST"

        print("\n\nCargando información de los archivos con representación de lista: " + ListType + " .....")
        catalog = initCatalog(ListType)
        loadData(catalog)
        print('\nAutores cargados: ' + str(lt.size(catalog['artists'])))
        print('\nObras cargadas: ' + str(lt.size(catalog['artworks'])))
        ultimasTresObras=lt.subList(catalog['artworks'],lt.size(catalog['artworks'])-2,3)
        print('\nTres últimas obras: ')
        print('  ',lt.removeFirst(ultimasTresObras)['Title'])
        print('  ',lt.removeFirst(ultimasTresObras)['Title'])
        print('  ',lt.removeFirst(ultimasTresObras)['Title'])
        ultimosTresArtistas=lt.subList(catalog['artists'],lt.size(catalog['artists'])-2,3)
        print('\nTres últimos artistas: ')
        print('  ',lt.removeFirst(ultimosTresArtistas)['DisplayName'])
        print('  ',lt.removeFirst(ultimosTresArtistas)['DisplayName'])
        print('  ',lt.removeFirst(ultimosTresArtistas)['DisplayName'])
        

    elif int(inputs[0]) == 2:
        pass

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass

    elif int(inputs[0]) == 7:
        pass

    else:
        sys.exit(0)
sys.exit(0)

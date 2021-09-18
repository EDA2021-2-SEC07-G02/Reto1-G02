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

from time import process_time

import prettytable
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from prettytable import PrettyTable

default_limit = 1000 
sys.setrecursionlimit(default_limit*10)


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("-"*50)
    print("Bienvenido")
    print("Opciones:")
    print("1- Cargar información en el catálogo")
    print("2- Listar cronológicamente los artistas")
    print("3- Listar cronológicamente las adquisiciones")
    print("4- Clasificar las obras de un artista por técnica")
    print("5- Clasificar las obras por la nacionalidad de sus creadores")
    print("6- Transportar obras de un departamento")
    print("7- Proponer una nueva exposición en el museo")
    print("0- Salir")
    print("-"*50)

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

def printRepLista():
    """
    Opciones de representación de lista que se pueden escoger
    al seleccionar la opción (1) de cargar información al catálogo.
    La representación de lista posibles son: (1) ARRAY_LIST o (2)LINKED_LIST
    """
    print("\n¿Qué representación de lista desea para la carga del catálogo?")
    print("1- ARRAY_LIST")
    print("2- LINKED_LIST")

def printOrdIterativo():
    """
    Opciones de ordenamiento iterativativo que se pueden escoger
    al seleccionar las opciones: (3) listar cronológicamente las adquisiciones o
    (2) listar cronológicamente los artistas
    Los agloritmos de ordenamientos posibles son: (1) Insertion, (2)Shell, (3) Merge o (4) Quick Sorts
    """
    print("\n¿Cuál tipo de algoritmo de ordenamiento iterativo quiere escoger?")
    print("1- Insertion Sort")
    print("2- Shell Sort")
    print("3- Merge Sort")
    print("4- Quick Sort")

def tuplaOrdIterativo(opcion):
    """
    Esta función será usada en las opciones (2) y (3). 
    Su parámetro de entrada puede ser "opcion2" o "opcion3" dependiendo en que opción sea utilizado

    La función le pedirá al usuario dos datos:
    1. Un entero representando el tipo de algoritmo de ordenamiento deseado
    2. Un entero con el tamaño de la muestra que quiere ordenar

    Los retorno de la función será una tupla que contega:
    1. Un booleano que comprueba si el tamaño de la muestra no superá al tamaño del catalogo correspondiente a la opción
    2. Una cadena de str correspondiente al tipo de ordenamiento que quiere por el usuario.
    3. Entero que representa el tamaño de la lista
    """
    printOrdIterativo()
    Tipo_ord=int(input("\nSeleccione el tipo de algoritmo de ordenamiento: "))
    sortType=None 
    if Tipo_ord==1:
        sortType="Insertion"
    elif Tipo_ord==2:
        sortType="Shell"
    elif Tipo_ord==3:
        sortType="Merge"
    else:#Opción número 4. Asimismo, queda por defecto Quick Sort en caso de que se haya digitado otra opción por equivocación
        sortType="Quick"
    print("\nLa ordenación se hará con el tipo de ordenamiento "+sortType+" Sort")

    porcentaje=float(input("Ingrese el porcentaje de registros del total de registros a organizar:"))
    return sortType, porcentaje
    """
    fecha_inicio=(input("\nIngrese la fecha de inicio del rango (YYYY-MM-DD): "))
    #fecha_final=(input("\nIngrese la fecha final del rango (YYYY-MM-DD): "))

    #return sortType, fecha_inicio, fecha_final
    """





def printFirstLastsResultsArt(ord_artwork, cadenaOpcion, sample=3):
    """
    Esta función es usada para mostrar a las 3 primeras y últimas obras 
    en distintas opciones del view. 
    
    Los parámetros son:
    ord_artwork: Catalogo de obras de arte (Cargado por catalogo en la opción 1 o ordenado por fechas de la opción 3)
    sample: Hace referencia a la cantidad de primeras y últimas obras que se quieren mostrar al usuario.
    Su valor predeterminado es 3 por requisitos del proyecto.
    cadenaOpcion: Es usado para imprimir si las obras fueron cargadas o ordenadas 
    """
    size = lt.size(ord_artwork)
    print("\nLas "+ str(sample)+" primeras y últimas obras "+cadenaOpcion)
    artPretty=PrettyTable()
    artPretty.field_names=["ObjectID","Title","Medium","Dimensions","Date","DateAcquired","URL"]
    artPretty.align="l"
    artPretty._max_width = {"ObjectID" : 10, "Title" : 25,"Medium":15,"Dimensions":25,"Date":12,"DateAcquired":12,"URL":15}
    i=1
    while i <= sample:
        artwork = lt.getElement(ord_artwork,i)
        artPretty.add_row((artwork['ObjectID'],artwork['Title'],artwork['Medium'],
        artwork['Dimensions'],artwork['Date'],artwork['DateAcquired'],artwork['URL']))
        i+=1
    j=size-(sample)+1
    while j <= size:
        artwork = lt.getElement(ord_artwork,j)
        artPretty.add_row((artwork['ObjectID'],artwork['Title'],artwork['Medium'],
        artwork['Dimensions'],artwork['Date'],artwork['DateAcquired'],artwork['URL']))
        j+=1
    print(artPretty)

def printFirstLastsResultsArtists(ord_artist, cadenaOpcion, sample=3):
    """
    Esta función es usada para mostrar a los 3 primeros y últimos artistas 
    en distintas opciones del view. 
    
    Los parámetros son:
    ord_artist: Catalogo de artistas
    sample: Hace referencia a la cantidad de primeras y últimas artistas que se quieren mostrar al usuario.
    Su valor predeterminado es 3 por requisitos del proyecto.
    cadenaOpcion: Es usado para imprimir si los artistas fueron cargados al catalogo o ordenadas 
    """
    size = lt.size(ord_artist)
    print("\nLos "+ str(sample)+" primeros y últimos artistas "+cadenaOpcion)
    artistPretty=PrettyTable()
    artistPretty.field_names=["DisplayName","BeginDate","EndDate","Nationality","Gender"]
    artistPretty.align="l"
    artistPretty._max_width = {"DisplayName" : 25, "BeginDate" : 8,"EndDate":8,"Nationality":15,"Gender":12}
    i=1
    while i <= sample:
        artist = lt.getElement(ord_artist,i)
        artistPretty.add_row((artist['DisplayName'],artist['BeginDate'],artist['EndDate'],
        artist['Nationality'],artist['Gender']))
        i+=1
    j=size-(sample)+1
    while j <= size:
        artist = lt.getElement(ord_artist,i)
        artistPretty.add_row((artist['DisplayName'],artist['BeginDate'],artist['EndDate'],
        artist['Nationality'],artist['Gender']))
        j+=1
    print(artistPretty)

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if inputs.isnumeric() == True:
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
            print('Obras cargadas: ' + str(lt.size(catalog['artworks'])))
            printFirstLastsResultsArt(catalog['artworks'],"cargadas al catalogo son:")
            printFirstLastsResultsArtists(catalog['artists'],"cargados al catalogo son:")
            
        elif int(inputs[0]) == 2:
            tupEntradasUsuario=tuplaOrdIterativo("opcion2")
            if tupEntradasUsuario[0]==True:
                pass
            pass

        elif int(inputs[0]) == 3:
            tupEntradasUsuario=tuplaOrdIterativo("opcion3")
            sortType=tupEntradasUsuario[0]
            porcentaje=tupEntradasUsuario[1]
            #fechaInicio=tupEntradasUsuario[1]
            #fechaFinal=tupEntradasUsuario[2]
            
            resultado= controller.SortArtWork(catalog, sortType, porcentaje)
            #resultado= controller.SortArtWork(catalog, sortType, fechaInicio, fechaFinal)
            print("\nEl tiempo de ejecución (mseg) fue: "+str(resultado[0]))
            printFirstLastsResultsArt(resultado[1]," ordenadas por fecha son:")
            

        elif int(inputs[0]) == 4:
            pass

        elif int(inputs[0]) == 5:
            pass

        elif int(inputs[0]) == 6:
            pass

        elif int(inputs[0]) == 7:
            pass

        elif int(inputs[0]) == 0:
            sys.exit(0)
        else:
            print("Seleccione una opción válida") 
    else:
        print("Seleccione una opción válida")

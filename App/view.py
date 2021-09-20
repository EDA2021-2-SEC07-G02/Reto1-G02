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
from typing import Iterator

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
    # TODO: documentación
    print("-"*50)
    print("Bienvenido")
    print("Opciones:")
    print("0 - Cargar información en el catálogo")
    print("1 - Listar cronológicamente los artistas")
    print("2 - Listar cronológicamente las adquisiciones")
    print("3 - Clasificar las obras de un artista por técnica")
    print("4 - Clasificar las obras por la nacionalidad de sus creadores")
    print("5 - Transportar obras de un departamento")
    print("6 - Proponer una nueva exposición en el museo")
    print("7 - Salir")
    print("-"*50)

def initCatalog(ListType):
    # TODO: documentación parámetros
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog(ListType)

def loadData(catalog):
    # TODO: documentación parámetros
    """
    Carga los artistas en la estructura de datos
    """
    controller.loadData(catalog)

def printFirstLastsResultsArt(ord_artwork, cadenaOpcion, sample=3):
    # TODO: documentación pasar a formáto estándar, problema posible OutOfRange
    """
    Esta función es usada para mostrar a las 3 primeras y últimas obras 
    en distintas opciones del view. 
    
    Los parámetros son:
    ord_artwork: Catalogo de obras de arte (Cargado por catalogo en la opción 1 o ordenado por fechas de la opción 3)
    sample: Hace referencia a la cantidad de primeras y últimas obras que se quieren mostrar al usuario. Su valor predeterminado es 3 por requisitos del proyecto.
    cadenaOpcion: Es usado para imprimir si las obras fueron cargadas o ordenadas 
    """
    size = lt.size(ord_artwork)
    print("\nLas "+ str(sample)+" primeras y últimas obras "+cadenaOpcion)
    artPretty=PrettyTable()
    artPretty.field_names=["ObjectID","Title","Medium","Dimensions","Date","DateAcquired","URL","Artists Names"]
    artPretty.align="l"
    artPretty._max_width = {"ObjectID" : 10, "Title" : 15,"Medium":13,"Dimensions":15,"Date":12,"DateAcquired":11,"URL":10,"Artists Names":16}

    for i in list(range(sample))+list(range(size-sample,size)):
        artwork = lt.getElement(ord_artwork,i)
        dispname_artwork=(controller.getArtistName(catalog,artwork["ConstituentID"]))[0:-1]
        artPretty.add_row((artwork['ObjectID'],artwork['Title'],artwork['Medium'],
        artwork['Dimensions'],artwork['Date'],artwork['DateAcquired'],artwork['URL'],
        dispname_artwork))
    print(artPretty)

def printFirstLastsResultsArtists(ord_artist, cadenaOpcion, sample=3):
    # TODO: documentación parámetros, problema posible OutOfRange
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

    for i in list(range(sample))+list(range(size-sample,size)):
        artist = lt.getElement(ord_artist,i)
        artistPretty.add_row((artist['DisplayName'],artist['BeginDate'],artist['EndDate'],
        artist['Nationality'],artist['Gender']))
    print(artistPretty)

catalog = None

def printResultsArtworks(ord_artwork):
    artPretty=PrettyTable()
    artPretty.field_names=["ObjectID","Title","Medium","Dimensions","Date","DateAcquired","URL","Artists Names"]
    artPretty.align="l"
    artPretty._max_width = {"ObjectID" : 10, "Title" : 15,"Medium":13,"Dimensions":15,"Date":12,"DateAcquired":11,"URL":10,"Artists Names":16}

    for artwork in lt.iterator(ord_artwork):
        dispname_artwork=(controller.getArtistName(catalog,artwork["ConstituentID"]))[0:-1]
        artPretty.add_row((artwork['ObjectID'],artwork['Title'],artwork['Medium'],
        artwork['Dimensions'],artwork['Date'],artwork['DateAcquired'],artwork['URL'],
        dispname_artwork))
    print(artPretty)

def printMediums(ord_mediums,top=5):
    medPretty=PrettyTable()
    medPretty.field_names=["Tecnica","Cantidad"]
    medPretty.align="l"
    medPretty._max_width = {"Tecnica" : 15, "Cantidad" : 5}
    cont=0
    for tecnica in lt.iterator(ord_mediums):
        nombreTecnica=lt.getElement(tecnica,0)["Medium"]
        medPretty.add_row((nombreTecnica,str(lt.size(tecnica))))
        cont+=1
        if(cont>top):
            break
    print(medPretty)


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if inputs.isnumeric():
        # Opción 0: Carga de datos
        if int(inputs[0]) == 0:
            ListType="ARRAY_LIST" #Opción número 1. Asimismo, queda por defecto ARRAY_LIST en caso de que se haya digitado otra opción por equivocación
            print("\n\nCargando información de los archivos con representación de lista: " + ListType + " .....")
            catalog = initCatalog(ListType)
            loadData(catalog)
            print('\nAutores cargados: ' + str(lt.size(catalog['artists'])))
            print('Obras cargadas: ' + str(lt.size(catalog['artworks'])))
            printFirstLastsResultsArt(catalog['artworks'],"cargadas al catalogo son:")
            printFirstLastsResultsArtists(catalog['artists'],"cargados al catalogo son:")
        
        # Opción 1: Listar cronológicamente los artistas (Requerimiento 1)
        elif int(inputs[0]) == 1:
            pass

        # Opción 2: Listar cronológicamente las obras adquiridas (Requerimiento 2)
        elif int(inputs[0]) == 2:  
            fechaInicial=input("\nIngrese la fecha inicial: ")
            fechaFinal=input("\nIngrese la fecha final: ")
            resultado= controller.listarAdquisicionesCronologicamente(catalog, fechaInicial, fechaFinal)
            printFirstLastsResultsArt(resultado[0]," ordenadas por fecha son:")
            print("\nEl total de obras en el rango de fechas "+fechaInicial+" - "+fechaFinal+" es: "+str(resultado[1]))
            print("\nEl total de obras compradadas ('Purchase') en el rango de fechas "+fechaInicial+" - "+fechaFinal+" es: "+str(resultado[2]))
            
        # Opción 3: Clasificar las obras de un artista por técnica (Requerimiento 3)
        elif int(inputs[0]) == 3:
            nombreArtista=input("Ingrese el nombre del artista: ")
            respuesta=controller.tecnicasObrasPorArtista(catalog,nombreArtista)
            tecnicas=respuesta[0]
            totalObras=respuesta[1]
            if totalObras!=0:
                obrasTecnica=lt.getElement(tecnicas,0)
                tecnica=lt.getElement(obrasTecnica,0)["Medium"]
                print("El artista",str(nombreArtista),"tiene",totalObras,"obras en total. De las",lt.size(tecnicas),"ténicas empleadas la más utilizada es",\
                    str(tecnica)+".\n")
                print("La lista de las 5 técnica más utilizadas")
                printMediums(tecnicas)
                print("A continuación se presentan la lista de las obras realizadas con la técnica",str(tecnica)+":")
                printResultsArtworks(obrasTecnica)
            else:
                print("El artista",nombreArtista,"no existe en la base de datos o no tiene ninguna obra.")


        # Opción 4: Clasificar las obras por la nacionalidad de un artista (Requerimiento 4)
        elif int(inputs[0]) == 4:
            print("Cargando clasificación por nacionalidad de obras......")
            listaprovisional=controller.req4(catalog)
            print("tiempo de req4: ",listaprovisional[2])
            print("top10")
            for pais in lt.iterator(listaprovisional[0]):
                print(type(pais["Artworks"]))
                try:
                    print("Q: ",str(lt.size(pais["Artworks"]),"Nationality: ",pais["Nationality"])) ##modificar
                except:
                    print("Nationality: ",pais["Nationality"])
            print("primer lugar",listaprovisional[1]["Nationality"]," q: ",str(lt.size(listaprovisional[1]["Artworks"])))
            printFirstLastsResultsArt(listaprovisional[1]["Artworks"],"info primer lugar: ")
            listaprovisional=None ##Se borra la lista provisional

        # Opción 5: Transportar obras de un departamento (Requerimiento 5)
        elif int(inputs[0]) == 5:
            pass
        
        # Opción 6: Proponer una nueva exposición en el museo (Requerimiento 6)
        elif int(inputs[0]) == 6:
            pass

        # Opción 7: Salir
        elif int(inputs[0]) == 7:
            sys.exit(0)
        else:
            print("Seleccione una opción válida") 
    else:
        print("Seleccione una opción válida")

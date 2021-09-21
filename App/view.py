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

#from DISClib.DataStructures.arraylist import size
from time import process_time
from typing import Iterator

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import prettytable
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

    Párametros:
        ListType: Tipo de lista con la que se hará el catalogo (ARRAY_LIST o LINKED_LIST)

    Retorno:
        Catalogo inicializado
    """
    return controller.initCatalog(ListType)

def loadData(catalog):
    # TODO: documentación parámetros
    """
    Carga los artistas y obras en la estructura de datos
    
    Párametros:
        Catalog: Catalogo en donde se añadirán obras y artistas
    
    Retorno:
        Catalogo cardgado con obras y artistas
    """
    controller.loadData(catalog)

def printFirstLastsResultsArt(ord_artwork, cadenaOpcion, sample=3):
    # TODO: documentación pasar a formáto estándar, problema posible OutOfRange
    """
    Esta función es usada para mostrar a las 3 primeras y últimas obras 
    en distintas opciones del view. 
    
    Parámetros:
        ord_artwork: Catalogo de obras de arte (Cargado por catalogo en la opción 1 o ordenado por fechas de la opción 3)
        sample: Hace referencia a la cantidad de primeras y últimas obras que se quieren mostrar al usuario. 
                Su valor predeterminado es 3 por requisitos del proyecto.
        cadenaOpcion: Es usado para imprimir si las obras fueron cargadas o ordenadas 
    
    print(artPretty) >> Imprime la tabla
    controller.limpiarVar(artPretty) >> Borra la tabla hecha. Dato provisional
    """
    size = lt.size(ord_artwork)
    print("\nLas "+ str(sample)+" primeras y últimas obras "+cadenaOpcion)
    artPretty=PrettyTable(hrules=prettytable.ALL)
    artPretty.field_names=["ObjectID","Title","Artists Names","Medium",
                            "Dimensions","Date","DateAcquired","URL"]
    artPretty.align="l"
    artPretty._max_width = {"ObjectID" : 10, "Title" : 15,"Artists Names":16,"Medium":13,
                            "Dimensions":15,"Date":12,"DateAcquired":11,"URL":10}

    for i in list(range(sample))+list(range(size-sample,size)):
        artwork = lt.getElement(ord_artwork,i)
        dispname_artwork=(controller.getArtistName(catalog,artwork["ConstituentID"]))[0:-1]
        artPretty.add_row((artwork['ObjectID'],artwork['Title'],dispname_artwork,artwork['Medium'],
                        artwork['Dimensions'],artwork['Date'],artwork['DateAcquired'],artwork['URL']))
    print(artPretty)
    controller.limpiarVar(artPretty) #Se elimina la tabla dado que es un dato provisional

def printFirstLastsResultsArtists(ord_artist, cadenaOpcion, sample=3):
    # TODO: documentación parámetros, problema posible OutOfRange
    """
    Esta función es usada para mostrar a los 3 primeros y últimos artistas 
    en distintas opciones del view. 
    
    Parámetros:
        ord_artist: Catalogo de artistas
        sample: Hace referencia a la cantidad de primeras y últimas artistas que se quieren mostrar al usuario.
                Su valor predeterminado es 3 por requisitos del proyecto.
        cadenaOpcion: Es usado para imprimir si los artistas fueron cargados al catalogo o ordenadas 
    
    Print(artistPretty) >> Imprime la tabla
    controller.limpiarVar(artistPretty) >> Borra la tabla hecha. Dato provisional
    """
    size = lt.size(ord_artist)
    print("\nLos "+ str(sample)+" primeros y últimos artistas "+cadenaOpcion)
    artistPretty=PrettyTable(hrules=prettytable.ALL)
    artistPretty.field_names=["ConstituentID","DisplayName","BeginDate","Nationality",
                            "Gender","ArtistBio","Wiki QID","ULAN"]
    artistPretty.align="l"
    artistPretty._max_width = {"ConstituentID":7,"DisplayName":15, "BeginDate":8,
                                "Nationality":15,"Gender":12, "ArtistBio":15,"Wiki QID":10,"ULAN":15}

    for i in list(range(sample))+list(range(size-sample,size)):
        artist = lt.getElement(ord_artist,i)
        ArtistBio=artist["Nationality"]+"- Unknown"
        NacimientoInt=int(artist["BeginDate"])
        FallecimientoInt=int(artist["EndDate"])
        if NacimientoInt!=0: #se excluyen los artistas con fechas vacias/iguales a cero
            if FallecimientoInt==0 and NacimientoInt<1950: #Suponemos que si nacieron antes de 1950 ya fallecieron
                ArtistBio=artist["Nationality"]+", born "+artist['BeginDate']
            elif FallecimientoInt==0 and NacimientoInt>=1950:
                ArtistBio=artist["Nationality"]+", est. "+artist['BeginDate']
            else:
                ArtistBio=artist["Nationality"]+", "+artist['BeginDate']+" - "+artist['EndDate']
        artistPretty.add_row((artist['ConstituentID'], artist['DisplayName'],artist['BeginDate'],artist['Nationality'],
                            artist['Gender'],ArtistBio,artist['Wiki QID'],artist['ULAN']))
    print(artistPretty)
    controller.limpiarVar(artistPretty) #Se elimina la tabla dado que es un dato provisional


def printResultsArtworks(ord_artwork):
    # TODO: documentación y que de exactamente lo que da el requerimiento 3
    artPretty=PrettyTable(hrules=prettytable.ALL)
    artPretty.field_names=["ObjectID","Title","Medium","Dimensions","Date",
                            "DateAcquired","URL","Artists Names"]
    artPretty.align="l"
    artPretty._max_width = {"ObjectID" : 10, "Title" : 15,"Medium":13,"Dimensions":15,
                            "Date":12,"DateAcquired":11,"URL":10,"Artists Names":16}

    for artwork in lt.iterator(ord_artwork):
        dispname_artwork=(controller.getArtistName(catalog,artwork["ConstituentID"]))[0:-1]
        artPretty.add_row((artwork['ObjectID'],artwork['Title'],artwork['Medium'],
        artwork['Dimensions'],artwork['Date'],artwork['DateAcquired'],artwork['URL'],
        dispname_artwork))
    print(artPretty)

def printTableTransPricesArtworks(ord_artwork, sample=5):
    artPretty=PrettyTable(hrules=prettytable.ALL)
    artPretty.field_names=["ObjectID","Title","ArtistsNames","Medium",
                            "Date","Dimensions","Classification","TransCost (USD)","URL"]
    artPretty.align="l"
    artPretty._max_width = {"ObjectID" : 10, "Title" : 15,"ArtistsNames":13,"Medium":15,
                            "Date":12,"Dimensions":10,"Classification":11,"TransCost (USD)":11,"URL":10}
    for i in range(sample):
        artwork = lt.getElement(ord_artwork,i)
        dispname_artwork=(controller.getArtistName(catalog,artwork["ConstituentID"]))[0:-1]
        artPretty.add_row((artwork['ObjectID'],artwork['Title'],dispname_artwork,artwork['Medium'],
                            artwork['Date'],artwork['Dimensions'],artwork['Classification'],
                            round(artwork['TransCost (USD)'],3),artwork['URL'] ))
    print(artPretty)

def printMediums(ord_mediums,top=5):
    medPretty=PrettyTable(hrules=prettytable.ALL)
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

def printNationalityArt(ord_Nationality):
    """
    Imprime los resultados del requerimiento 4

    Parámetros:
        ord_Nationality:lista con países y sus obras de arte
    
    print(NationalityPretty) >> Imprime la tabla hecha por medio de PrettyTable
    controller.limpiarVar(NationalityPretty) >> Limpia la tabla hecha (dato provisional)
    """
    NationalityPretty=PrettyTable(hrules=prettytable.ALL)
    NationalityPretty.field_names=["Nationality","ArtWorks"]
    NationalityPretty.align="l"
    NationalityPretty._max_width = {"Nationality" : 15, "ArtWorks" : 5}
    for nationality in lt.iterator(ord_Nationality):
        NationalityPretty.add_row((nationality["Nationality"],nationality["Artworks"]["size"]))
    print(NationalityPretty)
    controller.limpiarVar(NationalityPretty)

def printFirstLastsResultsExpo(ord_artwork, sample=5):
    # TODO: documentación pasar a formáto estándar, problema posible OutOfRange
    """
    Esta función es usada para mostrar a las 5 primeras y últimas obras del requisito 6.
    
    Parámetros:
        ord_artwork: Catalogo de obras de arte de la exposición propuesta para el museo.
        sample: Hace referencia a la cantidad de primeras y últimas obras que se quieren mostrar al museo. 
                Su valor predeterminado es 5 por requisitos del proyecto.
    
    print(ExpoPretty) >> Imprime la tabla
    controller.limpiarVar(artPretty) >> Borra la tabla hecha. Dato provisional
    """
    size = lt.size(ord_artwork)
    print("\nLas "+ str(sample)+" primeras y últimas obras propuestas para el MOMA son: ")
    ExpoPretty=PrettyTable(hrules=prettytable.ALL)
    ExpoPretty.field_names=["i","ObjectID","Title","Artists Names","Medium",
                            "Dimensions","Date","DateAcquired","Classification","EstArea (m^2)", "URL"]
    ExpoPretty.align="l"
    ExpoPretty._max_width = {"i":3,"ObjectID" : 10, "Title" : 15,"Artists Names":16,"Medium":13,
                            "Dimensions":15,"Date":12,"DateAcquired":11,"Classification":10,"EstArea (m^2)":6, "URL":10}
    posiciones=list(range(sample))+list(range(size-sample,size))
    for i in posiciones:
        artwork = lt.getElement(ord_artwork,i)
        dispname_artwork=(controller.getArtistName(catalog,artwork["ConstituentID"]))[0:-1]
        ExpoPretty.add_row((i,artwork['ObjectID'],artwork['Title'],dispname_artwork,artwork['Medium'],
                        artwork['Dimensions'],artwork['Date'],artwork['DateAcquired'],artwork["Classification"], round(artwork["EstArea (m^2)"],3),artwork['URL']))
    print(ExpoPretty)
    controller.limpiarVar(ExpoPretty)
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
            fechaInicial=input("\nIngrese el año inicial: ")
            fechaFinal=input("\nIngrese el año final: ")
            resultado= controller.listarArtistasCronologicamente(catalog, fechaInicial, fechaFinal)
            printFirstLastsResultsArtists(resultado[0]," ordenadas por año son:")
            print("\nEl total de artistas en el rango de fechas "+fechaInicial+" - "+fechaFinal+" es: "+str(resultado[1]))
            controller.limpiarVar(resultado)  #Se borra el resultado - Dato provisional

        # Opción 2: Listar cronológicamente las obras adquiridas (Requerimiento 2)
        elif int(inputs[0]) == 2:  
            fechaInicial=input("\nIngrese la fecha inicial: ")
            fechaFinal=input("\nIngrese la fecha final: ")
            resultado= controller.listarAdquisicionesCronologicamente(catalog, fechaInicial, fechaFinal)
            printFirstLastsResultsArt(resultado[0]," ordenadas por fecha son:")
            print("\nEl total de obras en el rango de fechas "+fechaInicial+" - "+fechaFinal+" es: "+str(resultado[1]))
            print("\nEl total de obras compradadas ('Purchase') en el rango de fechas "+fechaInicial+" - "+fechaFinal+" es: "+str(resultado[2]))
            controller.limpiarVar(resultado) #Se borra el resultado - Dato provisional
            
        # Opción 3: Clasificar las obras de un artista por técnica (Requerimiento 3)
        elif int(inputs[0]) == 3:
            nombreArtista=input("\nIngrese el nombre del artista: ")
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
            print("Top 10 nacionalidades de acuerdo a su cantidad de obras de arte")
            printNationalityArt(listaprovisional[0])
            print("-"*25 + " Primer lugar " +"-"*25)
            print("\nPrimer lugar: \nNacionalidad: ",listaprovisional[1]["Nationality"],"\nCantidad obras: ",str(lt.size(listaprovisional[1]["Artworks"])))
            printFirstLastsResultsArt(listaprovisional[1]["Artworks"],"de arte del primer lugar son: ")
            controller.limpiarVar(listaprovisional) ##Se borra la lista provisional

        # Opción 5: Transportar obras de un departamento (Requerimiento 5)
        elif int(inputs[0]) == 5:
            nombreDepartamento=input("\nIngrese el nombre del departamento: ")
            respuesta=controller.transportarObrasDespartamento(catalog,nombreDepartamento)
            listaObrasDepartamentoPrecio=respuesta[0]
            listaObrasDepartamentoAntiguedad=respuesta[1]
            precioTotal=respuesta[2]
            pesoTotal=respuesta[3]
            print("MoMA trasnportará",lt.size(listaObrasDepartamentoPrecio),"obras del departamento de",nombreDepartamento)
            print("\nEl peso total estimado es",str(pesoTotal)+"kg")
            print("El precio estimado de transportar todas las obras del departamento es",str(precioTotal)+"USD")
            print("\nTOP 5 de las obras más costosas de transportar")
            printTableTransPricesArtworks(listaObrasDepartamentoPrecio)
            print("\nTOP 5 de las obras más antiguas a transportar")
            printTableTransPricesArtworks(listaObrasDepartamentoAntiguedad)
            pass
        
        # Opción 6: Proponer una nueva exposición en el museo (Requerimiento 6)
        elif int(inputs[0]) == 6:
            areaExpo=float(input("Ingrese el área total disponible (m^2): "))
            fechaInicial=int(input("Ingrese el año inicial: "))
            fechaFinal=int(input("Ingrese el año final: "))
            print("Eligiendo obras de arte para la exposición........")
            resultado=controller.expoEpocaArea(catalog,areaExpo,fechaInicial,fechaFinal)
            print("\nÁrea utilizada por las obras: ",resultado[1])
            print("Total de obras: ",resultado[0])
            printFirstLastsResultsExpo(resultado[2])

        # Opción 7: Salir
        elif int(inputs[0]) == 7:
            sys.exit(0)
        else:
            print("Seleccione una opción válida") 
    else:
        print("Seleccione una opción válida")

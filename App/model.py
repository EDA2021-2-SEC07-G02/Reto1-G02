"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.arraylist import subList
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import quicksort as qs
import time
assert cf



# Construccion de modelos

def newCatalog(ListType):
    """
    Inicializa el catálogo. Se crea dos listas vacía, una para guardar a los artistas, otra para las obras de arte.
    
    Parámetro ListType: La representación de las listas que fue escogida por el usuario(ARRAY_LIST o LINKED_LIST)
    """
    catalog = {'artists': None,
               'artworks': None}

    catalog['artists'] = lt.newList(ListType)
    
    catalog['artworks'] = lt.newList(ListType)

    return catalog

# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):
    """
    Se agrega el artista entregado por parámetro en la última posición de la lista de artistas del catalogo.
    """
    lt.addLast(catalog['artists'], artist)

def addArtwork(catalog, artwork):
    """
    Se agrega la obra entregada por parámetro en la última posición de la lista de obras del catalogo.
    """
    lt.addLast(catalog['artworks'], artwork)


# Funciones para creacion de datos



# # Funciones de consulta

def getArtistName(catalog,ConstituentID): #req 2, 4
    """
    Se retornara una tupla con dos elementos, una cadena de texto con los nombres de los artistas y 
    una lista con sus nacionalidades.
    """
    codigoNum=ConstituentID[1:-1]
    dispname=""
    if "," in ConstituentID:
        codigoNum=codigoNum.split(",")
        for codigo in codigoNum:
                for artist in lt.iterator(catalog['artists']):
                    if codigo.strip()==artist["ConstituentID"].strip():
                        dispname+=artist["DisplayName"]+","
                        # lt.addLast(nationality,artist["Nationality"])
    else:
        for artist in lt.iterator(catalog['artists']):
            if codigoNum==artist["ConstituentID"]:
                dispname+= artist["DisplayName"] +","
    return dispname

########## req4
def getNationality(catalog,ConstituentID):
    """
    Se retornara las nacionalidades de los artistas.
    """
    codigoNum=ConstituentID[1:-1]
    nationality=""
    for artist in lt.iterator(catalog['artists']):
        if codigoNum.strip()==artist["ConstituentID"].strip():
            nationality=artist["Nationality"]
    
    return nationality
    # if "," in ConstituentID:
    #     codigoNum=codigoNum.split(",")
    #     for codigo in codigoNum:
    #             for artist in lt.iterator(catalog['artists']):
    #                 if codigo.strip()==artist["ConstituentID"].strip():
    #                     return artist["Nationality"]
    #                     #lt.addLast(nationality.append(artist["Nationality"])) ##modificar despuessss
    #                     # lt.addLast(nationality,artist["Nationality"])
    # else:
    #     for artist in lt.iterator(catalog['artists']):
    #         if codigoNum==artist["ConstituentID"]:
    #             return artist["Nationality"]
                

def newNationality(pais):
    adding={"Nationality":"","Cantidad":0}
    adding["Nationality"]=pais
    adding["Cantidad"]=1
    return adding

def addNationality(countries,nationality):
    """
    Se agregaran las nacionalidades a una lista provisional.
    """
    posNationality=lt.isPresent(countries,nationality)
    if posNationality>0:
        cantidad=lt.getElement(countries,posNationality)["Cantidad"]
        info={"Nationality":nationality,"Cantidad":cantidad+1}
        lt.changeInfo(countries,posNationality,info)
    else:
        pais=newNationality(nationality)
        lt.addLast(countries,pais)

def compareNationalities(name, nationality):
    if (name == nationality['Nationality']):
        return 0
    #elif (name > tag['name']):
     #   return 1
    return -1

def req4(catalog):
    """
    Lista provisional: Nacionalidades de las obras y la cantidad de veces que se repiten
    """
    countries=lt.newList("ARRAY_LIST",cmpfunction=compareNationalities)
    for obra in lt.iterator(catalog["artworks"]):
        conID=obra["ConstituentID"]
        if "," in conID:
            codigoNum=conID.split(",")
            for codigo in codigoNum:
                nationality= getNationality(catalog,codigo)
                addNationality(countries,nationality)
        else:
            nationality= getNationality(catalog,conID)
            addNationality(countries,nationality)
    return countries
# Funciones utilizadas para comparar elementos dentro de una lista

def cmpArtworkByDateAcquired(artwork1, artwork2): 
    """ 
    Devuelve verdadero (True) si el 'DateAcquired' de artwork1 es menores que el de artwork2 
    Args: artwork1: informacion de la primera obra que incluye su valor 'DateAcquired'
    artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired'
    """
    comparacion=False
    if len(artwork1["DateAcquired"])>0 and len(artwork2["DateAcquired"])>0: #La función dará False si la lista es vacía o posee un formato de fecha distinto, es decir fecha de artwork2 < artwork1
        fecha1=time.strptime(artwork1["DateAcquired"],"%Y-%m-%d")
        fecha2=time.strptime(artwork2["DateAcquired"],"%Y-%m-%d")
        comparacion=fecha1<fecha2
    return comparacion

# Funciones de ordenamiento

# def sortArtwork(catalog,sortType,porcentaje):
#     """
#     Esta función permite ordernar las obras de arte (Artwork) dependiendo del tipo de ordenamiento
#     iterativo deseado (Insertion, Shell, Merge o Quick Sorts). Esta función está adaptada a las pruebas
#     de laboratorio ya que realmente el tamaño de la muestra está dado el rango de fechas seleccionado
#     Args: catalog: estructura de datos con toda la información
#     sortType: string con el tipo de ordenamiento seleccionado por le usuario
#     procentaje: porcentaje de cantidad de registros de la lista total de registros a organizar
#     """
#     start_time = time.process_time()
#     cantidad_registros= ((porcentaje/100)*lt.size(catalog['artworks']))//1
#     subLista=lt.subList(catalog['artworks'],0,cantidad_registros)
#     if sortType == "Insertion":
#         sorted_list= ins.sort(subLista,cmpArtworkByDateAcquired)
#     elif sortType == "Shell":
#         sorted_list= sa.sort(subLista,cmpArtworkByDateAcquired)
#     elif sortType == "Merge":
#         sorted_list= ms.sort(subLista,cmpArtworkByDateAcquired)
#     elif sortType == "Quick":
#         sorted_list= qs.sort(subLista, cmpArtworkByDateAcquired)
    
#     med_time = time.process_time() # BORRAR
#     elapsed_time_mseg = (med_time - start_time)*1000 # BORRAR
#     print("TIEMPO DURACIÓN ORDENAMIENTO: ",elapsed_time_mseg) # BORRAR
#     print("TAMANO DE MUESTRA", lt.size(subLista))

#     stop_time = time.process_time()
#     elapsed_time_mseg = (stop_time - start_time)*1000
#     return elapsed_time_mseg, sorted_list

# NOTA: Esta función es la que está en implementación para la entrega final del reto.
def sortArtworkV1(catalog,sortType,fechaInicial,fechaFinal):
    """
    Esta función permite ordernar las obras de arte (Artwork) dependiendo del tipo de ordenamiento
    iterativo deseado (Insertion, Shell, Merge o Quick Sorts).
    Args: catalog: estructura de datos con toda la información
    sortType: string con el tipo de ordenamiento seleccionado por le usuario
    fechaInicial: fecha de inicio del rango
    fechaFinal: fecha final del rango de obras de arte
    """
    start_time = time.process_time()
    if sortType == "Insertion":
        sorted_list= ins.sort(catalog['artworks'],cmpArtworkByDateAcquired)
    elif sortType == "Shell":
        sorted_list= sa.sort(catalog['artworks'],cmpArtworkByDateAcquired)
    elif sortType == "Merge":
        sorted_list= ms.sort(catalog['artworks'],cmpArtworkByDateAcquired)
    elif sortType == "Quick":
        sorted_list= qs.sort(catalog['artworks'], cmpArtworkByDateAcquired)
    
    med_time = time.process_time() # BORRAR
    elapsed_time_mseg = (med_time - start_time)*1000 # BORRAR
    print("TIEMPO DURACIÓN ORDENAMIENTO: ",elapsed_time_mseg) # BORRAR

    cont=0
    while cmpArtworkByDateAcquired(lt.getElement(sorted_list,cont),{"DateAcquired":fechaInicial}) and cont<lt.size(sorted_list):
        cont+=1
    indiceInicial=cont+1
    while cmpArtworkByDateAcquired(lt.getElement(sorted_list,cont),{"DateAcquired":fechaFinal}) and cont<lt.size(sorted_list):
        cont+=1
    indiceFinal=cont
    print(indiceInicial, indiceFinal)
    if(indiceInicial<=indiceFinal):
        sub_list = lt.subList(sorted_list, indiceInicial, indiceFinal-indiceInicial) 
        sub_list = sub_list.copy()
        sorted_list=sub_list
    else:
        sorted_list=None   
    
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

def sortArtwork(catalog,sortType,fechaInicial,fechaFinal):
    """
    La función primero agregará a una lista provisional (rango) las obras que tenga 
    una fecha de aquisición dentro del rango deseado. A su vez, se irá 
    contando cuantas de estas obras se adquirieron por "Purchase" o compra del museo,
    además se tendrá un contador del total de obras dentro del rango de fechas.
    Después de esto se hará un ordenamiento con insertation a la lista provisional (rango)
    
    """
    start_time = time.process_time()
    sorted_list=lt.newList("ARRAY_LIST") #Se agregarán obras que tengan una fecha de adquisión en el rango deseado
    fechaInicialTi= time.strptime(fechaInicial,"%Y-%m-%d")
    fechaFinalTi= time.strptime(fechaFinal,"%Y-%m-%d")
    contadorRango=0
    contadorPurchase=0
    for obra in lt.iterator(catalog["artworks"]):
        if len(obra["DateAcquired"])==10: #Se ignoran las fechas vacías
            fecha=time.strptime(obra["DateAcquired"],"%Y-%m-%d")
            if fecha>fechaInicialTi and fecha<fechaFinalTi: 
                contadorRango+=1
                lt.addLast(sorted_list,obra) #se agregan fechas que estén dentro del rango deseado
            if obra["CreditLine"].startswith("Purchase"):
                contadorPurchase+=1
    
    ins.sort(sorted_list,cmpArtworkByDateAcquired) #ordenamiento por insertion
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg,sorted_list,contadorRango,contadorPurchase
    


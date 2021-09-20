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
    # TODO: Documentación return
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
    # TODO: Documentación parámetros
    """
    Se agrega el artista entregado por parámetro en la última posición de la lista de artistas del catalogo.
    """
    lt.addLast(catalog['artists'], artist)

def addArtwork(catalog, artwork):
    # TODO: Documentación parámetros y return
    """
    Se agrega la obra entregada por parámetro en la última posición de la lista de obras del catalogo.
    """
    lt.addLast(catalog['artworks'], artwork)

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpArtworkByDateAcquired(artwork1, artwork2):
    """ 
    Compara las fechas de dos obras de arte
    Parámetros: 
        artwork1: informacion de la primera obra que incluye su valor 'DateAcquired'
        artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired'
    Retorno:
        Devuelve verdadero (True) si artwork1 es menor en fecha que artwork2, si tienen la misma 
        fecha retorna falso (False)
    """
    comparacion=False
    if len(artwork1["DateAcquired"])>0 and len(artwork2["DateAcquired"])>0: #La función dará False si la lista es vacía o posee un formato de fecha distinto, es decir fecha de artwork2 < artwork1
        fecha1=time.strptime(artwork1["DateAcquired"],"%Y-%m-%d")
        fecha2=time.strptime(artwork2["DateAcquired"],"%Y-%m-%d")
        comparacion=fecha1<fecha2
    return comparacion

# Funciones de ordenamiento

def sortList(lista,cmpFunction):
    # TODO: documentación
    return ins.sort(lista,cmpFunction)

# Funciones de Consulta

def listarAdquisicionesCronologicamente(catalog,fechaInicial,fechaFinal):
    # TODO: documentación parámetros y return
    """
    La función primero agregará a una lista provisional (rango) las obras que tenga 
    una fecha de aquisición dentro del rango deseado. A su vez, se irá 
    contando cuantas de estas obras se adquirieron por "Purchase" o compra del museo,
    además se tendrá un contador del total de obras dentro del rango de fechas.
    Después de esto se hará un ordenamiento con insertation a la lista provisional (rango)
    
    """
    lista=lt.newList("ARRAY_LIST") #Se agregarán obras que tengan una fecha de adquisión en el rango deseado
    fechaInicialTi= time.strptime(fechaInicial,"%Y-%m-%d")
    fechaFinalTi= time.strptime(fechaFinal,"%Y-%m-%d")
    contadorRango=0
    contadorPurchase=0
    for obra in lt.iterator(catalog["artworks"]):
        if len(obra["DateAcquired"])==10: #Se ignoran las fechas vacías
            fecha=time.strptime(obra["DateAcquired"],"%Y-%m-%d")
            if fecha>fechaInicialTi and fecha<fechaFinalTi: 
                contadorRango+=1
                lt.addLast(lista,obra) #se agregan fechas que estén dentro del rango deseado
            if obra["CreditLine"].startswith("Purchase"):
                contadorPurchase+=1
    
    sortedList=sortList(lista,cmpArtworkByDateAcquired) #ordenamiento por insertion
    return sortedList, contadorPurchase, contadorRango


def getArtistName(catalog,ConstituentID): #req 2, 4
    # TODO: documentación parámetros y return
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
    # TODO: documentación parámetros retorno
    """
    Se retornara las nacionalidades de los artistas.
    """
    codigoNum=ConstituentID[1:-1]
    nationality=None
    for artist in lt.iterator(catalog['artists']):
        if codigoNum.strip()==artist["ConstituentID"].strip():
            nationality=artist["Nationality"]
    
    return nationality
            
def NewNationalityArt(pais,artwork):
    # TODO: documentación
    adding={"Nationality":"","Cantidad":0,"Artworks": lt.newList("ARRAY_LIST",cmpNationalities)}
    adding["Nationality"]=pais
    adding["Cantidad"]=1
    lt.addLast(adding["Artworks"],artwork)
    return adding


def addNationality(countries,nationality,artwork):
    # TODO: documentación parámetros retorno
    """
    Se agregaran las nacionalidades con sus respectivas obras a una lista provisional.
    """
    posNationality=lt.isPresent(countries,nationality)
    if posNationality>0: ### ARREGLAR
        cantidad=lt.getElement(countries,posNationality)["Cantidad"]
        artworksprevios=lt.getElement(countries,posNationality)["Artworks"]
        artworkAdd=lt.addLast(artworksprevios,artwork)
        # lt.changeInfo(countries,posNationality,info)
    else:
        pais=NewNationalityArt(nationality,artwork)
        lt.addLast(countries,pais)

def compareNationalities(name, nationality):
    # TODO: documentación parámetros retorno
    """
    Cmpfunction de lista provisional
    """
    if (name == nationality['Nationality']):
        return 0
    #elif (name > tag['name']):
     #   return 1
    return -1

def cmpNationalities(nacionalidad1,nacionalidad2):
    # TODO: documentación descripción parámetros
    """
    Retorna True cuando la primera nacionalidad tiene mayor cantidad de obras que la segunda.
    De lo contario, False.
    """
    return nacionalidad1["Cantidad"]>nacionalidad2["Cantidad"]

def req4(catalog):
    # TODO: documentación parámetros
    """
    Listas provisionales: 
    1. countries: Nacionalidades de las obras y la cantidad de veces que se repiten
    2. obrascountries: Lista de obras por cada nacionalidad

    Retornos:
    Top10 nacionalidades
    Obras por nacionalidad del primer lugar
    """
    start_time = time.process_time()
    countries=lt.newList("ARRAY_LIST",cmpfunction=compareNationalities)
    #obrascountries=lt.newList("ARRAY_LIST",cmpfunction=compareNationalities)# completarrrr
    for obra in lt.iterator(catalog["artworks"]):
        conID=obra["ConstituentID"]
        if "," in conID:
            codigoNum=conID.split(",")
            for codigo in codigoNum:
                nationality= getNationality(catalog,codigo)
                addNationality(countries,nationality,obra)
        else:
            nationality= getNationality(catalog,conID)
            addNationality(countries,nationality,obra)
    
    sort=ins.sort(countries,cmpNationalities)
    primerlugar=lt.getElement(sort,1)
    top10=lt.subList(sort,1,10)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000


    return top10,primerlugar,elapsed_time_mseg

###fin req 4

#Requerimiento 3
def tecnicasObrasPorArtista(catalog,nombre):
    constituentID=-1
    obras=lt.newList()
    tecnicas={}
    for artista in lt.iterator(catalog["artists"]):
        if nombre==artista["DisplayName"]:
            constituentID=artista["ConstituentID"]
    for obraArte in lt.iterator(catalog["artists"]):
        if str(constituentID) in obraArte["ConstituentID"].strip("[]").split(","):
            lt.addLast(obras,obraArte)
    for obraArtista in lt.iterator(obraArte):
        if obraArtista["Medium"] in tecnicas:
            lt.addLast(tecnicas[obraArtista["Medium"]],obraArtista)
        else:
            tecnicas[obraArtista["Medium"]]=lt.newList()
    print(tecnicas)

    
    




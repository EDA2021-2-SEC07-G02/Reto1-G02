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
import sys
assert cf

# Constantes

PRECIO_ENVIO_UNIDAD=72
PRECIO_ENVIO_FIJO=48

# Construccion de modelos

def newCatalog(ListType):
    # TODO: Documentación return
    """
    Inicializa el catálogo. Se crea dos listas vacía, una para guardar a los artistas, otra para las obras de arte.
    
    Parámetros:
        ListType: La representación de las listas que fue escogida por el usuario(ARRAY_LIST o LINKED_LIST)

    Retorno:
        catalog: Catalogo inicializado
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
    Párametros:
        catalog: catalogo de artistas y obras
        artist: artista a añadir
    
    Se añade el artista en la última posición del catalogo con lt.addLast() 
    """
    lt.addLast(catalog['artists'], artist)

def addArtwork(catalog, artwork):
    """
    Se agrega la obra entregada por parámetro en la última posición de la lista de obras del catalogo.
    Párametros:
        catalog: catalogo de artistas y obras
        artist: artista a añadir
    
    Se añade el artista en la última posición del catalogo con lt.addLast() 

    """
    lt.addLast(catalog['artworks'], artwork)

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpArtistDate(artist1,artist2): #req 1
    """
    Compara la fecha de dos artistas
    Parámetros: 
        artist1: informacion del primer artista y su valor 'BeginDate'
        artist1: informacion del primer artista y su valor 'BeginDate'
    Retorno:
        Devuelve verdadero (True) si artist1 es menor en fecha que artist2, de lo contrario (False)
    """
    if artist1["BeginDate"]==artist2["BeginDate"]: #se verifica si nacieron en el mismo año
        #se pasa a comparar por su fecha de fallecimiento.
        comparacion=artist1["EndDate"]<=artist2["EndDate"] #true si el artist1 falleció antes (o en el mismo año) que artist2
    else:
        comparacion=artist1["BeginDate"]<artist2["BeginDate"]
    return comparacion

def cmpArtworkByDateAcquired(artwork1, artwork2): #req 2
    """ 
    Compara las fechas de dos obras de arte
    Parámetros: 
        artwork1: informacion de la primera obra que incluye su valor 'DateAcquired'
        artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired'
    Retorno:
        Devuelve verdadero (True) si artwork1 es menor en fecha que artwork2, si tienen la misma 
        fecha retorna falso (False)
    """
    fecha1=time.strptime(artwork1["DateAcquired"],"%Y-%m-%d")
    fecha2=time.strptime(artwork2["DateAcquired"],"%Y-%m-%d")
    comparacion=fecha1<fecha2
    return comparacion

def cmpArtworkByPrice(obra1,obra2): # req 5
    if obra1["TransCost (USD)"]>obra2["TransCost (USD)"]: # orden descendentes
        return True
    else:
        return False

def cmpArtworkByDate(obra1,obra2): # req 5
    comparacion=obra1["Date"]<obra2["date"]
    return comparacion


    
# Funciones de ordenamiento

def sortList(lista,cmpFunction):
    """
    Función de ordenamiento con insertation que se usará en distintos requerimientos
    Parámetros: 
        lista: lista que se ordenara
        cmpFunction: función de comparación
    Retorno:
        lista ordenada por insertion
    """
    return ins.sort(lista,cmpFunction)

# Funciones de Consulta

def listarArtistasCronologicamente(catalog,fechaInicial,fechaFinal): #req1
    """
    Esta función se usará para el Requerimiento 2. Primero agregarán los artistas
    a una nueva array list (ListaNac) dependiendo un rango de fechas ingresado por el usuario
    que representa la fecha de nacimiento (fechaInicial) y la fecha de fallecimiento
    del artista (fechaFinal).
    Al mismo tiempo contará cuantos artistas hay en el rango de fechas deseado.
    
    Parámetros: 
        catalog: catalogo con obras y artistas
        fechaInicial: fecha inicial ingresada por el usuario
        fechaFinal: fecha final ingresada por el usuario
    
    Retorno:
        sortedList: lista de obras ordenada cronologicamente 
        contadorArtistas: número de artistas en el rango de fechas deseado
    """
    listaNac=lt.newList("ARRAY_LIST") #Se agregarán artistas que estén en el rango adecuado
    contador=0
    for artist in lt.iterator(catalog["artists"]):
        if len(artist["BeginDate"])==4: #Se ignoran si su fecha de nacimiento es vacía
            nacimiento=int(artist["BeginDate"])
            fallecimiento=int(artist["EndDate"])
            #"BeginDate","EndDate"
            if (nacimiento>= fechaInicial and nacimiento<=fechaFinal) and (fallecimiento<=fechaFinal):
                lt.addLast(listaNac,artist)
                contador+=1
    sortList(listaNac,cmpArtistDate)
    return listaNac,contador

def listarAdquisicionesCronologicamente(catalog,fechaInicial,fechaFinal):
    # TODO: documentación parámetros y return
    """
    La función primero agregará a una nueva array list (listaAdq) las obras que tengan
    una fecha de aquisición dentro del rango deseado. A su vez, se va a ir 
    contando cuantas de estas obras se adquirieron por "Purchase" o compra del museo,
    además se tendrá un contador del total de obras dentro del rango de fechas.
    Después de esto se hará un ordenamiento con insertion a listaAdq.

    Parámetros: 
        catalog: catalogo con obras y artistas
        fechaInicial: fecha inicial ingresada por el usuario
        fechaFinal: fecha final ingresada por el usuario
    Retorno:
        sortedList: lista de obras ordenada cronologicamente 
        contadorPurchase: entero que representa las obras compradas (purchase)dentro
        del rango de fechas 
        contadorRango: total de obras en el rango de fechas
    """
    listaAdq=lt.newList("ARRAY_LIST") #Se agregarán obras que tengan una fecha de adquisión en el rango deseado
    fechaInicialTi= time.strptime(fechaInicial,"%Y-%m-%d")
    fechaFinalTi= time.strptime(fechaFinal,"%Y-%m-%d")
    contadorRango=0
    contadorPurchase=0
    for obra in lt.iterator(catalog["artworks"]):
        if len(obra["DateAcquired"])==10: #Se ignoran las fechas vacías
            fecha=time.strptime(obra["DateAcquired"],"%Y-%m-%d")
            if fecha>fechaInicialTi and fecha<fechaFinalTi: 
                contadorRango+=1
                lt.addLast(listaAdq,obra) #se agregan fechas que estén dentro del rango deseado
            if obra["CreditLine"].startswith("Purchase"):
                contadorPurchase+=1
    
    sortList(listaAdq,cmpArtworkByDateAcquired) #ordenamiento por insertion
    return listaAdq, contadorPurchase, contadorRango


def getArtistName(catalog,ConstituentID): #req 2
    # TODO: documentación parámetros y return
    """
    Se retornara el nombre de un artista de acuerdo a su ConstituentID.
    Parámetros: 
        catalog: catalogo con obras y artistas
        ConstituentID: código del artista. Relaciona a una obra dentro del catalogo["artworks"]
        con su artista correspondiente en catalogo["DisplayName"]
    Retorno:
        dispname: cadena de texto con el/los nombre/s de los artistas
    """
    codigoNum=ConstituentID[1:-1]
    dispname=""
    if "," in ConstituentID: #Significa que hay más de un artista en el ConstituentID
        codigoNum=codigoNum.split(",") #Hace split de la cadena de texto con los distintos códigos
        for codigo in codigoNum:
                for artist in lt.iterator(catalog['artists']):
                    if codigo.strip()==artist["ConstituentID"].strip():
                        dispname+=artist["DisplayName"]+","
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
    lt.addLast(adding["Artworks"],artwork)
    return adding


def addNationality(countries,nationality,artwork):
    # TODO: documentación parámetros retorno
    """
    Se agregaran las nacionalidades con sus respectivas obras a una lista provisional.
    """
    posNationality=lt.isPresent(countries,nationality)
    if posNationality>0: ### ARREGLAR
        artworksprevios=lt.getElement(countries,posNationality)["Artworks"]
        lt.addLast(artworksprevios,artwork)
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
    return nacionalidad1["Artworks"]["size"]>nacionalidad2["Artworks"]["size"]

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
    for obra in lt.iterator(catalog["artworks"]):
        conID=obra["ConstituentID"]
        if "," in conID:
            codigoNum=conID.split(",")
            for codigo in codigoNum: #Se hace un recorrido cuando una obra fue hecha por más de un autor
                nationality= getNationality(catalog,codigo)
                addNationality(countries,nationality,obra)
        else:
            nationality= getNationality(catalog,conID)
            addNationality(countries,nationality,obra)
    
    sortList(countries,cmpNationalities)
    primerlugar=lt.getElement(countries,1)
    top10=lt.subList(countries,1,10)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000


    return top10,primerlugar,elapsed_time_mseg

###fin req 4

#Requerimiento 5

def transportarObrasDespartamento(catalog,departamento):
    obrasDepartamento=lt.newList()
    precioTotalEnvio=0
    peso=0
    for obra in lt.iterator(catalog["artwork"]):
        if str(departamento)==obra["Department"]:
            altura=obra["Height (cm)"]
            ancho=obra["Width (cm)"]
            peso=obra["Weight (kg)"]
            profundidad=obra["Depth (cm)"]
            precioPorPeso=PRECIO_ENVIO_UNIDAD*float(peso) if len(peso)>0 else 0
            precioPorM2=PRECIO_ENVIO_UNIDAD*(float(altura)/100)*(float(ancho)/100) if len(peso)>0 else 0
            precioPorM3=PRECIO_ENVIO_UNIDAD*(float(altura)/100)*(float(ancho)/100)*(float(profundidad)/100) if len(peso)>0 else 0
            precioEnvio=max(precioPorM2,precioPorM3,precioPorPeso)
            if precioEnvio==0:
                precioEnvio=PRECIO_ENVIO_FIJO
            obra["TransCost (USD)"]=precioEnvio
            precioTotalEnvio+=precioEnvio
            if (len(peso)>0):
                peso+=float(peso)
            # preguntar por peso estimado xdd
            lt.addLast(obrasDepartamento,obra)
    fechaSortedList=sortList(obrasDepartamento,cmpArtworkByDate)
    precioSortedList=sortList(obrasDepartamento,cmpArtworkByPrice)
    return precioSortedList, fechaSortedList, precioTotalEnvio, peso

#Requerimiento 3
def cmpFunctionTecnicasArtista(tecnica1,tecnica2):
    """ 
    Compara dos técnicas por su cantiadad de obras
    Parámetros: 
        tecnica1: lista de obras de una tecnica
        tecnica2: lista de obras de otra tecnica
    Retorno:
        retorna verdader (True) si la lista tecnica 1 tiene más elementos que la lista de la tecnica 2
    """
    if lt.size(tecnica1)>lt.size(tecnica2): # comparación con orden ascendente
        return True
    else:
        return False

def tecnicasObrasPorArtista(catalog,nombre):
    """ 
    Clasifica las obras de un artista por técnica dado un nombre
    Parámetros: 
        catalog: estructura de datos con el catalogo de artistas y obras
        nombre: nombre del artista
    Retorno:
        sortedList: lista de técnicas en donde cada elemento es una lista de obras de cada técnica
        totalObras: número total de obras del artista
    """
    constituentID=-1
    obras=lt.newList()
    tecnicas=lt.newList() # cada técnica es una lista tipo lt que contiene las obras de esa técnica
    # encontrar el constituentID
    for artista in lt.iterator(catalog["artists"]):
        if nombre==artista["DisplayName"]:
            constituentID=artista["ConstituentID"]
    if constituentID!=-1: # verifica que haya encontrado el id
        for obraArte in lt.iterator(catalog["artworks"]): # se añaden las obras del artista en una lista
            if str(constituentID) in obraArte["ConstituentID"].strip("[]").split(","):
                lt.addLast(obras,obraArte)
        for obraArtista in lt.iterator(obras): # se van añadiendo cada obra a una lista con la obras de cada tecnica alojada a su vez en una lista de tecnicas
            encontro=False
            for tecnica in lt.iterator(tecnicas): # busca si la tecnica existe en la lista de tecnicas
                if obraArtista["Medium"] == lt.getElement(tecnica,0)["Medium"]:
                    lt.addLast(tecnica,obraArtista) # si existe la añade la obra a la técnica
                    encontro=True
            if not encontro: # si no existe
                lt.addLast(tecnicas,lt.newList()) # crea una técnica (lista de obras) en la lista de tecnicas
                lt.addLast(lt.lastElement(tecnicas),obraArtista) # añade la lista de obras de esa tecnica
        sortedList=sortList(tecnicas,cmpFunctionTecnicasArtista) # utiliza la función de comparación con orden ascendente
        totalObras=lt.size(obras) # retorna el número total de obras
    else:
        totalObras=0 # en el caso de que no encuentre el artista no hay obras
        sortedList=lt.newList() # se inicializa una lista para evitar posibles errores
    return sortedList, totalObras

def limpiarVar(dato):
    """
    Esta función limpia cualquier tipo de dato que tenga como párametro de entrada.
    Se utilizará cuando el programa este ejecutando datos provisionales que no necesiten
    ser guardados, esto con el objetivo de optimizar el uso de memoria ram.
    Parámetros:
        dato: Dato de cualquier tipo (str, listas, entre otros)
    Retorno:
        dato: Dato en None
    """
    #print("La ocupación inicial en memoria del dato era:" + str(sys.getsizeof(dato)))
    dato=None
    #print("La ocupación final en memoria del dato es:" + str(sys.getsizeof(dato)))
    return dato
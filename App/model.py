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
from DISClib.ADT import queue
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import quicksort as qs
import time
import datetime
import sys
import re
assert cf


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

# Contrucción modelo [requerimiento 4]
def NewNationalityArt(pais,artwork):  # Requerimiento individual 4
    """
    Requerimiento 4
    Se retornara un diccionario con una nueva nacionalidad. El diccionario contiene
    dos llaves "Nationality" una cadena de texto que representa una nacionalidad en específico y 
    Artworks un tipo de array list que contiene todas las obras relacionadas a esa nacionalidad.
    Parámetros:
        Pais: Nueva nacionalidad
        Artwork: obra de arte relacionada a esa nacionalidad
    Retorno:
        adding: Diccionario con una nueva nacionalidad 
    """
    adding={"Nationality":"","Artworks": lt.newList("ARRAY_LIST",compareNationalities)}
    adding["Nationality"]=pais
    lt.addLast(adding["Artworks"],artwork)
    return adding


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

#Funciones para agregar información [requerimiento 4]
def addNationality(countries,nationality,artwork):  # Requerimiento individual 4
    """
    Requerimiento 4
    La función comprueba si una nacionalidad está o no en la lista de countries.
    Si ya está la nacionalidad, accederá a este elemento y agregará de últimas 
    su respectiva obra de arte en la llave de "Artworks". En caso la obra no se encuentre
    en la lista se agregará a esta lista con la función NewNationalityArt().
    Parámetros:
        countries: lista de nacionalidades con sus respectivas obras
        nationality: nacionalidad a buscar / agregar
        artwork: obra de arte de la nacionalidad correspondiente
    Retorno:
        Se agregarán las nacionalidades y/o obras con addLast()
    """
    posNationality=lt.isPresent(countries,nationality)
    if posNationality>0: #si el país ya se encuentra en la lista se agregará solamente la obra a artworks
        lt.addLast(lt.getElement(countries,posNationality)["Artworks"],artwork)
    else:
        pais=NewNationalityArt(nationality,artwork)
        lt.addLast(countries,pais)

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpArtistDate(artist1,artist2):  # Requerimiento Grupal 1: Función Comparación Ordenamiento
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

def cmpArtworkByDateAcquired(artwork1, artwork2): # Requerimiento Grupal 2: Función Comparación Ordenamiento
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

def cmpFunctionTecnicasArtista(tecnica1,tecnica2): # Requerimiento Individual 3: Función Comparación Ordenamiento
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

def compareNationalities(name, nationality):  # Requerimiento individual 4 : Función comparación al crear una array_list
    """
    Requerimiento 4
    Función de comparación usada al crear la array list de countries en el requerimiento 4.
    Se usa para acceder a las llaves de cada país.
    Parámetros:
        name: nombre de la nacionalidad
        nationality: diccionario dentro de la lista
    Retorno:
        0:  El nombre de la nacionalidad es una de las llaves
        -1: El nombre de la nacionalidad no es una de las llaves
    """
    if (name == nationality['Nationality']):
        return 0
    else:
        return -1

def cmpNationalitiesSize(nacionalidad1,nacionalidad2):  # Requerimiento individual 4 : Función comparación ordenamiento
    """
    Requerimiento 4
    Función de comparación por cantidad de artworks por nacionalidad.
    
    Parámetros:
        obra1: primera nacionalidad, contiene el valor "size" dado que artworks es un array list
        obra2: segunda nacionalidad, contiene el valor "size" dado que artworks es un array list
    Retorno:
        True cuando la primera nacionalidad tiene mayor cantidad de obras que la segunda.
        De lo contario, False.
    """
    return nacionalidad1["Artworks"]["size"]>nacionalidad2["Artworks"]["size"]

def cmpArtworkByPrice(obra1,obra2): # Requerimiento Grupal 5: Función Comparación Ordenamiento
    """
    Función de comparación por el costo de transporte de artworks.
    Parámetros:
        obra1: primera obra, contiene el valor "TransCost (USD)"
        obra2: segunda obra, contiene el valor "TransCost (USD)"
    Retorno:
        True si la obra1 tiene un costo en USD mayor que la obra2
    """
    return obra1["TransCost (USD)"]>obra2["TransCost (USD)"] # orden descendentes
    

def cmpArtworkByDate(obra1,obra2): # Requerimiento Grupal 5: Función Comparación Ordenamiento
    """
    Función de comparación por fechas de artworks.
    Si alguna de las dos fechas es vacía se toma como valor de referencia el
    entero 2022. Esto se hace con el objetivo de dejar las fechas vacías de 
    últimas al ordenar.
    Parámetros:
        obra1: primera obra, contiene el valor "Date"
        obra2: segunda obra, contiene el valor "Date"
    Retorno:
        True si la obra1 tiene una fecha menor que la fecha2.
        False en el caso contrario.
    """
    fecha1=2022 #año actual +1
    fecha2=2022 
    if len(obra1["Date"])>0:
        fecha1=int(obra1["Date"])
    if len(obra2["Date"])>0:
        fecha2=int(obra2["Date"]) 
    return fecha1<fecha2
   


# Funciones de ordenamiento

def sortList(lista,cmpFunction,sortType):
    """
    ####### FUNCIÓN MODIFICADA PARA HACER PRUEBAS #####
    Función de ordenamiento que se usará en distintos requerimientos dependiendo
    del ordenamiento deseado
    Parámetros: 
        lista: lista que se ordenara
        cmpFunction: función de comparación
        sortType: tipo de ordenamiento (1)Insertion - (2)Selection - (3)Merge - (4)Quick
    Retorno:
        lista ordenada por insertion
    """
    if sortType == "1":
        sorted_list= ins.sort(lista,cmpFunction)
    elif sortType == "2":
        sorted_list= sa.sort(lista,cmpFunction)
    elif sortType == "3":
        sorted_list= ms.sort(lista,cmpFunction)
    elif sortType == "4":
        sorted_list= qs.sort(lista, cmpFunction)
    return sorted_list

# Funciones de Consulta

def listarArtistasCronologicamente(catalog,fechaInicial,fechaFinal,sortType="3"):  # Requerimiento Grupal 1: Función Principal
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
            if (nacimiento>= fechaInicial and nacimiento<=fechaFinal):
                lt.addLast(listaNac,artist)
                contador+=1
    sortList(listaNac,cmpArtistDate,sortType)
    return listaNac,contador

def listarAdquisicionesCronologicamente(catalog,fechaInicial,fechaFinal,sortType="3"):  # Requerimiento Grupal 2: Función Principal
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
    pattern = re.compile("[0-9][0-9][0-9][0-9]-([1][0-2]|[0][1-9])-([3][1]|[0-2][0-9])")
    contadorRango=0
    contadorPurchase=0
    if pattern.match(fechaInicial) and pattern.match(fechaFinal):
        fechaInicialTi= time.strptime(fechaInicial,"%Y-%m-%d")
        fechaFinalTi= time.strptime(fechaFinal,"%Y-%m-%d")
        for obra in lt.iterator(catalog["artworks"]):
            if len(obra["DateAcquired"])==10: #Se ignoran las fechas vacías
                fecha=time.strptime(obra["DateAcquired"],"%Y-%m-%d")
                if fecha>=fechaInicialTi and fecha<=fechaFinalTi: 
                    contadorRango+=1
                    lt.addLast(listaAdq,obra) #se agregan fechas que estén dentro del rango deseado
                    if obra["CreditLine"].startswith("Purchase"):
                        contadorPurchase+=1
        
        sortList(listaAdq,cmpArtworkByDateAcquired,sortType) #ordenamiento por insertion
    return listaAdq, contadorPurchase, contadorRango


def getArtistName(catalog,ConstituentID): # Requerimiento Grupal 2: Función Complementaria
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


def tecnicasObrasPorArtista(catalog,nombre,sortType="3"): # Requerimiento Individual 3: Función Principal
    """ 
    Clasifica las obras de un artista por técnica dado un nombre
    Parámetros: 
        catalog: estructura de datos con el catalogo de artistas y obras
        nombre: nombre del artista
        sortType: tipo de ordenamiento a utilizar
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
        sortedList=sortList(tecnicas,cmpFunctionTecnicasArtista,sortType) # utiliza la función de comparación con orden ascendente
        totalObras=lt.size(obras) # retorna el número total de obras
    else:
        totalObras=0 # en el caso de que no encuentre el artista no hay obras
        sortedList=lt.newList() # se inicializa una lista para evitar posibles errores
    return sortedList, totalObras
    
def getNationality(catalog,ConstituentID):  # Requerimiento individual 4
    """
    Requerimiento 4
    Se retornara las nacionalidades de los artistas de acuerdo a su ConstituentID.
    Parámetros: 
        catalog: catalogo con obras y artistas
        ConstituentID: código del artista. Relaciona a una obra dentro del catalogo["artworks"]
        con su nacionalidad correspondiente en catalogo["DisplayName"]
    Retorno:
        nationality: nacionalidad del artista que realizó la obra de arte
    """
    
    nationality=""
    for artist in lt.iterator(catalog['artists']):
        if ConstituentID.strip()==artist["ConstituentID"].strip():
            nationality=artist["Nationality"]
    if nationality=="Nationality unknown" or nationality=="":
        nationality="Unknown" 
    return nationality
            
def ClasificarObrasNacionalidad(catalog,sortType="1"):  # Requerimiento individual 4: Función Principal
    """
    Requerimiento 4.
    La función clasificará las obras de acuerdo a la nacionalidad de su/s creador/es.
    Se recorrerá todo el catalogo de obras de arte, y se relacionará el "ConstituentID" de cada
    obra con su respectivo nacionalidad. En caso de que una de las obras tenga más de un artista 
    se relacionará esta obra con las nacionalidades de cada artista. Al momento de relacionar la obra con
    la nacionalidad de su/s artista/s se iran agregando nacionalidades con sus respectivas obras
    a una array lista (countries).
    Después de finalizar el recorrido y la categorización por nacionalidades, se usará un ordenamiento 
    por tipo insertation para ordenar la lista de countries de mayor a menor.
    Parámetros:
        catalog: catalogo de obras y artistas
        sortType="1" ordenamiento por insertion
    Retornos:
        top10: Lista con el top10 de nacionalidades, ordenada de mayor a menor
        primerlugar: Obras por nacionalidad del primer lugar
    """
    countries=lt.newList("ARRAY_LIST",cmpfunction=compareNationalities)
    for obra in lt.iterator(catalog["artworks"]):
        conID=obra["ConstituentID"][1:-1]
        if "," in conID:
            codigoNum=conID.split(",")
            for codigo in codigoNum: #Se hace un recorrido cuando una obra fue hecha por más de un autor
                nationality= getNationality(catalog,codigo)
                addNationality(countries,nationality,obra)
        else:
            nationality= getNationality(catalog,conID)
            addNationality(countries,nationality,obra)
    
    sortList(countries,cmpNationalitiesSize,sortType)
    primerlugar=lt.getElement(countries,1)
    top10=lt.subList(countries,1,10)
    return top10,primerlugar


def transportarObrasDespartamento(catalog,departamento,sortType="3"): # Requerimiento Grupal 5: Función Principal
    """
    La función indica el precio total de envío que cuesta transportar un departamento. Entrega también una
    lista que contiene las obras que se van a transportar y el precio de transportar cada obra. Los precios
    se establecen de acuerdo a 

    Parámetros: 
        catalog: catalogo con obras y artistas
        departamento: nombre del departamento a transportar
        sortType: tipo de ordenamiento utilizado dentro del método // ordenamiento por merge
    Retorno:
        precioSortedList: lista de obras organizadas por precio
        obrasDepartamento: lista de obras organizadas por fecha de antiguedad 
        precioTotalEnvio: costo total de transportar las obras
        pesoTotal: peso total de las obras
        cantidadDeObras: cantidad de obras a transportar
    """

    # Constantes
    PRECIO_ENVIO_UNIDAD=72
    PRECIO_ENVIO_FIJO=48
    obrasDepartamento=lt.newList("ARRAY_LIST")
    precioTotalEnvio=0
    pesoTotal=0
    for obra in lt.iterator(catalog["artworks"]):
        if str(departamento)==obra["Department"]:
            altura=obra["Height (cm)"]
            ancho=obra["Width (cm)"]
            peso=obra["Weight (kg)"]
            profundidad=obra["Depth (cm)"]
            precioPorPeso=0
            precioPorM2=0
            precioPorM3=0
            if peso.isnumeric(): #KG   #se comprueba que peso no sea una cadena vacia 
                precioPorPeso=PRECIO_ENVIO_UNIDAD*float(peso) #if len(peso)>0 else 0
                pesoTotal+=peso
            #Se comprueban si cada una de las medidas es una cadena de str vacía. Si alguno de ellos es verdad se cambia a 100 dado que son cm
            if len(altura)==0:
                altura=100
            if len(ancho)==0:
                ancho=100
            if len(profundidad)==0:
                profundidad=100
            precioPorM2=PRECIO_ENVIO_UNIDAD*(float(altura)/100)*(float(ancho)/100) #if len(peso)>0 else 0
            precioPorM3=PRECIO_ENVIO_UNIDAD*(float(altura)/100)*(float(ancho)/100)*(float(profundidad)/100) #if len(peso)>0 else 0
            precioEnvio=max(precioPorM2,precioPorM3,precioPorPeso)
            if precioEnvio==0:
                precioEnvio=PRECIO_ENVIO_FIJO
            obra["TransCost (USD)"]=precioEnvio
            precioTotalEnvio+=precioEnvio
            lt.addLast(obrasDepartamento,obra)
    
    size=obrasDepartamento["size"]
    precioSortedList=lt.subList(obrasDepartamento,0,size) #se copia la lista 
    sortList(precioSortedList,cmpArtworkByPrice,sortType)
    sortList(obrasDepartamento,cmpArtworkByDate,sortType)#lista ordenada por fecha
    return precioSortedList, obrasDepartamento, precioTotalEnvio, pesoTotal, lt.size(obrasDepartamento)


def expoEpocaArea(catalog,areaExpo,fechaInicialSt,fechaFinalSt, obraCortadaB=True): # Requerimiento Grupal 6 (Bono): Función Principal
    """
    La función propone una nueva exposición dada una área disponible y unos rangos de fechas de las obras

    Parámetros: 
        catalog: catalogo con obras y artistas
        areaExpo: área disponible en metros cuadrados para la exposición
        fechaInicial: fecha inicial de obras ingresada por el usuario
        fechaFinal: fecha final de obras ingresada por el usuario
        obraCortadaB: si el usuario quiere que se corte alguna obra para ocupar el área disponible
    Retorno:
        cantidad: cantidad de obras de la nueva exposición
        areaTotalObras: área total ocupada por las obras
        obrasExpo: lista con las obras de la exposición
        obraCortada: parámetro que indica si quieren cortar una obra con tal de completar el espacio 
        disponible para la exposición
    """
    obrasExpo= lt.newList("ARRAY_LIST")
    areaTotalObras=0
    cantidad=0
    size=lt.size(catalog["artworks"])
    i=0
    obraCortada=""
    pattern=re.compile("[0-9][0-9][0-9][0-9]")
    fechasCorrectas=False
    if pattern.match(fechaFinalSt) and pattern.match(fechaInicialSt):
        fechasCorrectas=True
        fechaInicial=int(fechaInicialSt)
        fechaFinal=int(fechaFinalSt)
    while areaTotalObras<areaExpo and i<size and fechasCorrectas:
        artwork=lt.getElement(catalog["artworks"],i)
        #el siguiente condicional ignorará obras que tengan datos como su fecha, largo o ancho vacíos. Si la fecha es vacía
        #no se podrá utilizar la obra para la exposición por época. Pero si la obra tiene ancho y/o largo se podrá utilizar en la exposición.
        if artwork["Date"].isnumeric() and (artwork["Height (cm)"].isnumeric() or artwork["Width (cm)"].isnumeric()) and len(artwork["Depth (cm)"])==0:
            dateArt=int(artwork["Date"])
            if dateArt>=fechaInicial and dateArt<=fechaFinal:
                altura=1 #tomamos la altura o ancho como 1 metro en caso de que alguno de los dos tengan un valor vacío
                ancho=1
                if artwork["Height (cm)"].isnumeric():
                   altura=float(artwork["Height (cm)"])/100 
                if artwork["Width (cm)"].isnumeric():
                    ancho=float(artwork["Width (cm)"])/100
                areaArt=altura*ancho
                areaprov=areaTotalObras+areaArt #se comprueba si con esta obra se supera el área
                if areaprov>areaExpo: #esto significa que ya se sobrepasa el área si se añade esta obra
                    diferencia=areaExpo-areaTotalObras
                    #print("AT",areaTotalObras,"dif",diferencia)
                    if obraCortadaB: #se cortará una obra para completar el área disponible en caso de que el usuario haya dicho que sí
                        areaArt=diferencia #areaExpo-areaTotalObras #se "corta" esta obra para que quepa en el área
                        obraCortada=("Se utilizaron "+str(diferencia)+ " del área (m^2) de la obra titulada: "+artwork["Title"]+
                                    " con ObjectID: "+artwork["ObjectID"]+" para completar el área de la exposición")
                        areaTotalObras+=areaArt
                        cantidad+=1
                        artwork["EstArea (m^2)"]=areaArt
                        lt.addLast(obrasExpo,artwork)
                    else:
                        obraCortada="No se utilizó ninguna fracción de área de una obra de acuerdo a lo seleccionado por el usuario"
                        break   
                else:
                    areaTotalObras+=areaArt
                    cantidad+=1
                    artwork["EstArea (m^2)"]=areaArt
                    lt.addLast(obrasExpo,artwork)
        i+=1               
    return cantidad,areaTotalObras,obrasExpo,obraCortada

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
    dato=None
    return dato
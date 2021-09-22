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
    Función de ordenamiento con insertation que se usará en distintos requerimientos
    Parámetros: 
        lista: lista que se ordenara
        cmpFunction: función de comparación
    Retorno:
        lista ordenada por insertion
    """
    start_time = time.process_time()
    #cantidad_registros= ((porcentaje/100)*lt.size(catalog['artworks']))//1
    #subLista=lt.subList(catalog['artworks'],0,cantidad_registros)
    if sortType == "1":
        sorted_list= ins.sort(lista,cmpFunction)
    elif sortType == "2":
        sorted_list= sa.sort(lista,cmpFunction)
    elif sortType == "3":
        sorted_list= ms.sort(lista,cmpFunction)
    elif sortType == "4":
        sorted_list= qs.sort(lista, cmpFunction)
    
    med_time = time.process_time() # BORRAR
    elapsed_time_mseg = (med_time - start_time)*1000 # BORRAR
    print(sortType,"TIEMPO DURACIÓN ORDENAMIENTO: ",elapsed_time_mseg) # BORRAR

    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

# Funciones de Consulta

def listarArtistasCronologicamente(catalog,fechaInicial,fechaFinal,sortType):  # Requerimiento Grupal 1: Función Principal
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

def listarAdquisicionesCronologicamente(catalog,fechaInicial,fechaFinal,sortType):  # Requerimiento Grupal 2: Función Principal
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


def tecnicasObrasPorArtista(catalog,nombre,sortType): # Requerimiento Individual 3: Función Principal
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
        sortedList=sortList(tecnicas,cmpFunctionTecnicasArtista,sortType)[1] # utiliza la función de comparación con orden ascendente
        totalObras=lt.size(obras) # retorna el número total de obras
    else:
        totalObras=0 # en el caso de que no encuentre el artista no hay obras
        sortedList=lt.newList() # se inicializa una lista para evitar posibles errores
    return sortedList, totalObras
    
########## req4
def getNationality(catalog,ConstituentID):
    """
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
    if posNationality>0: #si el país ya se encuentra en la lista se agregará solamente la obra a artworks
        lt.addLast(lt.getElement(countries,posNationality)["Artworks"],artwork)
    else:
        pais=NewNationalityArt(nationality,artwork)
        lt.addLast(countries,pais)

def compareNationalities(name, nationality):
    """
    Función de comparación usada al crear la array list de countries en el requerimiento 4.
    Se usa para acceder a las llaves de cada país.
    Parámetros:
        name: ######
        nationality: ###
    Retorno:
        0:  #####
        -1: #####
    """
    if (name == nationality['Nationality']):
        return 0
    else:
        return -1

def cmpNationalities(nacionalidad1,nacionalidad2):
    """
    Función de comparación por cantidad de artworks por nacionalidad.
    
    Parámetros:
        obra1: primera nacionalidad, contiene el valor "size" dado que artworks es un array list
        obra2: segunda nacionalidad, contiene el valor "size" dado que artworks es un array list
    Retorno:
        True cuando la primera nacionalidad tiene mayor cantidad de obras que la segunda.
        De lo contario, False.
    """
    return nacionalidad1["Artworks"]["size"]>nacionalidad2["Artworks"]["size"]

def req4(catalog,sortType):
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
        conID=obra["ConstituentID"][1:-1]
        if "," in conID:
            codigoNum=conID.split(",")
            for codigo in codigoNum: #Se hace un recorrido cuando una obra fue hecha por más de un autor
                nationality= getNationality(catalog,codigo)
                addNationality(countries,nationality,obra)
        else:
            nationality= getNationality(catalog,conID)
            addNationality(countries,nationality,obra)
    
    sortList(countries,cmpNationalities,sortType)
    primerlugar=lt.getElement(countries,1)
    top10=lt.subList(countries,1,10)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return top10,primerlugar,elapsed_time_mseg

###fin req 4

def transportarObrasDespartamento(catalog,departamento,sortType): # Requerimiento Grupal 5: Función Principal
    """
    La función indica el precio total de envío que cuesta transportar un departamento. Entrega también una
    lista que contiene las obras que se van a transportar y el precio de transportar cada obra. Los precios
    se establecen de acuerdo a 

    Parámetros: 
        catalog: catalogo con obras y artistas
        departamento: nombre del departamento a transportar
        sortType: tipo de ordenamiento utilizado dentro del método
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
    x=0 ##Borrar
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

        #!!!!!!!!! Decidir que hacemos con Depth (cm)
        if artwork["Date"].isnumeric() and (artwork["Height (cm)"].isnumeric() or artwork["Width (cm)"].isnumeric()) and len(artwork["Depth (cm)"])==0:
            #print(x, "paso", artwork["ObjectID"], "cumple")
            x+=1
            # print()
            dateArt=int(artwork["Date"])
            if dateArt>=fechaInicial and dateArt<=fechaFinal:
                #print(x, "paso", artwork["ObjectID"], "cumple con rango de fechas")
                altura=1 #tomamos la altura o ancho como 1 metro en caso de que alguno de los dos tengan un valor vacío
                ancho=1
                if artwork["Height (cm)"].isnumeric():
                   altura=float(artwork["Height (cm)"])/100 
                if artwork["Width (cm)"].isnumeric():
                    ancho=float(artwork["Width (cm)"])/100
                areaArt=altura*ancho
                areaprov=areaTotalObras+areaArt #se comprueba si con esta obra se supera el área
                if areaprov>areaExpo: #esto significa que ya se sobrepasa el área si se añade esta obra
                    #print("!! Área obra:",areaArt,"Prueba, Object ID:", "A prov", areaprov)
                    diferencia=areaExpo-areaTotalObras
                    #print("AT",areaTotalObras,"dif",diferencia)
                    if obraCortadaB:
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
                #queue.enqueue(obrasExpo,artwork)
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
    #print("La ocupación inicial en memoria del dato era:" + str(sys.getsizeof(dato)))
    dato=None
    #print("La ocupación final en memoria del dato es:" + str(sys.getsizeof(dato)))
    return dato
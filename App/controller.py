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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo 

def initCatalog(ListType):
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog(ListType)
    return catalog

# Funciones para la carga de datos

def loadData(catalog,muestra):

    """
    Carga los artistas y obras al catalogo
    """
    loadArtists(catalog,muestra)
    loadArtworks(catalog,muestra)

def loadArtists(catalog,muestra): ##MODIFICADO PARA HACER PRUEBAS

    """
    Carga los artistas en una lista dado un nombre de archivo
    """
    artistsFilename = cf.data_dir + 'MOMA\\Artists-utf8-'+muestra+'.csv'
    inputFile= csv.DictReader(open(artistsFilename, encoding='utf-8'))
    for artist in inputFile:
        model.addArtist(catalog, artist)

def loadArtworks(catalog,muestra="small"):
    # TODO: documentación parámetros retorno
    """
    Carga las obras en una lista dado un nombre de archivo
    """
    artworksFilename = cf.data_dir + 'MOMA\\Artworks-utf8-'+muestra+'.csv'
    inputFile= csv.DictReader(open(artworksFilename, encoding='utf-8'))
    for artwork in inputFile:
        model.addArtwork(catalog, artwork)

# Funciones de Consulta

def getArtistName(catalog, ID):
    """
    Retorna el nombre de un artista de acuerdo a su ConstituentID
    """
    return model.getArtistName(catalog,ID)

def listarArtistasCronologicamente(catalog,fechaInicial,fechaFinal,sortType):
    """
    Retorna a los artistas ordenados cronologicamente de acuerdo a un rango de fechas
    Además del total de artistas en ese rango de fechas
    """
    return model.listarArtistasCronologicamente(catalog,int(fechaInicial),int(fechaFinal),sortType)

def listarAdquisicionesCronologicamente(catalog,fechaInicial,fechaFinal,sortType):
    """
    Retorna obras de arte ordenadas cronologicamente de acuerdo a un rango de fechas.
    Además del total de obras compradas en el rango deseado
    """
    return model.listarAdquisicionesCronologicamente(catalog,fechaInicial,fechaFinal,sortType)

def tecnicasObrasPorArtista(catalog, nombre,sortType):
    """
    Retorna las técnicas usadas en obras de acuerdo a un artista en específico, junto al total de obras del
    artista y su técnica más usada y su listado de obras
    """
    return model.tecnicasObrasPorArtista(catalog,nombre,sortType)

def ClasificarObrasNacionalidad(catalog,sortType):
    """
    Retorna el top10 de las obras de arte de acuerdo a su nacionalidad, además brinda las obras del primer lugar
    """
    return model.ClasificarObrasNacionalidad(catalog,sortType)

def transportarObrasDespartamento(catalog, departamento,sortType):
    """
    Retorna las obras de arte más costosas y antiguas a transportar por departamento, junto al total de obras, 
    precio del servicioy peso estimado. 
    """
    return model.transportarObrasDespartamento(catalog,departamento,sortType)



def expoEpocaArea(catalog,areaExpo,fechaInicial,fechaFinal,cortarObra): #req 6
    """
    Retorna las obras propuestas para el MOMA de acuerdo a especificaciones de área y un rango de fechas
    """
    return model.expoEpocaArea(catalog,areaExpo,fechaInicial,fechaFinal,cortarObra)

def limpiarVar(dato):
    """
    Llama a la función limpiarvar
    """
    return model.limpiarVar(dato)
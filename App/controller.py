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
    # TODO: documentación parámetros retorno
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog(ListType)
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    # TODO: documentación parámetros retorno
    """
    Carga los artistas y obras al catalogo
    """
    loadArtists(catalog)
    loadArtworks(catalog)

def loadArtists(catalog):
    # TODO: documentación parámetros retorno
    """
    Carga los artistas en una lista dado un nombre de archivo
    """
    artistsFilename = cf.data_dir + 'MOMA\\Artists-utf8-small.csv'
    inputFile= csv.DictReader(open(artistsFilename, encoding='utf-8'))
    for artist in inputFile:
        model.addArtist(catalog, artist)

def loadArtworks(catalog):
    # TODO: documentación parámetros retorno
    """
    Carga las obras en una lista dado un nombre de archivo
    """
    artworksFilename = cf.data_dir + 'MOMA\\Artworks-utf8-small.csv'
    inputFile= csv.DictReader(open(artworksFilename, encoding='utf-8'))
    for artwork in inputFile:
        model.addArtwork(catalog, artwork)

# Funciones de Consulta

def getArtistName(catalog, ID):
    # TODO: Documentación
    return model.getArtistName(catalog,ID)

def listarArtistasCronologicamente(catalog,fechaInicial,fechaFinal):
    """
    ##llenar
    """
    return model.listarArtistasCronologicamente(catalog,int(fechaInicial),int(fechaFinal))

def listarAdquisicionesCronologicamente(catalog,fechaInicial,fechaFinal):
    # TODO: Documentación
    """
    llenar
    """
    return model.listarAdquisicionesCronologicamente(catalog,fechaInicial,fechaFinal)

def tecnicasObrasPorArtista(catalog, nombre):
    # TODO: Documentación
    return model.tecnicasObrasPorArtista(catalog,nombre)

def transportarObrasDespartamento(catalog, departamento):
    # TODO: Documentación
    return model.transportarObrasDespartamento(catalog,departamento)


#TODO: cambiar nombre
def req4(catalog):
    # TODO: Documentación
    return model.req4(catalog)

def limpiarVar(dato):
    """
    Llama a la función limpiarvar
    """
    return model.limpiarVar(dato)
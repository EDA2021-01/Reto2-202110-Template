﻿"""
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


import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import selectionsort as ss
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as mg
from DISClib.Algorithms.Sorting import quicksort as qs
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos Array
def newCatalog():
    catalog = {'videos': None,
               'country': None,
               'tagvideos': None,
               'categories': None}
    catalog['videos'] = lt.newList('SINGLE_LINKED')
    catalog['country'] = mp.newMap(150,
                                    maptype="CHAINING",
                                    loadfactor=2.0)
    catalog['tagvideos'] = mp.newMap(50000,
                                     maptype="CHAINING",
                                    loadfactor=2.0)
    catalog['categories'] = mp.newMap(32,
                                     maptype="CHAINING",
                                    loadfactor=2.0)
    return catalog

# Funciones para agregar informacion al catalogo
def addVideo(catalog, video):
    # Se adiciona el video a la lista de videos
    lt.addLast(catalog['videos'], video)
    #Se adicionan los tags en la lista de tagvideos
    mp.put(catalog['tagvideos'], video['tags'], video)
    tagvideo_info = video['tags'].split("|")
    # for tag_info in tagvideo_info:
    #     addTagsVideo(catalog, tag_info.strip(), video)
    #Adiciona los países en su respectiva llave
    addCountry(catalog, video)
    
def addCountry(catalog, video):
    countries = catalog['country']
    act_country = video['country']
    #print(countries)
    # pos_country = lt.isPresent(countries, n_country)
    # if pos_country > 0:
    #     lt.addLast(countries['videos'], video)
    # else: 
    #     country = newCountry(n_country)
    #     lt.addLast(countries, video['country'])
    # lt.addLast(country['videos'], video)
    existconutry  = mp.contains(countries, act_country)
    if existconutry:
        entry = mp.get(countries, act_country)
        country = me.getValue(entry)
    else: 
        country = newCountry(act_country)
        mp.put(countries, act_country, country)
    lt.addLast(country['videos'], video)

def addTagsVideo(catalog, n_tag, video):
    tagvideos = catalog['tagvideos']
    existeTag = mp.contains(tagvideos, n_tag)
    if existeTag: 
        entry = mp.get(tagvideos, n_tag)
        tag = me.getValue(entry)
    else:
        tagvideo = newVideoTag(n_tag)
        mp.put(tagvideos,n_tag,tagvideo)
    lt.addLast(tagvideos['videos'],video)
     # pos_tag = lt.isPresent(tagvideos, n_tag)
     # if pos_tag > 0:
     #     videotag = lt.getElement(tagvideos, pos_tag)
     # else:
     #     videotag = newVideoTag(n_tag)
     #     lt.addLast(tagvideos, videotag)
     # lt.addLast(videotag['videos'], video)


def addCategories(catalog, category):
    #     category = NewCategories(categories_videos['name'], categories_videos['id'])
    #     lt.addLast(catalog['categories'], category)
    # lista = categories_videos["id\tname"].split("\t ")
    # categories_videos["id"] = lista[1].strip()
    # categories_videos["name"] = lista[0]
    t = newCategories(category['name'], category["id"])
    mp.put(catalog['categories'], t['name'], t['id'])
    # Funciones para creacion de datos
    # Estas funciones son precisamente para hacer la creación 
    # De las llaves y sus respectivos valores (llaves vacías, la idea es crear la llave y en las funciones
    # de agregar información al catálogo se completan)

def newCountry(n_country):
    country = {'name': "", 'videos': None}
    country['name'] = n_country
    country['videos'] = lt.newList('SINGLE_LINKED', cmpcountry)
    return country

def newVideoTag(tag_name):
    video_tag = {'name': "", 'videos': None}
    video_tag['name'] = tag_name
    video_tag['videos'] = lt.newList('ARRAY_LIST')
    return video_tag

def newCategories(name, ca_id):
    categories_videos = {'name': "", 'id': ""}
    categories_videos['name'] = name
    categories_videos['id'] = ca_id
    return categories_videos

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpcountry(country1, country2):
    if (country1 == country2):
        return 0
    elif country1 > country2:
        return 1
    else:
        return -1
def cmptags(tag1,tag2):
    if (tag1.lower() in tag2['name'].lower()):
        return 0
    return -1

def cmpcategories(n_category, categories_videos):
    return (n_category == categories_videos['name'])

def cmpVideosByViews(video1, video2):
    if video1['views'] < video2['views']:
        return True
    return False

# Funciones de ordenamiento

def sortVideos(catalog, size, sortType):
    sub_list = lt.subList(catalog['videos'], 0, size)
    start_time = time.process_time()
    if sortType == 1:
        sorted_list = ss.sort(sub_list, cmpVideosByViews)
    elif sortType == 2:
        sorted_list = ins.sort(sub_list, cmpVideosByViews)
    elif sortType == 3:
        sorted_list = sa.sort(sub_list, cmpVideosByViews)
    elif sortType == 4:
        sorted_list = mg.sort(sub_list, cmpVideosByViews)
    else:
        sorted_list = qs.sort(sub_list, cmpVideosByViews)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

#Funciones para contar la información en el cátalogo
def VideoSize(catalog):
    return lt.size(catalog['videos'])

def CountrySize(catalog):
    return mp.size(catalog['country'])

def TagSize(catalog):
    return mp.size(catalog['tagvideos'])

def CategoriesSize(catalog):
    return mp.size(catalog['categories'])


#Funciones de consulta

def LikesbyCategory(catalog, number, category):
    #los n videos con más LIKES para el nombre de una categoría específica
    FilterCategory = lt.newList('ARRAY_LIST')
    
    i = 0
    while i < lt.size(catalog['videos']):
        a = lt.getElement(catalog['videos'], i)
        i += 1
        print(i, "video: ")
        print(a['views'])

# def greatestTendency(catalog, n_category):
#     temp_list = []
#     video_template = {'title': "", 
#                       'channel_title': "", 
#                       'category_id': "", 
#                       'days_trending': []
#                       'ammount_of_days': 0}
#     for video in catalog['categories']:
#         for video_temp in temp_list:
#             if video['title'] == video_temp['title']:
#                 trending_date = video['publish_time'][0:9]
#                 if trending_date not in video_temp['days_trending']:
#                     video_temp['days_trending'].append(trending_date)
#                     video_temp['ammount_of_days'] += 1
#             else:
#                 video_template['title'] = video['title']
#                 video_template['channel_title'] = video['channel_title']
#                 video_template['category_id'] = video['category_id']
#                 video_template['days_trending'].append(video['publish_time'][0:9])
#                 video_template['ammount_of_days'] = 1
#     best = None
#     days = 0
#     for video in temp_list:
#         if video['ammount_of_days'] > days:
#             days = video['ammount_of_days']
#             best = video
#     return best

# def compareCategories(videos, ca_id):
#     if videos['info']['category_id'] == ca_id:
    
def findIDwithName(catalog, ca_name):
    if mp.contains(catalog['categories'], ca_name):
        ca_id = mp.get(catalog['categories'], ca_name)
        ca_id = me.getValue(ca_id)
        return ca_id

def tendencyByCategory(catalog, ca_name):
    video_template = {'title': "", 
                      'channel_title': "", 
                      'category_id': "", 
                      'days_trending': [],
                      'ammount_of_days': 0}
    videos = catalog['videos']['first']
    ca_id = findIDwithName(catalog, ca_name)
    print(mp.keySet(catalog['categories']))

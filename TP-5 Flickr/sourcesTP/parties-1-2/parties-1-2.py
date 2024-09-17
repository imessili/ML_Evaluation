#!/usr/bin/env python
# coding: utf-8

# # TP Fouilles de données
# 23 octobre 2019 - Master 2 Décision & Optimisation - Univ. Caen

# ### Détection et caractérisation des centres d'intérêt d'une ville (ici Caen) à partir des photos publiées sur un site de partage (Flickr)
# 
# Centre d'intérêt : zone dense de photos publiées sur Flickr. 

# Utilisation de Python 3

# Imports des librairies utilisées lors du TP
import folium
import folium.plugins
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sqlalchemy import create_engine


# Constantes pour la suite
LAT_CAEN, LON_CAEN = 49.17195, -0.369374 #latitude, longitude du centre de la région étudiée (Caen)
PSQL_USER, PSQL_PWD = "VOTRE_NUM_ETU", "VOTRE_MDP_PSQL"


# ## Récupération et prétraitement des données

# Création du DataFrame (pandas) par appel à la base de données PostgreSQL. On garde une trace du DataFrame d'origine (*photos_original*).
engine = create_engine("postgresql://"+PSQL_USER+":"+PSQL_PWD+"@postgresql.info.unicaen.fr/app_decim_fdd_bd")
with engine.begin() as comm:
    photos_original = pd.read_sql_table("photos", comm, index_col="id")
    photos = photos_original.copy()
    urls_original = pd.read_sql_table("urls", comm, index_col="id")
    urls = urls_original.copy()

# Nombre de photos contenues dans le DataFrame (photos géolocalisées dans la région de Caen extraites fin 2017 sur Flickr)




# Nombre d'utilisateurs distincts



# Nombre d'utilisateurs ayant posté qu'une seule photo



# ### Affichage des données photos
# 
# #### Description des colonnes :
# - **id** = identifiant de la photo
# - **title** = titre de la photo
# - **owner** = identifiant du propriétaire de la photo (utilisateur qui a publié la photo)
# - **datetaken** = date de prise de la photo
# - **dateupload** = date de téléchargement de la photo sur Flickr
# - **secret, farm, server** = informations quant à l'emplacement de la photo sur les serveurs Flickr.
# Pour afficher l'image dans un  navigateur : https://farm[farm].staticflickr.com/[server]/[id]_[secret].jpg
# - **latitude, longitude** = coordonnées géographiques de la prise de vue
# - **tags** = les tags fournis par l'utilisateur
# - **views** = nombre de vues de la photo sur Flickr
# 
# Les champs qui nous seront utiles : id, title, owner, datetaken, dateupload, latitude, longitude, tags, views
# 
# 


# **Données abérrantes** : La base de données contient un certains nombre de données où la date de téléchargement sur Flickr (**dateupload**) est postérieure à la date de prise (**datetaken**)...
# Donnez l'instruction *pandas* pour supprimer ces photos du dataframe. Attention, les types des deux colonnes précédemment citées ne sont pas identiques.



# **Problème des "albums photos"** : Certains utilisateurs publient des séries de photos, généralemment prises au même endroit, dans un court laps de temps (quelques minutes). Exemple trouvé dans la base : un utilisateur a pris (et publié sur Flickr) plusieurs photos de son chat à son domicile. Il est évident que cet album photo, bien que le nombre de photos soit "conséquent" (~20), ne représente pas un centre d'intérêt. Il est nécéssaire de traiter les données afin d'éliminer, ou du moins réduire ce phénomène. Une solution, très simpliste, est de considérer dans notre analyse qu'une photo par utilisateur par heure de temps. Donner l'instruction *pandas* correspondante et critiquez la. Mettez ensuite à jour le DataFrame photos en gardant une seule photo par groupe (on pourra prendre celle dont l'identifiant est minimal par exemple).
# 
# Indication : utiliser les méthodes *pandas.DataFrame.groupby* et *pandas.Grouper*.



# Nombre de photos désormais



# ## Affichage des données photos sur une carte
# Utilisez pour cela la librairie *folium*.

map = folium.Map(location=[LAT_CAEN, LON_CAEN], tiles="cartodbpositron", zoom_start=12)

# Un point pour chaque photo
for ind, row in photos.iterrows():
    folium.CircleMarker([row['latitude'], row['longitude']], radius = 1).add_to(map)

# Enregistrer la map au format HTML (appelez seulement "map" si vous êtes sur Jupyter sur FireFox)

map.save("map.html")




# ## Clustering

# Nous allons désormais chercher à connaitre les centres d'intérêt au regard du DataFrame *photos*. Quel algorithme de clustering proposeriez-vous ?

# #### Utilisation de l'algorithme DBSCAN via scikit-learn


# Créer une nouvelle colonne "clusters_step1" dans le dataframe photos pour le label des clusters


# Ensemble des clusters donnés par l'algorithme DBSCAN. -1 est le label pour le bruit.




# Définition des couleurs pour représenter les clusters. Il n'y a pas spécialement assez de couleurs mais nous nous en contenterons avec un modulo. Le noir correspond au bruit (-1).

COLORS = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
             'lightred', 'darkblue', 'darkgreen', 'cadetblue', 'pink', 'lightblue', 'lightgreen',
             'gray', 'black']

def getColor(label):
    if label < 0: #bruit
        return "lightgray"
    else:
        return COLORS[label % len(COLORS)]


# #### Affichage de la carte avec les clusters

map = folium.Map(location=[LAT_CAEN, LON_CAEN], tiles="cartodbpositron", zoom_start=12)

# Un point pour chaque photo
for ind, row in photos.iterrows():
    folium.CircleMarker([row['latitude'], row['longitude']], radius = 1, color=getColor(row["clusters_step1"])).add_to(map)

# Afficher un marker-popup pour chaque cluster à son centre (sauf pour le bruit) avec folium.Marker



    

map.save("map.html")



# **Amélioration** : un cluster C contient un très grand ensemble de photos. Cette région, trop dense, n'a pas permis à DBSCAN avec les paramètres donnés précédemment de discriminer d'avantage les centres d'intérêt.
# Il serait intéréssant d'appliquer de nouveau l'algorithme avec des paramètres plus fins pour ce cluster.

# *Remarque* : pour ce nouveau DBSCAN, créer une nouvelle colonne "clusters_step2" initialisée avec les valeurs "clusters_step1",
# puis ensuite modifier le numéro de cluster en "clusters_step2" seulement pour les photos du cluster C, en utilisant la fonction changeLabels

def changeLabels(x, firstLabel):
    return np.array([firstLabel+xi if xi >= 0 else -1 for xi in x])

photos["clusters_step2"] = photos["clusters_step1"]


# #### Affichage de la carte avec les clusters

map = folium.Map(location=[LAT_CAEN, LON_CAEN], tiles="cartodbpositron", zoom_start=12)

# Un point pour chaque photo
for ind, row in photos.iterrows():
    folium.CircleMarker([row['latitude'], row['longitude']], radius = 1, color=getColor(row["clusters_step2"])).add_to(map)

# Un marker-popup pour chaque cluster à son centre (hormis le bruit)

    
map.save("map.html")



# Etape 3 : Même procédure pour le centre historique de Caen où la région est encore une fois plus dense
# Créer une colonne "cluster_step3", appliquer la même démarche et afficher les résultats avec les popups

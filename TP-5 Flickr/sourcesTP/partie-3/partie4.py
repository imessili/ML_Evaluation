# -*- coding: utf-8 -*-

import psycopg2
from googletrans import Translator
import json
import codecs
import ast
import re

### Filtrer seulement ceux étant alpha-numériques et pouvant contenir des traits d'union et des tirets bas
# re.match('^[a-z0-9_#-]+$', <tag>)
    
def supprimeAccent(mot):
    accents = { 'a': ['à', 'ã', 'á', 'â'],
                'e': ['é', 'è', 'ê', 'ë'],
                'i': ['î', 'ï'],
                'u': ['ù', 'ü', 'û'],
                'o': ['ô', 'ö'] }
    for (char, accented_chars) in accents.iteritems():
        for accented_char in accented_chars:
            mot = mot.replace(accented_char, char)
    return mot

def traitementTags(tagslist):
    global nb_requetes
    global trads
    stop_words = ["le", "la", "les", "un", "une", "des"]
    translator = Translator()
    for i in range(len(tagslist)):
        t = tagslist[i]
        if ':' in t or '=' in t:
            #suppression des tags de la forme 'uploaded:by=instagram'
            tagslist[i] = ''
        else:
            #traduction
            if t in trads:
                t = trads[t]
            tagslist[i] = t
    return tagslist



with codecs.open("traductions.json", 'r', encoding="utf-8") as trads_file:  
    trads = json.load(trads_file)
    trads = ast.literal_eval(trads)

# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 14:27:38 2020

@author: Willi
"""

import liwc                                       # pip install liwc      
from collections import Counter
import pandas as pd 

ruta  = "Utilities/LIWC_dictionaries/LIWC_English.dic"
parse, category_names = liwc.load_token_parser(ruta) 


def LIWC_ENGLISH(corpus):
    
    LIWC_categories = {key:0 for key in category_names}
    rows = []
    N_shape = len(corpus)
    
    for texto in corpus:
        tokens = texto.split()
        N = len(tokens)
        
        LIWC_n = Counter([category for token in tokens for category in parse(token)])
        LIWC_n = dict(LIWC_categories,**LIWC_n)
        LIWC_n = {k: v/N for k, v in LIWC_n.items()}      # Normalizar 
        rows.append(LIWC_n)
        
    return pd.DataFrame(rows)
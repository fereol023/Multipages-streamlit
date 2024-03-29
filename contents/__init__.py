import streamlit as st
import numpy as np
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium

from io import StringIO
from colour import Color
from streamlit_folium import st_folium
from folium.plugins import HeatMap


def clean_data(d):
    "Pour exercice 1"
    lot1 = [
        'Distance Covered In Possession',
        'Distance Covered Not In Possession',       
        'Distance Covered']
    for c in d.columns:
        if c in lot1:
            d[c] = d[c].apply(lambda r: float(str(r).replace('km', '')))
    lot2 = ['Top Speed']
    for c in d.columns:
        if c in lot2:
            d[c] = d[c].apply(lambda r: float(str(r).replace('km/h', '')))
    return d


def transform_names(d):
    """Pour exercice 2"""
    new_colnames = list(map(lambda m: m.replace('Code ', 'Code_'), d.columns))
    new_colnames = list(map(lambda m: m.replace(' ', ''), new_colnames))
    mapping = dict(zip(d.columns, new_colnames))
    return d.rename(columns=mapping, inplace=True) 

def numeric_cast(d, cols):
    """Force le type des colonnes en float en mettant np.nan lorsque ce n'est paspossible.
    param cols: liste de colonnes numériques.
    param d: jeu de données pd.DataFrame.
    """
    for c in d.columns:
        if c in cols:
            try:
                d[c] = d[c].astype(float)  
            except Exception as e:
                if type(e) == ValueError:
                    # remplacer les caractères non convertibles par des np.nan
                    d[c] = d[c].apply(lambda r: np.nan if r==' -     ' else float(r))
                else :
                    print(f'{c} : {e}')

def transform_villes(d):
    """Retirer les espaces avant et après le nom de la ville."""
    d['NomVille'] = d['NomVille'].apply(lambda r: r.rstrip().lstrip())
    d['MAJ'] = d['MAJ'].apply(lambda r: r.rstrip().lstrip())
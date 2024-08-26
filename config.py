# Paleta de colores personalizada
CUSTOM_PALETTE = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']

# Configuraciones de plots
PLOTLY_LAYOUT = {
    'title_font': {'size': 24, 'family': 'Consolas, sans-serif', 'color': '#333'},
    'legend_title_font': {'size': 14, 'color': '#555'},
    # Otros parámetros de configuración
}
# Librerías
import pandas as pd
import numpy as np
import streamlit as st
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
# 1. Bibliotecas estándar de Python
import os
import locale
from datetime import datetime

# 2. Bibliotecas de terceros

## Manipulación de datos
import pandas as pd
import numpy as np

## Visualización de datos
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## Machine Learning
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import classification_report, confusion_matrix

## Visualización interactiva
import streamlit as st
from streamlit_echarts import st_pyecharts
import pydeck as pdk
import streamlit.components.v1 as components
## Pyecharts
import pyecharts as py
from pyecharts.charts import Bar, Line, Grid, Candlestick
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# Paleta de colores personalizada

CUSTOM_PALETTE = ['#1F6AFF', '#FFA314', '#07B07F', '#E4637B', '#8846F3','#0ACB93','#E67086','#A574F8']

# Configuraciones de plots
PLOTLY_LAYOUT = {
    'title_font': {'size': 24, 'family': 'Consolas, sans-serif', 'color': '#333'},
    'legend_title_font': {'size': 14, 'color': '#555'},
    # Otros parámetros de configuración
}

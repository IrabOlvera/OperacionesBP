import streamlit as st
import pandas as pd
import pydeck as pdk

# Definir subheader
st.subheader("Inventarios generales", anchor="Stocks", help="Resumen general inventarios", divider="violet")

# Leer DataFrame
data_path = r'C:\Users\opera\OneDrive\Documentos\GitHub\OperacionesBP\pages\Inventarios\installments.csv'
df = pd.read_csv(data_path)

# Asegurarse de que 'qty' sea numérico
df['qty'] = pd.to_numeric(df['qty'], errors='coerce')

# Crear el DataFrame para el gráfico
chart_data = df[["lat", "long", "qty"]].copy()  # Asegúrate de que los nombres de columnas coincidan

# Definir el rango de colores para el heatmap
color_range = [
    [99, 110, 250, 255],   # #636EFA
    [239, 85, 59, 255],    # #EF553B
    [0, 204, 150, 255],    # #00CC96
    [171, 99, 250, 255],   # #AB63FA
    [255, 161, 90, 255]    # #FFA15A
]

# Crear y mostrar el gráfico en pydeck
st.pydeck_chart(
    pdk.Deck(
        map_provider='mapbox',
        map_style= 'light',
        initial_view_state=pdk.ViewState(
            height = 500,
            width = '150%',
            latitude=19.4343,
            longitude=-99.1933,
            zoom=5,
            pitch=0,
            tooltip = True
        ),
        layers=[
            # Usar HeatmapLayer en lugar de H3ClusterLayer
            pdk.Layer(
                "HeatmapLayer",
                data=chart_data,
                get_position='[long, lat]',
                get_weight="qty",  # Usar 'qty' como peso para el heatmap
                radiusPixels= 20,  # Ajusta el tamaño del radio
                colorRange=color_range,
                pickable = True
            ),
        ],
            ),
    )
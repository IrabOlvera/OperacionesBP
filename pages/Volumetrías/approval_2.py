from config import *
# Configuración de la página de Streamlit
st.set_page_config(page_title="Análisis de Approval", layout="wide")

# Título de la Aplicación
st.title("Análisis de Approval")

# -------------------------------
# Carga y Preparación de Datos
# -------------------------------

# Ruta al archivo CSV
data_path = r'C:\Users\opera\OneDrive\Documentos\GitHub\OperacionesBP\pages\Volumetrías\approval.csv'

# Cargar datos
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

df = load_data(data_path)

# Preprocesamiento de datos
df['mes'] = pd.to_datetime(df['mes'], dayfirst=True)
df['membership_number'] = df['membership_number'].astype(str)

# Agrupar datos por mes, Owner, response_code y Estatus
df_grouped = df.groupby(['mes', 'Owner', 'response_code', 'Estatus']).agg({'qty': 'sum'}).reset_index()

# Crear columna de mes en formato string para visualización
df_grouped['mes_str'] = df_grouped['mes'].dt.strftime('%Y-%m')

# Calcular el total de qty por mes y Owner para usar en el cálculo de porcentajes
df_grouped['total_qty'] = df_grouped.groupby(['mes', 'Owner'])['qty'].transform('sum')

# Calcular el porcentaje de cada response_code dentro del total de su grupo
df_grouped['percent'] = (df_grouped['qty'] / df_grouped['total_qty']) * 100

# -------------------------------
# Controles Interactivos
# -------------------------------

st.sidebar.header("Filtros")

# Filtro de meses
meses_disponibles = sorted(df_grouped['mes_str'].unique())
meses_seleccionados = st.sidebar.multiselect(
    "Selecciona los Meses",
    options=meses_disponibles,
    default=meses_disponibles[-3:]  # Últimos 3 meses por defecto
)

# Filtro de Owners
owners_disponibles = sorted(df_grouped['Owner'].unique())
owner_seleccionado = st.sidebar.selectbox(
    "Selecciona el Owner",
    options=owners_disponibles
)

# Filtro de Estatus
estatus_disponibles = sorted(df_grouped['Estatus'].unique())
estatus_seleccionados = st.sidebar.multiselect(
    "Selecciona los Estatus",
    options=estatus_disponibles,
    default=estatus_disponibles
)

# Filtrar datos según selecciones
df_filtered = df_grouped[
    (df_grouped['mes_str'].isin(meses_seleccionados)) &
    (df_grouped['Owner'] == owner_seleccionado) &
    (df_grouped['Estatus'].isin(estatus_seleccionados))
]

# Filtro de Response Codes basado en datos filtrados
response_codes_disponibles = sorted(df_filtered['response_code'].unique())
response_codes_seleccionados = st.sidebar.multiselect(
    "Selecciona los Response Codes",
    options=response_codes_disponibles,
    default=response_codes_disponibles
)

# Aplicar filtro de response codes
df_filtered = df_filtered[df_filtered['response_code'].isin(response_codes_seleccionados)]

# -------------------------------
# Verificación de Datos
# -------------------------------

if df_filtered.empty:
    st.warning("No hay datos disponibles para los filtros seleccionados.")
else:
    # -------------------------------
    # Visualización de Datos
    # -------------------------------

    # Pivotear datos para facilitar la visualización
    df_pivot = df_filtered.pivot_table(
        index='mes_str',
        columns='response_code',
        values='percent',  # Usar la columna 'percent' para los gráficos
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    # Ordenar meses cronológicamente
    df_pivot['mes_datetime'] = pd.to_datetime(df_pivot['mes_str'])
    df_pivot = df_pivot.sort_values('mes_datetime')

    # Seleccionar tipo de gráfico
    tipo_grafico = st.selectbox(
        "Selecciona el Tipo de Gráfico",
        options=["Líneas", "Barras Apiladas", "Heatmap"]
    )

    # -------------------------------
    # Gráfico de Líneas
    # -------------------------------
    if tipo_grafico == "Líneas":
        fig = go.Figure()
        for code in response_codes_seleccionados:
            fig.add_trace(go.Scatter(
                x=df_pivot['mes_str'],
                y=df_pivot[code],
                mode='lines+markers',
                name=f"Response Code {code}"
            ))
        fig.update_layout(
            title=f"Evolución de Response Codes (Porcentaje) para {owner_seleccionado}",
            xaxis_title="Mes",
            yaxis_title="Porcentaje (%)",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Gráfico de Barras Apiladas
    # -------------------------------
    elif tipo_grafico == "Barras Apiladas":
        fig = go.Figure()
        for code in response_codes_seleccionados:
            fig.add_trace(go.Bar(
                x=df_pivot['mes_str'],
                y=df_pivot[code],
                name=f"Response Code {code}"
            ))
        fig.update_layout(
            barmode='stack',
            title=f"Distribución de Response Codes (Porcentaje) por Mes para {owner_seleccionado}",
            xaxis_title="Mes",
            yaxis_title="Porcentaje (%)",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Heatmap
    # -------------------------------
    elif tipo_grafico == "Heatmap":
        fig = px.imshow(
            df_pivot[response_codes_seleccionados].T,
            labels=dict(x="Mes", y="Response Code", color="Porcentaje (%)"),
            x=df_pivot['mes_str'],
            y=response_codes_seleccionados,
            aspect="auto",
            color_continuous_scale='turbo'
        )
        fig.update_layout(
            title=f"Heatmap de Response Codes (Porcentaje) para {owner_seleccionado}"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Tabla de Datos
    # -------------------------------
    with st.expander("Mostrar Tabla de Datos"):
        st.dataframe(df_pivot.set_index('mes_str'), use_container_width=True)
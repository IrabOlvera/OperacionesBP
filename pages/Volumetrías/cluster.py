from config import *

# Definir subheader
st.subheader("Agrupacion", anchor="Agrupacion", help="Agrupación de datos", divider="violet")

# Cargar datos
data_path =  r'C:\Users\opera\OneDrive\Documentos\GitHub\OperacionesBP\pages\Volumetrías\vol_general.csv' # Asegúrate de definir data_path correctamente
df = pd.read_csv(data_path)

# Asegúrate de que la columna 'mes' está en el DataFrame
if 'mes' not in df.columns:
    st.error("La columna 'mes' no se encuentra en el DataFrame.")
else:
    # Intentar convertir 'mes' a datetime y manejar errores
    df['mes'] = pd.to_datetime(df['mes'], infer_datetime_format=True, dayfirst=True, errors='coerce')

    # Verificar si hay valores nulos después de la conversión
    invalid_dates = df['mes'].isnull().sum()
    if invalid_dates > 0:
        st.warning(f"Se encontraron {invalid_dates} fechas inválidas en la columna 'mes', se han eliminado del análisis.")
        df = df.dropna(subset=['mes'])

    # Ordenar y truncar 'mes' a YYYY-MM-DD
    df = df.sort_values(by='mes')
    df['mes'] = df['mes'].dt.to_period('M').dt.to_timestamp()

    # Limpiar columnas categóricas para evitar errores de tipo
    df['branch_office'] = df['branch_office'].astype(str).fillna('Desconocido')
    df['corporation'] = df['corporation'].astype(str).fillna('Desconocido')
    df['business'] = df['business'].astype(str).fillna('Desconocido')

    # -------------------------------
    # Controles Interactivos
    # -------------------------------

    st.sidebar.header("Filtros")

    # Filtro de meses
    meses_disponibles = sorted(df['mes'].dt.to_period('M').astype(str).unique())
    meses_seleccionados = st.sidebar.multiselect(
        "Selecciona los Meses",
        options=meses_disponibles,
        default=meses_disponibles[-3:]  # Últimos 3 meses por defecto
    )

    # Filtro de Corporations
    corporations_disponibles = sorted(df['corporation'].unique())
    corporation_seleccionadas = st.sidebar.multiselect(
        "Selecciona Corporation",
        options=corporations_disponibles,
        default=corporations_disponibles
    )

    # Filtro de Business
    business_disponibles = sorted(df['business'].unique())
    business_seleccionadas = st.sidebar.multiselect(
        "Selecciona Business",
        options=business_disponibles,
        default=business_disponibles
    )

    # Filtro de Branch Office
    branch_office_disponibles = sorted(df['branch_office'].unique())
    branch_office_seleccionadas = st.sidebar.multiselect(
        "Selecciona Branch Office",
        options=branch_office_disponibles,
        default=branch_office_disponibles
    )

    # Filtrar datos según selecciones
    df_filtered = df[
        (df['mes'].dt.to_period('M').astype(str).isin(meses_seleccionados)) &
        (df['corporation'].isin(corporation_seleccionadas)) &
        (df['business'].isin(business_seleccionadas)) &
        (df['branch_office'].isin(branch_office_seleccionadas))
    ]

    # Agrupar datos por columnas categóricas y sumar 'amount_one'
    df_grouped = df_filtered.groupby(['corporation', 'business', 'branch_office'])['amount_one'].sum().reset_index()

    # Codificación de columnas categóricas para clustering
    label_encoder = LabelEncoder()
    
    df_grouped['corporation_encoded'] = label_encoder.fit_transform(df_grouped['corporation'])
    df_grouped['business_encoded'] = label_encoder.fit_transform(df_grouped['business'])
    df_grouped['branch_office_encoded'] = label_encoder.fit_transform(df_grouped['branch_office'])

    # Preparar datos para clustering
    X = df_grouped[['corporation_encoded', 'business_encoded', 'branch_office_encoded', 'amount_one']]

    # Realizar clustering K-Means
    kmeans = KMeans(n_clusters=len(df_grouped['corporation'].unique()), random_state=0)
    df_grouped['cluster'] = kmeans.fit_predict(X)

    # Crear gráfico de clusters
    fig_clusters = go.Figure()

    # Graficar puntos de datos
    fig_clusters.add_trace(
        go.Scatter(
            x=df_grouped['amount_one'],
            y=df_grouped['branch_office_encoded'],
            mode='markers',
            marker=dict(color=df_grouped['cluster'], colorscale='Viridis', size=10),
            name='Datos'
        )
    )

    # Graficar centros de clúster
    centers = kmeans.cluster_centers_

    fig_clusters.add_trace(
        go.Scatter(
            x=centers[:, 3],  # Columna 'amount_one' para los centros
            y=centers[:, 2],  # Columna 'branch_office_encoded' para los centros
            mode='markers',
            marker=dict(size=15, color='white', symbol='x'),
            name='Centros de Clúster'
        )
    )

    # Configuración de etiquetas y títulos para la gráfica de clusters
    fig_clusters.update_layout(
        title='Resultado del Clustering K-Means',
        xaxis_title='Amount One',
        yaxis_title='Branch Office Encoded',
        height=600
    )

    # Mostrar la gráfica de clusters en Streamlit
    st.plotly_chart(fig_clusters)
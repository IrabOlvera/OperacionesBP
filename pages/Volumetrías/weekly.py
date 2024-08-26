from config import *

# Definir subheader
st.subheader("Análisis Semanal", anchor="Semanales", help="Selecciona las dimensiones a visualizar", divider="violet")

# Cargar datos
data_path = 'C:\\Users\\opera\\OneDrive\\Documentos\\GitHub\\OperacionesBP\\pages\\Volumetrías\\week.csv'
df = pd.read_csv(data_path)

# Conversión de columnas y limpieza
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%y')  # Asegúrate de ajustar el formato si es necesario
df['Sucursal'] = df['Sucursal'].astype(str).str.strip()
df['Error'] = df['Error'].astype(str).str.strip()
df['Owner'] = df['Owner'].astype(str).str.strip()
df['Tipo'] = df['Tipo'].astype(str).str.strip()
df['prod'] = df['prod'].astype(str).str.strip()

# -------------------------------
# Controles Interactivos
# -------------------------------
st.sidebar.header("Filtros")

# Filtro de fecha: rango de fechas
fecha_inicio = df['Fecha'].min()
fecha_fin = df['Fecha'].max()
fechas_disponibles = pd.date_range(start=fecha_inicio, end=fecha_fin).strftime('%Y-%m-%d').tolist()

fecha_inicio_seleccionada, fecha_fin_seleccionada = st.sidebar.date_input(
    "Selecciona el rango de fechas",
    [fecha_inicio, fecha_fin],
    min_value=fecha_inicio,
    max_value=fecha_fin
)

# Filtrar el DataFrame por el rango de fechas seleccionado
df_filtered = df[(df['Fecha'] >= fecha_inicio_seleccionada) & (df['Fecha'] <= fecha_fin_seleccionada)]

# Filtrar valores únicos según las selecciones actuales
corporativos_disponibles = sorted(df_filtered['Corporativo'].unique())
comercios_disponibles = sorted(df_filtered['Comercio'].unique())
sucursales_disponibles = sorted(df_filtered['Sucursal'].unique())
errores_disponibles = sorted(df_filtered['Error'].unique())
owners_disponibles = sorted(df_filtered['Owner'].unique())
tipos_disponibles = sorted(df_filtered['Tipo'].unique())
prods_disponibles = sorted(df_filtered['prod'].unique())

# Filtros de selección múltiple para los demás campos
corporativo_seleccionado = st.sidebar.multiselect("Selecciona los Corporativos", options=corporativos_disponibles)
comercio_seleccionado = st.sidebar.multiselect("Selecciona los Comercios", options=comercios_disponibles)
sucursal_seleccionada = st.sidebar.multiselect("Selecciona las Sucursales", options=sucursales_disponibles)
error_seleccionado = st.sidebar.multiselect("Selecciona los Errores", options=errores_disponibles)
owner_seleccionado = st.sidebar.multiselect("Selecciona los Owners", options=owners_disponibles)
tipo_seleccionado = st.sidebar.multiselect("Selecciona los Tipos", options=tipos_disponibles)
prod_seleccionado = st.sidebar.multiselect("Selecciona los Productos", options=prods_disponibles)

# Aplicar filtros adicionales
df_filtered = df_filtered[
    (df_filtered['Corporativo'].isin(corporativo_seleccionado) | (not corporativo_seleccionado)) &
    (df_filtered['Comercio'].isin(comercio_seleccionado) | (not comercio_seleccionado)) &
    (df_filtered['Sucursal'].isin(sucursal_seleccionada) | (not sucursal_seleccionada)) &
    (df_filtered['Error'].isin(error_seleccionado) | (not error_seleccionado)) &
    (df_filtered['Owner'].isin(owner_seleccionado) | (not owner_seleccionado)) &
    (df_filtered['Tipo'].isin(tipo_seleccionado) | (not tipo_seleccionado)) &
    (df_filtered['prod'].isin(prod_seleccionado) | (not prod_seleccionado))
]

# -------------------------------
# Gráficos
# -------------------------------

# Veces operadas
st.subheader("Veces Operadas")
veces_operadas = df_filtered.shape[0]
st.write(f"Total de veces operadas: {veces_operadas}")

# Monto total filtrando solo aprobada
st.subheader("Monto Total (Aprobadas)")
monto_aprobadas = df_filtered[df_filtered['Respuesta'] == 'APROBADA']['Monto total'].sum()
st.write(f"Monto total aprobado: {monto_aprobadas}")

# Agrupación por producto
st.subheader("Agrupación por Producto")
df_grouped_prod = df_filtered.groupby('prod').agg({'Monto total': 'sum'}).reset_index()
st.bar_chart(df_grouped_prod.set_index('prod'))
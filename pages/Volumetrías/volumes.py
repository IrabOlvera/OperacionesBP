from config import *
st.header("Volumetrías mensuales")
st.write("Revisión de los límites de operación por mes acumulado y corriente")

# Definir subheader
st.subheader("Análisis Mensual", anchor="Mensuales", help="Selecciona las dimensiones a visualizar", divider="violet")

# Leer DataFrame "volumes"
data_path = r'C:\Users\opera\OneDrive\Documentos\GitHub\OperacionesBP\pages\Volumetrías\volumes.csv'
df = pd.read_csv(data_path)

# Convertir la columna 'mes' al formato de fecha
df['mes'] = pd.to_datetime(df['mes'], format='%d/%m/%y')  # Ajusta el formato de fecha según sea necesario

# Añadir columna de orden para los meses
df['mes_order'] = df['mes'].dt.month
df['mes_str'] = df['mes'].dt.strftime('%B')  # Nombre del mes como cadena

# Selector para mostrar todas, Top 10 o Bottom 10 corporaciones
filter_type = st.radio(
    "Mostrar:",
    ('Todas las Corporaciones', 'Top 10 por TRX', 'Bottom 10 por TRX', 'Top 10 por Monto', 'Bottom 10 por Monto')
)

# Lógica para filtrar el DataFrame según la selección
if filter_type == 'Top 10 por TRX':
    filtered_df = df.nlargest(10, 'trx')
elif filter_type == 'Bottom 10 por TRX':
    filtered_df = df.nsmallest(10, 'trx')
elif filter_type == 'Top 10 por Monto':
    filtered_df = df.nlargest(10, 'mto')
elif filter_type == 'Bottom 10 por Monto':
    filtered_df = df.nsmallest(10, 'mto')
else:
    filtered_df = df  # Mostrar todas las corporaciones

# Crear selector de corporaciones en Streamlit
corporations = filtered_df['corporation'].unique().tolist()
selected_corporations = st.multiselect("Selecciona Corporación", corporations, default=corporations)

# Filtrar el DataFrame con base en la selección
filtered_df = filtered_df[filtered_df['corporation'].isin(selected_corporations)]

# Obtener todos los meses únicos para asegurar que todos estén en el gráfico
all_months = pd.date_range(start=df['mes'].min(), end=df['mes'].max(), freq='MS').strftime('%B').tolist()

# Crear gráficos de barras apiladas para Transacciones (TRX) y Montos (MTO)

# Crear gráfico de barras apiladas para Transacciones (TRX)
fig_trx = go.Figure()

# Añadir trazas para cada corporación
for corporation in selected_corporations:
    df_corp = filtered_df[filtered_df['corporation'] == corporation]
    df_corp = df_corp.groupby('mes_str').agg({'trx': 'sum'}).reindex(all_months, fill_value=0).reset_index()
    
    fig_trx.add_trace(go.Bar(
        x=df_corp['mes_str'],
        y=df_corp['trx'],
        name=corporation,
        marker_color=CUSTOM_PALETTE[selected_corporations.index(corporation) % len(CUSTOM_PALETTE)]
    ))

fig_trx.update_layout(
    title="Transacciones por Mes",
    xaxis_title="Mes",
    yaxis_title="Transacciones (TRX)",
    barmode='stack'
)

# Mostrar gráfico de barras apiladas en Streamlit
st.subheader("Transacciones (TRX)")
st.plotly_chart(fig_trx)

# Crear gráfico de barras apiladas para Montos (MTO)
fig_mto = go.Figure()

# Añadir trazas para cada corporación
for corporation in selected_corporations:
    df_corp = filtered_df[filtered_df['corporation'] == corporation]
    df_corp = df_corp.groupby('mes_str').agg({'mto': 'sum'}).reindex(all_months, fill_value=0).reset_index()
    
    fig_mto.add_trace(go.Bar(
        x=df_corp['mes_str'],
        y=df_corp['mto'],
        name=corporation,
        marker_color=CUSTOM_PALETTE[selected_corporations.index(corporation) % len(CUSTOM_PALETTE)]
    ))

fig_mto.update_layout(
    title="Montos por Mes",
    xaxis_title="Mes",
    yaxis_title="Montos (MTO)",
    barmode='stack'
)

# Mostrar gráfico de barras apiladas en Streamlit
st.subheader("Montos (MTO)")
st.plotly_chart(fig_mto)
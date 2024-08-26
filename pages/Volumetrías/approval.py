from config import *


# Leer el DataFrame
data_path = r'C:\Users\opera\OneDrive\Documentos\GitHub\OperacionesBP\pages\Volumetrías\approval.csv'
df = pd.read_csv(data_path)

# Convertir 'mes' a datetime
df['mes'] = pd.to_datetime(df['mes'], dayfirst=True)

# Asegurarse de que 'membership_number' sea texto
df['membership_number'] = df['membership_number'].astype(str)

# Filtrar solo las transacciones rechazadas
rechazos_df = df[df['Estatus'] != 'Aprobada']

# Agrupar por mes, Owner y Estatus, y sumar el volumen (qty)
rechazos_grouped = rechazos_df.groupby(['mes', 'Owner', 'Estatus']).agg({'qty': 'sum'}).reset_index()

# Calcular el porcentaje de rechazos por Owner
rechazos_grouped['porcentaje_rechazos'] = rechazos_grouped.groupby('Owner')['qty'].transform(lambda x: x / x.sum() * 100)

# Convertir la columna 'mes' a string para utilizarla en el selector de Streamlit
rechazos_grouped['mes_str'] = rechazos_grouped['mes'].dt.strftime('%Y-%m')

# Crear un pivot table para un formato más fácil de visualizar en Streamlit
rechazos_pivot = rechazos_grouped.pivot_table(index=['mes_str', 'Owner'], columns='Estatus', values='porcentaje_rechazos', fill_value=0)

# Asegurarse de que rechazos_pivot tenga un MultiIndex
rechazos_pivot = rechazos_pivot.reset_index().set_index(['mes_str', 'Owner'])

# Seleccionar los meses a visualizar
meses_disponibles = rechazos_grouped['mes_str'].unique()
meses_seleccionados = st.multiselect("Selecciona los meses a visualizar", options=meses_disponibles, default=list(meses_disponibles))

# Filtrar los datos según los meses seleccionados
datos_filtrados = rechazos_pivot.loc[rechazos_pivot.index.get_level_values('mes_str').isin(meses_seleccionados)]

# Crear gráfico de barras
fig = go.Figure()

owners = datos_filtrados.index.get_level_values('Owner').unique()

for owner in owners:
    for mes in meses_seleccionados:
        if (mes, owner) in datos_filtrados.index:
            datos_mes = datos_filtrados.loc[(mes, owner)]
            fig.add_trace(go.Bar(
                x=[owner],
                y=[datos_mes.sum()],
                name=f"{owner} - {mes}"
            ))

fig.update_layout(
    barmode='stack',
    title="Porcentaje de Rechazos por Owner y Mes",
    xaxis_title="Owner",
    yaxis_title="Porcentaje de Rechazos",
)

st.plotly_chart(fig)
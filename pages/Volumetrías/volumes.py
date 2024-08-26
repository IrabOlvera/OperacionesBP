from config import *

st.header("Volumetrías mensuales")
st.write("Revisión de los límites de operación por mes acumulado y corriente")

# Definir subheader
st.subheader("Análisis Mensual", anchor="Mensuales", help="Selecciona las dimensiones a visualizar", divider="violet")

# Leer DataFrame "volumes"

data_path = r'C:\Users\opera\OneDrive\Documentos\GitHub\OperacionesBP\pages\Volumetrías\volumes.csv'
df = pd.read_csv(data_path)

# Convertir 'mes' a datetime (día/mes/año con dos dígitos para el año)
df['mes'] = pd.to_datetime(df['mes'], format='%d/%m/%y')  # Ajustar el formato al de tus datos
df['mes_nombre'] = df['mes'].dt.strftime('%B')

# Ordenar por fecha
df.sort_values('mes', inplace=True)
df['ordinal'] = df['mes'].map(datetime.toordinal)

# Opciones de selección
options = ["Monto Total", "Transacciones","Ticket Promedio"]
selected_options = st.multiselect("Elige las dimensiones a visualizar", options, default=options)

# Crear subgráficas
fig = make_subplots(
    rows=len(selected_options), cols=1,
    subplot_titles=[f"{option}" for option in selected_options],
    shared_xaxes=True,
    vertical_spacing=0.2  # Ajustar el espaciado vertical entre subgráficas
)

# Graficar según las opciones seleccionadas
for i, option in enumerate(selected_options):
    if option == "Monto Total":
        # Graficar Monto Total
        fig.add_trace(
            go.Scatter(x=df['mes'], y=df['montotal'], mode='markers+lines', name='Monto Total'),
            row=i+1, col=1
        )
        
        # Calcular y graficar la línea de tendencia para Monto Total
        z = np.polyfit(df['ordinal'], df['montotal'], 1)
        p = np.poly1d(z)
        trend = p(df['ordinal'])
        fig.add_trace(
            go.Scatter(x=df['mes'], y=trend, mode='lines', name='Línea de Tendencia Monto Total', line=dict(dash='dash')),
            row=i+1, col=1
        )
    
    elif option == "Transacciones":
        # Graficar Transacciones
        fig.add_trace(
            go.Scatter(x=df['mes'], y=df['qty'], mode='markers+lines', name='Transacciones'),
            row=i+1, col=1
        )
        
        # Calcular y graficar la línea de tendencia para Transacciones
        z = np.polyfit(df['ordinal'], df['qty'], 1)
        p = np.poly1d(z)
        trend = p(df['ordinal'])
        fig.add_trace(
            go.Scatter(x=df['mes'], y=trend, mode='lines', name='Línea de Tendencia Transacciones', line=dict(dash='dash')),
            row=i+1, col=1
        )
    elif option == "Ticket Promedio":
        # Graficar Ticket promedio
        fig.add_trace(
            go.Scatter(x=df['mes'], y=df['Ticket promedio'], mode='markers+lines', name='Ticket promedio'),
            row=i+1, col=1
        )
        
        # Calcular y graficar la línea de tendencia para Transacciones
        z = np.polyfit(df['ordinal'], df['Ticket promedio'], 1)
        p = np.poly1d(z)
        trend = p(df['ordinal'])
        fig.add_trace(
            go.Scatter(x=df['mes'], y=trend, mode='lines', name='Línea de Tendencia Transacciones', line=dict(dash='dash')),
            row=i+1, col=1
        )

# Configuración de etiquetas y títulos
fig.update_layout(
    title='Análisis Mensual con Líneas de Tendencia',
    xaxis_title='Mes',
    xaxis_tickangle=-45,
    xaxis=dict(
        tickformat='%d/%m/%y'  # Formato de fecha para el eje x
    ),
    yaxis_title='Valor',
)

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig)
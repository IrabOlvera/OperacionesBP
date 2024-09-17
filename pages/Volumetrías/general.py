from config import *

# Definir subheader
st.subheader("Volumetría general", anchor="Generales", help="Volumenes Generales", divider="violet")

# Leer DataFrame "vol_general"
data_path = r'C:\Users\opera\OneDrive\Documentos\GitHub\OperacionesBP\pages\Volumetrías\vol_general.csv'
df = pd.read_csv(data_path)

# Convertir la columna 'mes' al formato de nombre de mes
df['mes'] = pd.to_datetime(df['mes'], format='mixed', dayfirst=True)
df['ordinal'] = df['mes'].map(lambda x: x.toordinal())

# Calcular las diferencias mensuales
df = df.sort_values('mes')
df['trx_diff'] = df['trx'].diff().fillna(0)
df['mto_diff'] = df['mto'].diff().fillna(0)

# Calcular línea de tendencia
def calculate_trend_line(y_values):
    x = np.arange(len(y_values))
    coeffs = np.polyfit(x, y_values, 1)  # Ajuste lineal
    trend_line = np.polyval(coeffs, x)
    return trend_line

# Gráfico de Barras para 'qtyb', 'qtys', 'pos'
bar_chart = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1000px", height="400px"))
    .add_xaxis(df['mes'].dt.strftime('%B').tolist())
    .add_yaxis("QtyB", df['qtyb'].tolist(), color=CUSTOM_PALETTE[0])
    .add_yaxis("QtyS", df['qtys'].tolist(), color=CUSTOM_PALETTE[1])
    .add_yaxis("POS", df['pos'].tolist(), color=CUSTOM_PALETTE[2])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Base Instalada Mensual"),
        xaxis_opts=opts.AxisOpts(name="Mes"),
        yaxis_opts=opts.AxisOpts(name="Cantidad"),
        legend_opts=opts.LegendOpts(pos_right="right")
    )
)

# Gráfico de Línea para 'mto' con diferencial y línea de tendencia
line_chart_mto = (
    Line(init_opts=opts.InitOpts(height="400px"))
    .add_xaxis(df['mes'].dt.strftime('%B').tolist())
    .add_yaxis(
        "Monto (MTO)", [m / 1e3 for m in df['mto'].tolist()],  # Convertir monto a miles para el gráfico
        is_smooth=True,
        color=CUSTOM_PALETTE[4],
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        "Tendencia MTO", [m / 1e3 for m in calculate_trend_line(df['mto'])],  # Línea de tendencia
        is_smooth=True,
        color="red",
        linestyle_opts=opts.LineStyleOpts(type_="dashed"),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Monto (MTO) por Mes"),
        xaxis_opts=opts.AxisOpts(name="Mes"),
        yaxis_opts=opts.AxisOpts(name="Monto (MTO) en Miles"),
        legend_opts=opts.LegendOpts(pos_right="right"),
    )
)

# Gráfico de Área para 'trx' con diferencial y línea de tendencia
area_chart_trx = (
    Line(init_opts=opts.InitOpts(height="400px"))
    .add_xaxis(df['mes'].dt.strftime('%B').tolist())
    .add_yaxis(
        "Transacciones (TRX)", df['trx'].tolist(),
        is_smooth=True,
        color=CUSTOM_PALETTE[3],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),  # Gráfico de área para TRX
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_yaxis(
        "Tendencia TRX", calculate_trend_line(df['trx']),
        is_smooth=True,
        color="blue",
        linestyle_opts=opts.LineStyleOpts(type_="dashed"),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Transacciones (TRX) por Mes"),
        xaxis_opts=opts.AxisOpts(name="Mes"),
        yaxis_opts=opts.AxisOpts(name="Transacciones (TRX)"),
        legend_opts=opts.LegendOpts(pos_right="right"),
    )
)

# Mostrar gráficos de forma separada en Streamlit
st.title("Datos Generales Operacion")

# Mostrar el gráfico de barras
st_pyecharts(bar_chart)

# Añadir un espacio entre los gráficos
st.write("")  
st.write("")  

# Cambiar el color del subtítulo del gráfico de línea
st.markdown('<p style="color:#EBEFF4; font-size:20px;">Monto (MTO) por Mes</p>', unsafe_allow_html=True)

# Mostrar el gráfico de línea para Monto
st_pyecharts(line_chart_mto)

# Añadir un espacio entre los gráficos
st.write("")  
st.write("")  

# Cambiar el color del subtítulo del gráfico de área
st.markdown('<p style="color:#EBEFF4; font-size:20px;">Transacciones (TRX) por Mes</p>', unsafe_allow_html=True)

# Mostrar el gráfico de área para Transacciones
st_pyecharts(area_chart_trx)
from config import *
# Importa y configura las páginas que deseas mostrar
welcome = st.Page("pages/welcome.py", title="Bienvenida", icon=":material/home:", default=True)
explore = st.Page("pages/Exploratorio/explore.py", title="Exploratorio - regresión", icon=":material/leaderboard:")
general = st.Page("pages/Volumetrías/general.py", title="Generales", icon=":material/stacked_bar_chart:") #General quedó completo 16092024 - no es necesario mover nada más Irab del futuro
cluster = st.Page("pages/Volumetrías/cluster.py", title="Agrupacion", icon=":material/stacked_bar_chart:")
volumetries = st.Page("pages/Volumetrías/volumes.py", title="Volumetrías", icon=":material/assessment:")
weekly = st.Page("pages/Volumetrías/weekly.py", title="Volumetrías semanales", icon=":material/view_week:")
approval = st.Page("pages/Volumetrías/approval.py", title="Aprobación", icon=":material/price_check:")
approval_2 = st.Page("pages/Volumetrías/approval_2.py", title="Desglose de errores", icon=":material/trending_down:")
chargebacks = st.Page("pages/Volumetrías/chargebacks.py", title="Contracargos", icon=":material/assignment_returned:")
stocks = st.Page("pages/Inventarios/stocks.py", title="Inventarios", icon=":material/sell:")
products = st.Page("pages/Productos/products.py", title="Producto", icon=":material/star:")

# Configuración de navegación sin estado de sesión
pg = st.navigation(
    {
        "Menú Principal": [welcome, explore],
        "Volumetrías": [general , volumetries, weekly], # falta corregir el cluster que va por ahí y approval se va a modificar approval, approval_2, chargebacks
        "Inventarios": [stocks], # faltan páginas
        "Productos": [products]  # Y aquí también
    }
)

# Ejecutar la navegación
pg.run()

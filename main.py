from config import *
# Importa y configura las páginas que deseas mostrar
welcome = st.Page("pages/welcome.py", title="Bienvenida", icon=":material/home:", default=True)
volumetries = st.Page("pages/Volumetrías/volumes.py", title="Volumetrías", icon=":material/assessment:")
weekly = st.Page("pages/Volumetrías/weekly.py", title="Volumetrías semanales", icon=":material/view_week:")
approval = st.Page("pages/Volumetrías/approval.py", title="Aprobación", icon=":material/price_check:")
approval_2 = st.Page("pages/Volumetrías/approval_2.py", title="Desglose de errores", icon=":material/trending_down:")
chargebacks = st.Page("pages/Volumetrías/chargebacks.py", title="Contracargos", icon=":material/assignment_returned:")
stocks = st.Page("pages/Inventarios/generales.py", title="Inventarios", icon=":material/sell:")
products = st.Page("pages/Productos/products.py", title="Producto", icon=":material/star:")

# Configuración de navegación sin estado de sesión
pg = st.navigation(
    {
        "Menú Principal": [welcome],
        "Volumetrías": [volumetries, weekly, approval, approval_2, chargebacks],
        "Inventarios": [stocks], # faltan páginas
        "Productos": [products]  # Y aquí también
    }
)

# Ejecutar la navegación
pg.run()

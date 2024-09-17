from config import *

# Definir subheader
st.subheader("Análisis exploratorio", anchor="Explore", help="Exploratorio de investigación")

# Cargar datos
data_path = 'C:\\Users\\opera\\OneDrive\\Documentos\\GitHub\\OperacionesBP\\pages\\Exploratorio\\explore.csv'

try:
    df = pd.read_csv(data_path)
    st.write("Datos cargados correctamente.")
except FileNotFoundError:
    st.error(f"No se pudo encontrar el archivo en la ruta: {data_path}")
    st.stop()

# Verificar las columnas disponibles
st.write(df.columns)

# Si 'bin' es categórica, asegúrate de que se haya codificado correctamente
if 'bin' in df.columns and df['bin'].dtype == 'object':
    df = pd.get_dummies(df, columns=['bin'], drop_first=True)
else:
    st.write("'bin' column is missing or not categorical.")

# Preparar los datos
X = df[['bin', 'id_business', 'montotal']]
y = df['Chargeback']

# División de los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entrenar el modelo
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predecir en los datos de prueba
y_pred = model.predict(X_test)

# Evaluar el modelo
st.write("Confusion Matrix:")
st.write(confusion_matrix(y_test, y_pred))
st.write("Classification Report:")
st.write(classification_report(y_test, y_pred))

# Importancia de las características
feature_importances = pd.Series(model.feature_importances_, index=X.columns)
st.write("Feature Importances:")
st.write(feature_importances.sort_values(ascending=False))

# Gráfico de Barras por id_business
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='id_business', palette='viridis')
plt.title('Cantidad de Transacciones por id_business')
plt.xlabel('id_business')
plt.ylabel('Cantidad')
st.pyplot()
plt.close()

# Boxplot de Montos (montotal) por id_business
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='id_business', y='montotal', palette='viridis')
plt.title('Distribución de Montos (montotal) por id_business')
plt.xlabel('id_business')
plt.ylabel('Monto Total (montotal)')
st.pyplot()
plt.close()

# Scatter Plot de montotal vs id_business con hue en Chargeback
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='montotal', y='id_business', hue='Chargeback', palette='viridis')
plt.title('Relación entre Monto Total (montotal) y id_business')
plt.xlabel('Monto Total (montotal)')
plt.ylabel('id_business')
st.pyplot()
plt.close()

# Gráfico de Calor de la Correlación
plt.figure(figsize=(10, 6))
correlation = df[['montotal', 'id_business']].corr()
sns.heatmap(correlation, annot=True, cmap='viridis', vmin=-1, vmax=1)
plt.title('Mapa de Calor de la Correlación')
st.pyplot()
plt.close()
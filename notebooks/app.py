import streamlit as st
import pandas as pd
import plotly.express as px


# st.title("Dashboard de Accidentes en México") # Muestra el título 
# st.write("Primera prueba de carga exitosa.") # Muestra un mensaje


@st.cache_data # Utilizamos cache para mejorar el rendimiento
#Función para cargar los datos desde un archivo CSV
def cargar_datos():
    return pd.read_csv("data/accidentes_cdmx_limpio.csv", parse_dates=["fecha_evento"]) #Parseamos la columna de fecha como tipo datetime

df = cargar_datos() # Cargamos los datos

# st.write("Número total de accidentes:", len(df)) # Mostramos un mensaje con el número total de accidentes


# fecha_min = df["fecha_evento"].min().date()
# fecha_max = df["fecha_evento"].max().date()

# st.write(f"Rango de fechas en los datos: {fecha_min} — {fecha_max}")

# num_alcaldias = df["alcaldia"].nunique()
# st.write(f"Número de alcaldías registradas: {num_alcaldias}")

# # Crear columna de mes (si no existe ya)
# df["mes"] = df["fecha_evento"].dt.month

# # Diccionario para traducir número de mes a nombre en español
# meses_es = {
#     1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
#     5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
#     9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
# }

# # Conteo de accidentes por mes y orden de enero a diciembre
# conteo_meses = df["mes"].value_counts().sort_index()
# conteo_meses.index = conteo_meses.index.map(meses_es)

# # Crear gráfico con Plotly
# fig = px.bar(
#     x=conteo_meses.index,
#     y=conteo_meses.values,
#     title="📅 Accidentes por Mes",
#     labels={'x': 'Mes', 'y': 'Número de accidentes'},
#     text=conteo_meses.values
# )

# fig.update_layout(
#     xaxis_title='Mes',
#     yaxis_title='Número de accidentes'
# )

# # Mostrar en Streamlit
# st.plotly_chart(fig, use_container_width=True)

##########################################################

# Creamos columnas
col1, col2, col3 = st.columns(3)

# Usamos 'with' para colocar los elementos dentro de cada columna del layout
with col1:
    st.metric("Total de accidentes", f"{len(df):,}") # Muestra el número total de accidentes
with col2:
    fecha_min = df["fecha_evento"].min().date() # Obtiene la fecha mínima
    fecha_max = df["fecha_evento"].max().date() # Obtiene la fecha máxima
    st.write(f"Rango de fechas en los datos: {fecha_min} — {fecha_max}") # Muestra el rango de fechas en los datos
with col3:
    num_alcaldias = df["alcaldia"].nunique() # Obtiene el número de alcaldías únicas
    st.write(f"Número de alcaldías registradas: {num_alcaldias}") # Muestra el número de alcaldías registradas

st.markdown("---")
st.subheader("📊 Visualización de accidentes por mes")

# Creamos columna de mes
df["mes"] = df["fecha_evento"].dt.month

# Diccionario para traducir número de mes a nombre en español
meses_es = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

# Conteo de accidentes por mes y orden de enero a diciembre
conteo_meses = df["mes"].value_counts().sort_index() # Contamos los accidentes por mes y ordenamos por índice
conteo_meses.index = conteo_meses.index.map(meses_es) # Mapeamos los números de mes a nombres en español

# Creamos gráfico con Plotly
fig = px.bar(
    x=conteo_meses.index,  # Índice del conteo de accidentes (meses)
    y=conteo_meses.values, # Valores del conteo de accidentes
    labels={'x': 'Mes', 'y': 'Número de accidentes'}, 
    text=conteo_meses.values # Texto que se mostrará en las barras del gráfico
)

# Mostrar en Streamlit
st.plotly_chart(fig, use_container_width=True)
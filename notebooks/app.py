import pandas as pd
import streamlit as st
import plotly.express as px

# Cargamos el archivo CSV y convertimos la columna 'fecha_evento' a tipo datetime
df = pd.read_csv("data/accidentes_cdmx_limpio.csv", parse_dates=["fecha_evento"])
# parse_dates: Convierte la columna a tipo datetime

# Extraemos el mes de la columna fecha_evento para análisis temporal
df["mes"] = df["fecha_evento"].dt.month
# dt.month: Extrae el número de mes de una fecha (1=enero, 12=diciembre)

# Mostramos una vista previa del DataFrame
# st.subheader("🧾 Vista previa del DataFrame")  # st.subheader: Agrega un subtítulo visual en la app
# st.dataframe(df.head())  # st.dataframe: Muestra un DataFrame interactivo, head(): muestra las primeras filas


# ----------------------------------------------------
# 🔹 Sidebar con filtros interactivos
# sidebar: Panel lateral para filtros y opciones
# ----------------------------------------------------
with st.sidebar.expander("🔎 Filtros interactivos", expanded=True): 
# with: # en streamlit, todo lo que ponga aquí aparece dentro del panel
# st.sidebar.expander: Crea un panel lateral que se puede expandir o contraer
# expanded=True: El panel se muestra expandido por defecto 

    st.markdown("### 🏙️ Alcaldías")  # st.markdown: Muestra texto con formato Markdown
    alcaldias = sorted(df["alcaldia"].unique()) 
    # sorted: Ordena las alcaldías alfabéticamente
    # df["alcaldia"].unique(): Obtiene las alcaldías única

    cols = st.columns(2)  # Creamos dos columnas para distribuir las casillas de verificación
    # st.columns: Crea columnas para organizar el layout

    alcaldias_seleccionadas = []  # Lista para almacenar las alcaldías seleccionadas

    seleccionar_todas = st.checkbox("Seleccionar todas", value=False)  
    if seleccionar_todas:
        alcaldias_seleccionadas = alcaldias
    else:
        # Recorremos las alcaldías
        for i, alcaldia in enumerate(alcaldias): 
            col = cols[i % 2] # Alternamos columnas usando módulo
            if col.checkbox(alcaldia, key=alcaldia):  # Casilla de verificación para cada alcaldía
                alcaldias_seleccionadas.append(alcaldia) # Añade la alcaldía a la lista si está seleccionada
            # Checkbox: Crea una casilla de verificación para cada alcaldía
            # append: Añade un elemento a la lista
        


    st.divider()  # st.divider: Agrega una línea divisoria visual

    # checkbox para seleccionar todas las alcaldías
    
  

    # Lista de meses abreviados en orden
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    
    st.markdown("### 📆 Selecciona el rango de meses:") # Muestra texto en markdown
    # Slider (deslizador) con meses
    mes_inicio, mes_fin = st.select_slider( # salida: tupla con mes de inicio y fin
        label=" ", # texto que aparece arriba del slider
        options=meses, #Opciones del slider se le pasa la lista de meses
        value=("Enero", "Diciembre") #Valores iniciales seleccionados
    )


# ----------------------------------------------------
# 🔹 Filtrar datos según selección
# ----------------------------------------------------
# Convertimos los nombres de meses a números

meses_numeros = {mes: i + 1 for i, mes in enumerate(meses)}  # Diccionario: nombre de mes → número (Enero: 1, ..., Diciembre: 12)
mes_inicio_num = meses_numeros[mes_inicio] # Convierte el mes de inicio a número
mes_fin_num = meses_numeros[mes_fin] # Convierte el mes de fin a número

# Creamos un DataFrame (datadrame: tabla de datos)
df_filtrado = df[
    # Filtra filas donde la alcaldía esté en la lista seleccionada por el usuario
    (df["alcaldia"].isin(alcaldias_seleccionadas)) &
    
    # Filtra filas donde el número del mes esté entre el inicio y fin seleccionados
    (df["mes"].between(mes_inicio_num, mes_fin_num))
]


# ----------------------------------------------------
# 🔹 Encabezado y métricas
# ----------------------------------------------------
st.title("🚦 Dashboard de Accidentes CDMX") # Título principal
st.subheader("📌 Indicadores principales") # Subtítulo


col1, col2, col3 = st.columns(3) # Creamos tres columnas para mostrar las métricas

# len() cuenta el número de filas en el DataFrame filtrado (total de accidentes)
col1.metric("📍 Total de Accidentes", len(df_filtrado))

# sum() suma todos los valores de la columna 'personas_lesionadas'
col2.metric("🩹 Personas Lesionadas", int(df_filtrado["personas_lesionadas"].sum()))

# sum() suma todos los valores de la columna 'personas_fallecidas'
col3.metric("⚰️ Personas Fallecidas", int(df_filtrado["personas_fallecidas"].sum()))


st.divider()

# ----------------------------------------------------
# 🔹 Gráfico de accidentes por mes
# ----------------------------------------------------

# Subtítulo para la sección del gráfico en el dashboard
st.subheader("📊 Distribución mensual de accidentes")


# Agrupamos los datos por número de mes y contamos cuántos accidentes hay en cada mes
# groupby("mes") agrupa por mes (1 a 12)
# size() cuenta las filas (accidentes) por grupo
# reset_index(name="accidentes") convierte la serie en DataFrame y nombra la columna
accidentes_por_mes = df_filtrado.groupby("mes").size().reset_index(name="accidentes")

# Invertimos el diccionario: número → nombre del mes
# Esto es necesario para mostrar nombres como "Enero", "Febrero", etc.
numeros_a_meses = {v: k for k, v in meses_numeros.items()}

# map() reemplaza el número del mes por su nombre (1 → "Enero", etc.)
accidentes_por_mes["mes_nombre"] = accidentes_por_mes["mes"].map(numeros_a_meses)

# Lista ordenada de nombres de meses para que aparezcan en orden cronológico
orden_meses = list(meses_numeros.keys())  # ["Enero", "Febrero", ..., "Diciembre"]

# Creamos el gráfico de barras
# x = "mes_nombre" para mostrar etiquetas con nombres
# y = "accidentes" para mostrar el conteo
# category_orders asegura que los meses no salgan en orden alfabético
#labels define las etiquetas de los ejes
fig = px.bar(
    accidentes_por_mes,
    x="mes_nombre",
    y="accidentes",
    category_orders={"mes_nombre": orden_meses},
    labels={"mes_nombre": "Mes", "accidentes": "Número de accidentes"},
    title="Número de accidentes por mes",
    color_discrete_sequence=["#FF6361"]
)

# Mostramos el gráfico en el dashboard ocupando todo el ancho disponible
st.plotly_chart(fig, use_container_width=True)

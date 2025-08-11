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

    seleccionar_todas = st.checkbox("Seleccionar todas", value=True)  
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


    # checkbox para seleccionar todas las alcaldías

    # Lista de meses abreviados en orden
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    # Slider (deslizador) con meses
    mes_inicio, mes_fin = st.select_slider( # salida: tupla con mes de inicio y fin
        label="📆 Selecciona el rango de meses:", # texto que aparece arriba del slider
        options=meses, #Opciones del slider se le pasa la lista de meses
        value=("Enero", "Diciembre") #Valores iniciales seleccionados
    )

    # checkbox para seleccionar tipos de evento
    st.markdown("### 🚨 Tipo de evento")
    tipos_evento = sorted(df["tipo_evento"].dropna().unique())
    # Creamos dos columnas para los checkboxes
    columnas = st.columns(2)

    tipo_evento_seleccionado = [] # Lista para almacenar los tipos de evento seleccionados
    seleccionar_todos_eventos = st.checkbox("Seleccionar todos", value=True)
    # Casilla de verificación para seleccionar todos los tipos de evento
    if seleccionar_todos_eventos:
        tipo_evento_seleccionado = tipos_evento
    else: # Si no se seleccionan todos, se muestran los checkboxes individuales
        for i, tipo_evento in enumerate(tipos_evento):
            col = columnas[i % 2]  # Alternamos columnas usando módulo
            if col.checkbox(tipo_evento, key=tipo_evento):
                tipo_evento_seleccionado.append(tipo_evento)


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

# Creamos un DataFrame para los tipos de evento seleccionados
df_filtrado_eventos = df[
    (df["tipo_evento"].isin(tipo_evento_seleccionado))
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

# ----------------------------------------------------
# 🗺️ Mapa interactivo de accidentes geolocalizados
# ----------------------------------------------------
st.subheader("🗺️ Mapa de Accidentes por Coordenadas")  # st.subheader: Agrega un subtítulo visual en la app

# Verificamos que existan columnas de latitud y longitud en el DataFrame filtrado
if "latitud" in df_filtrado_eventos.columns and "longitud" in df_filtrado_eventos.columns:
    
    # dropna(): Elimina las filas donde 'latitud' o 'longitud' tengan valores nulos
    df_mapa = df_filtrado_eventos.dropna(subset=["latitud", "longitud"])

    # Verificamos que el DataFrame no esté vacío
    if not df_mapa.empty:
        # fig_mapa: Gráfico de mapa que se mostrará en la app
        # px.scatter_mapbox(): Crea un mapa de puntos usando coordenadas
        # lat / lon: Columnas que contienen las coordenadas
        # hover_name: Texto principal que se muestra al pasar el cursor
        # hover_data: Columnas adicionales que se muestran al pasar el cursor
        # color: Columna usada para diferenciar los puntos por color
        # zoom: Nivel inicial de acercamiento del mapa
        # height: Altura del gráfico en píxeles
        fig_mapa = px.scatter_mapbox(
            df_mapa,
            lat="latitud",
            lon="longitud",
            hover_name="tipo_evento",
            hover_data=["alcaldia", "fecha_evento", "personas_lesionadas", "personas_fallecidas"],
            color="tipo_evento",
            zoom=10,
            height=600
        )

        #fig_mapa: Gráfico de mapa que se mostrará en la app
        # update_layout(): Ajusta el diseño del gráfico
        # mapbox_style: Estilo del mapa (carto-positron es gratuito y claro)
        # margin: Márgenes del gráfico (en píxeles)
        # title: Título que aparece encima del mapa
        fig_mapa.update_layout(
            mapbox_style="carto-positron",
            margin={"r":0, "t":30, "l":0, "b":0},
            title="Ubicación de accidentes en CDMX"
        )

        # st.plotly_chart(): Muestra el gráfico en Streamlit
        # use_container_width=True: Ajusta el gráfico al ancho disponible en pantalla
        st.plotly_chart(fig_mapa, use_container_width=True)
    else:
        # Mensaje informativo si después de eliminar nulos no hay datos
        st.info("No hay datos con coordenadas disponibles para los filtros seleccionados.")
else:
    # Advertencia si las columnas de coordenadas no existen en el DataFrame
    st.warning("Las columnas 'latitud' y 'longitud' no están disponibles en el DataFrame.")

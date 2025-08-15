# Módulo para generación de visualizaciones en el dashboard
# Contiene funciones que reciben un DataFrame filtrado y devuelven figuras de Plotly Express.

from __future__ import annotations
import pandas as pd                      # Manipulación de datos tabulares
import plotly.express as px              # Gráficos interactivos
from .theme import (
    PALETA,          # Paleta de colores corporativa (lista de hex o nombres)
    TEMPLATE,        # Template de Plotly (tipografía, fondos, grids, etc.)
    DIAS_SEMANA,     # Catálogo opcional (no usado en estas funciones)
    MESES,           # ["Enero", "Febrero", ..., "Diciembre"] en orden natural
    NUM_A_MESES,     # {1:"Enero", 2:"Febrero", ..., 12:"Diciembre"}
    MAPBOX_STYLE,    # Estilo del mapa (p.ej. "carto-positron" o "open-street-map")
)

# -----------------------------------------------------------------------------
# 1) Barras por mes
# -----------------------------------------------------------------------------
def fig_accidentes_por_mes(df: pd.DataFrame):
    """
    Construye un gráfico de barras con el número de accidentes por mes.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame ya filtrado con una columna 'mes' (int 1-12).

    Retorna
    -------
    plotly.graph_objs._figure.Figure
        Figura de Plotly. Si df está vacío, devuelve una figura con título informativo.
    """
    # si no hay datos, devolvemos una figura vacía con el template
    if df.empty:
        return px.bar(title="Sin datos para el rango seleccionado", template=TEMPLATE)

    # Requisito mínimo: columna 'mes' presente y numérica
    if "mes" not in df.columns:
        # Creamos una figura con aviso para ayudar al diagnóstico
        fig = px.bar(title="No se encontró la columna 'mes' en el DataFrame", template=TEMPLATE)
        return fig

    # Agrupamos por número de mes y contamos accidentes (filas)
    # .size() → conteo por grupo; reset_index → convierte a DataFrame con columna 'accidentes'
    tmp = df.groupby("mes").size().reset_index(name="accidentes")

    # Mapeamos número → nombre de mes (1→"Enero", ..., 12→"Diciembre")
    # NUM_A_MESES viene del theme para mantener consistencia del catálogo
    tmp["mes_nombre"] = tmp["mes"].map(NUM_A_MESES)

    # Creamos gráfico ordenando por el orden natural de los meses (MESES)
    fig = px.bar(
        tmp,
        x="mes_nombre",
        y="accidentes",
        category_orders={"mes_nombre": MESES},  # evita orden alfabético
        labels={"mes_nombre": "Mes", "accidentes": "Número de accidentes"},
        title="Número de accidentes por mes",
        color_discrete_sequence=[PALETA[0]],    # color corporativo para la serie
        template=TEMPLATE
    )

    # mejorar legibilidad de etiquetas
    fig.update_layout(xaxis_title="Mes", yaxis_title="Accidentes")
    return fig


# -----------------------------------------------------------------------------
# 2) Mapa de incidentes
# -----------------------------------------------------------------------------
def fig_mapa_incidentes(df: pd.DataFrame):
    """
    Renderiza un mapa de puntos (scatter_mapbox) con incidentes georreferenciados.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame filtrado con columnas 'latitud', 'longitud' y opcionalmente:
        'tipo_evento', 'alcaldia', 'fecha_evento', 'personas_lesionadas', 'personas_fallecidas'.

    Retorna
    -------
    plotly.graph_objs._figure.Figure | None
        Figura de Plotly si hay coordenadas válidas; None si no hay datos geográficos.
    """
    # Guardas defensivas: verificar que existan columnas mínimas
    if df.empty or not {"latitud", "longitud"}.issubset(df.columns):
        return None

    # Eliminamos filas con lat/long nulas para evitar errores en el mapa
    m = df.dropna(subset=["latitud", "longitud"])
    if m.empty:
        return None

    # Creamos el mapa: cada fila con coordenadas dibuja un punto
    # hover_*: información útil al pasar el cursor
    fig = px.scatter_mapbox(
        m,
        lat="latitud",
        lon="longitud",
        hover_name="tipo_evento",   # título del hover
        hover_data=[
            "alcaldia",
            "fecha_evento",
            "personas_lesionadas",
            "personas_fallecidas",
        ],
        color="tipo_evento",        # colorea por tipo de evento (categoría)
        zoom=10,                    # zoom inicial (ajústalo si trabajas otro estado/ciudad)
        height=600                  # altura del contenedor del gráfico
    )

    # Estilo del mapa + márgenes + template general del dashboard
    fig.update_layout(
        mapbox_style=MAPBOX_STYLE,
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        title="Ubicación de accidentes en CDMX",
        template=TEMPLATE
    )

    return fig



def fig_accidentes_por_hora(df: pd.DataFrame):
    """
    Genera un gráfico de barras que muestra la distribución de accidentes por hora del día (0 a 23).

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame filtrado que debe contener una columna 'hora' con valores enteros (0 a 23).

    Retorna
    -------
    plotly.graph_objs._figure.Figure
        Gráfico de barras con la cantidad de accidentes por cada hora del día.
        Si el DataFrame está vacío o no tiene la columna 'hora', se devuelve una figura vacía.
    """

    # Validación: si el DataFrame está vacío o no tiene la columna 'hora', mostrar mensaje
    if df.empty or "hora" not in df.columns:
        return px.bar(title="Sin datos para mostrar", template=TEMPLATE)

    # Agrupar: contar cuántos accidentes hay por cada hora (0 a 23)
    # .astype(int): asegura que los valores sean enteros
    # .value_counts(): cuenta ocurrencias por hora
    # .reindex(range(24), fill_value=0): asegura que aparezcan todas las horas (aunque algunas sean 0)
    tmp = df["hora"].astype(int).value_counts().reindex(range(24), fill_value=0).reset_index()
    tmp.columns = ["hora", "accidentes"]  # renombrar columnas

    # Crear gráfico de barras
    fig = px.bar(
        tmp,
        x="hora",
        y="accidentes",
        title=" ",  # Título vacío porque se suele poner un subtítulo desde app.py
        labels={"hora": "Hora (0–23)", "accidentes": "Número de accidentes"},
        text="accidentes",  # muestra el valor encima de cada barra
        template=TEMPLATE,  # aplica el estilo global del dashboard
        color_discrete_sequence=[PALETA[1]],  # segundo color de la paleta definida en theme.py
    )

    # Ajustes visuales del gráfico
    fig.update_layout(
        xaxis=dict(dtick=1),      # mostrar todas las horas (0–23) en el eje X
        yaxis_title="Accidentes"  # título del eje Y
    )
    fig.update_traces(textposition="outside")  # mostrar los números fuera de las barras

    return fig


def fig_heatmap_hora_dia(df: pd.DataFrame):
    """
    Genera un heatmap (mapa de calor) con el número de accidentes distribuidos
    por hora del día (0–23) y día de la semana (Lunes–Domingo).

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame que debe contener las columnas 'hora' y 'dia_semana_nombre'.

    Retorna
    -------
    plotly.graph_objs._figure.Figure
        Figura tipo heatmap. Si no hay datos o columnas requeridas, devuelve un heatmap vacío.
    """

    # Validación: si no hay datos o faltan columnas clave, devolver heatmap vacío con aviso
    if df.empty or not {"hora", "dia_semana_nombre"}.issubset(df.columns):
        return px.imshow(
            [[0]*24]*7,                   # Matriz 7x24 vacía (7 días, 24 horas)
            x=list(range(24)),            # Eje X: horas del día (0 a 23)
            y=DIAS_SEMANA,                # Eje Y: días de la semana ordenados
            title="Sin datos para construir el heatmap",
            template=TEMPLATE
        )

    # Asegura que los valores de hora estén en rango válido (0–23)
    df["hora"] = df["hora"].astype("Int64").clip(0, 23)

    # Crear tabla dinámica: filas = día, columnas = hora, valores = cuenta de accidentes
    # aggfunc='count': cuenta cuántos registros hay por combinación día-hora
    # fill_value=0: completa con ceros donde no hay datos
    tabla = (
        df.pivot_table(
            index="dia_semana_nombre",   # filas: días
            columns="hora",              # columnas: horas
            values="tipo_evento",        # cuenta eventos para llenar la celda
            aggfunc="count",
            fill_value=0
        )
        .reindex(index=DIAS_SEMANA, columns=list(range(24)), fill_value=0)
        # reindex: asegura orden correcto de días (L–D) y todas las horas (0–23)
    )

    # Crear heatmap usando px.imshow
    fig = px.imshow(
        tabla.values,                   # matriz de valores
        labels=dict(
            x="Hora del día",
            y="Día de la semana",
            color="Accidentes"
        ),
        x=tabla.columns,               # etiquetas del eje X
        y=tabla.index,                 # etiquetas del eje Y
        title="Heatmap: Accidentes por hora y día de la semana",
        template=TEMPLATE,
        color_continuous_scale="YlOrRd"  # escala de colores cálida
    )

    # Asegura que el eje X se interprete como categorías (no números continuos)
    fig.update_xaxes(type="category")

    return fig



def fig_treemap_accidentes_por_alcaldia(df: pd.DataFrame):
    """
    Genera un treemap (diagrama de árbol) que muestra la cantidad de accidentes por alcaldía.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame con una columna 'alcaldia' que identifica la ubicación del accidente.

    Retorna
    -------
    plotly.graph_objs._figure.Figure
        Figura tipo treemap. Si el DataFrame está vacío o le falta la columna 'alcaldia',
        se devuelve una figura vacía con mensaje informativo.
    """

    # Validación: si no hay datos o falta la columna requerida, devuelve treemap vacío
    if df.empty or "alcaldia" not in df.columns:
        return px.treemap(title="Sin datos para construir el treemap", template=TEMPLATE)

    # Agrupar: contar accidentes por alcaldía
    tmp = df["alcaldia"].dropna().value_counts().reset_index()
    # dropna(): elimina registros sin alcaldía
    # value_counts(): cuenta cuántas veces aparece cada alcaldía
    # reset_index(): convierte la Serie resultante en DataFrame

    tmp.columns = ["alcaldia", "accidentes"]
    # Renombrar columnas para claridad y compatibilidad con Plotly

    # Crear gráfico tipo treemap
    fig = px.treemap(
        tmp,
        path=["alcaldia"],               # jerarquía del treemap: una sola capa por alcaldía
        values="accidentes",             # tamaño de cada rectángulo proporcional al conteo
        title="📍 Treemap: Accidentes por alcaldía (sin filtro)",
        template=TEMPLATE,               # estilo visual global
        color="accidentes",              # color proporcional al número de accidentes
        color_continuous_scale=[         # escala de color personalizada (rojos degradados)
            "#ffffff", "#fcae91", "#fb6a4a", "#de2d26", "#a50f15"
        ]
    )

    return fig




def fig_tendencia_mensual_accidentes(df: pd.DataFrame):
    """
    Genera una línea de tendencia con la evolución mensual del número de accidentes.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame con una columna 'mes' (número del 1 al 12) ya preprocesada.

    Retorna
    -------
    plotly.graph_objs._figure.Figure
        Gráfico de línea con marcadores que muestra el total de accidentes por mes.
        Si el DataFrame está vacío o le falta la columna 'mes', se devuelve una figura vacía.
    """

    # Validación: si no hay datos o falta la columna 'mes', devolver figura vacía
    if df.empty or "mes" not in df.columns:
        return px.line(title="Sin datos para mostrar", template=TEMPLATE)

    # Importar catálogos desde el módulo theme
    from .theme import NUM_A_MESES, MESES

    # Agrupar: contar cuántos accidentes hay por cada mes (1 al 12)
    tmp = df["mes"].value_counts().sort_index().reset_index()
    # .value_counts(): cuenta ocurrencias por mes
    # .sort_index(): asegura orden cronológico de los meses (1→12)
    # .reset_index(): convierte a DataFrame

    tmp.columns = ["mes", "accidentes"]  # renombrar columnas
    tmp["mes_nombre"] = tmp["mes"].map(NUM_A_MESES)  # 1→"Enero", 2→"Febrero", etc.

    # Crear gráfico de línea
    fig = px.line(
        tmp,
        x="mes_nombre",           # eje X: nombres de meses
        y="accidentes",           # eje Y: conteo por mes
        title="📈 Tendencia mensual de accidentes (todos los datos)",
        labels={
            "mes_nombre": "Mes",
            "accidentes": "Número de accidentes"
        },
        markers=True,             # muestra marcadores en los puntos de la línea
        template=TEMPLATE         # estilo global del dashboard
    )

    # Ordena manualmente el eje X según el catálogo MESES (evita orden alfabético)
    fig.update_layout(xaxis=dict(categoryorder="array", categoryarray=MESES))

    return fig


def fig_fallecidos_por_alcaldia(df: pd.DataFrame):
    """
    Genera un gráfico de barras que muestra el total de personas fallecidas por alcaldía.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame con las columnas 'alcaldia' y 'personas_fallecidas'.

    Retorna
    -------
    plotly.graph_objs._figure.Figure
        Gráfico de barras ordenado de mayor a menor por cantidad de fallecidos.
        Devuelve una figura vacía si faltan columnas o el DataFrame está vacío.
    """

    # Validación: verificar que el DataFrame tenga las columnas necesarias y no esté vacío
    if df.empty or not {"alcaldia", "personas_fallecidas"}.issubset(df.columns):
        return px.bar(title="Sin datos para mostrar", template=TEMPLATE)

    # Agrupar y sumar fallecidos por alcaldía (solo donde ambas columnas tienen datos válidos)
    tmp = (
        df.dropna(subset=["alcaldia", "personas_fallecidas"])  # elimina registros incompletos
        .groupby("alcaldia")["personas_fallecidas"]            # agrupa por alcaldía
        .sum()                                                 # suma fallecidos por grupo
        .sort_values(ascending=False)                          # ordena de mayor a menor
        .reset_index()                                         # convierte índice en columna
    )

    # Crear gráfico de barras con etiquetas y color personalizado
    fig = px.bar(
        tmp,
        x="alcaldia",                          # eje X: alcaldías
        y="personas_fallecidas",               # eje Y: total de fallecidos
        title="☠️ Total de personas fallecidas por alcaldía",
        labels={
            "alcaldia": "Alcaldía",
            "personas_fallecidas": "Fallecidos"
        },
        template=TEMPLATE,
        color_discrete_sequence=[PALETA[0]],   # primer color de la paleta definida en theme.py
        text="personas_fallecidas"             # muestra número sobre cada barra
    )

    # Ajustes visuales del gráfico
    fig.update_traces(textposition="outside")  # texto fuera de las barras
    fig.update_layout(
        yaxis_title="Fallecidos",
        xaxis_title=""                         # eje X sin título extra
    )

    return fig





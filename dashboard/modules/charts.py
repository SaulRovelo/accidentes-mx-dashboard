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

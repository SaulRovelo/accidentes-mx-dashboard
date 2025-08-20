# dashboard/app.py

import math
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from modules.data import load_data
from modules.theme import DATOS_FUENTE_URL
from modules.charts import (
    fig_accidentes_por_mes, fig_mapa_incidentes, fig_accidentes_por_hora,
    fig_fallecidos_por_alcaldia, fig_treemap_accidentes_por_alcaldia,
    fig_heatmap_hora_dia, fig_prioridad_atencion, fig_fallecidos_donut,
    fig_bubble_lesionados_vs_fallecidos_total, fig_eventos_por_tipo,
    apply_base_layout,
)

# --- App ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard de Siniestros Viales CDMX — 2024"

# --- Data ---
df = load_data("data/accidentes_cdmx_limpio.csv")

# KPI totals
total_accidentes = len(df)
total_lesionados = int(df["personas_lesionadas"].fillna(0).sum())
total_fallecidos = int(df["personas_fallecidas"].fillna(0).sum())

# Opciones para filtro local del mapa
tipos_evento = sorted([t for t in df["tipo_evento"].dropna().unique()])
radio_options = [{"label": "Todos", "value": "Todos"}] + [{"label": t, "value": t} for t in tipos_evento]

# --- Header ---
header = html.Div([
    html.H1("Dashboard de Siniestros Viales en CDMX — 2024", className="text-center"),
    html.P([
        "Resumen interactivo de incidentes viales reportados en 2024. Fuente: ",
        html.A("Datos Abiertos CDMX", href=DATOS_FUENTE_URL, target="_blank", rel="noopener")
    ], className="text-center text-muted")
], className="my-4")

# --- KPIs ---
kpi_cards = dbc.Row([
    dbc.Col(dbc.Card(dbc.CardBody([html.H5("Total de accidentes"), html.H2(f"{total_accidentes:,}")]), className="card-kpi"), md=4),
    dbc.Col(dbc.Card(dbc.CardBody([html.H5("Personas lesionadas"), html.H2(f"{total_lesionados:,}")]), className="card-kpi"), md=4),
    dbc.Col(dbc.Card(dbc.CardBody([html.H5("Personas fallecidas"), html.H2(f"{total_fallecidos:,}")]), className="card-kpi"), md=4),
], className="mb-4")

# ------------- Config slider treemap (normal) -------------
MIN_ACC = 100
MAX_ACC = 4000

def _nice_number(x: float, round_to=True) -> float:
    """Devuelve 1, 2, 5 o 10 × 10^n para ‘redondear’ rangos."""
    if x <= 0:
        return 1.0
    exp = math.floor(math.log10(x))
    f = x / (10 ** exp)
    if round_to:
        if f < 1.5:
            nf = 1
        elif f < 3:
            nf = 2
        elif f < 7:
            nf = 5
        else:
            nf = 10
    else:
        if f <= 1:
            nf = 1
        elif f <= 2:
            nf = 2
        elif f <= 5:
            nf = 5
        else:
            nf = 10
    return nf * (10 ** exp)

def build_slider_marks(min_v: int, max_v: int, target_ticks: int = 6) -> dict:
    """Genera marcas proporcionales y legibles entre min_v y max_v (normal)."""
    span = max_v - min_v
    if span <= 0:
        return {min_v: f"{min_v:,}"}
    step = int(_nice_number(span / (target_ticks - 1), round_to=True))
    # Asegura un step mínimo razonable
    step = max(100, step)
    # Alinear desde el primer múltiplo >= min_v
    start = (math.ceil(min_v / step)) * step
    values = [min_v]
    v = start
    while v < max_v:
        values.append(v)
        v += step
    if values[-1] != max_v:
        values.append(max_v)
    # quita duplicados preservando orden
    seen = set()
    ordered = []
    for n in values:
        if n not in seen:
            ordered.append(n); seen.add(n)
    return {n: f"{n:,}" for n in ordered}

# --- Cards ---
card_treemap = dbc.Card([
    dbc.CardHeader(html.Div([
        html.H4("Accidentes por alcaldía"),
        html.Div("Comparativo del volumen por demarcación.", className="subtitle"),
        dcc.Slider(
            id="slider-min-accidentes",
            min=MIN_ACC,
            max=MAX_ACC,
            step=50,  # control fino
            value=MIN_ACC,
            marks=build_slider_marks(MIN_ACC, MAX_ACC, target_ticks=6),
            tooltip={"always_visible": False},
            className="mt-3"
        ),
        html.Div(id="slider-valor-visible", className="text-center text-muted small py-1")
    ])),
    dbc.CardBody([
        dcc.Graph(id="treemap-figure", className="plot-container"),
        # Conserva tu insight estático si gustas (ya NO se duplica el texto dinámico)
        # html.P("Las demarcaciones centrales concentran mayor número de eventos.", className="insight")
    ])
], className="card-plot")

card_mapa = dbc.Card([
    dbc.CardHeader(html.Div([
        html.H4("Mapa de incidentes"),
        html.Div("Localización geográfica de los siniestros.", className="subtitle"),
        dbc.RadioItems(
            id="filtro-tipo-mapa",
            options=radio_options,
            value="Todos",
            inline=True,
            className="mt-2"
        )
    ])),
    dbc.CardBody([
        dcc.Graph(id="mapa-figure", figure=fig_mapa_incidentes(df), className="plot-container"),
        html.P("Los corredores viales principales muestran alta densidad de puntos.", className="insight")
    ])
], className="card-plot")

card_prioridad = dbc.Card([
    dbc.CardHeader(html.Div([html.H4("Distribución de prioridad de atención"), html.Div("Proporción de reportes por nivel de prioridad.", className="subtitle")])),
    dbc.CardBody([html.Div(dcc.Graph(figure=fig_prioridad_atencion(df)), className="plot-container")])
], className="card-plot")

card_hora = dbc.Card([
    dbc.CardHeader(html.Div([html.H4("Accidentes por hora"), html.Div("Picos en horarios laborales y fines de semana.", className="subtitle")])),
    dbc.CardBody([html.Div(dcc.Graph(figure=fig_accidentes_por_hora(df)), className="plot-container")])
], className="card-plot")

card_heatmap = dbc.Card([
    dbc.CardHeader(html.Div([html.H4("Accidentes por hora y día"), html.Div("Mapa de calor por franja horaria y día de la semana.", className="subtitle")])),
    dbc.CardBody([html.Div(dcc.Graph(figure=fig_heatmap_hora_dia(df)), className="plot-container")])
], className="card-plot")

card_fallecidos_mes = dbc.Card([
    dbc.CardHeader(html.Div([html.H4("Fallecidos por mes"), html.Div("Distribución mensual de víctimas fatales.", className="subtitle")])),
    dbc.CardBody([html.Div(dcc.Graph(figure=fig_fallecidos_donut(df)), className="plot-container")])
], className="card-plot")

card_mes = dbc.Card([
    dbc.CardHeader(html.Div([html.H4("Accidentes por mes"), html.Div("Tendencia mensual de reportes en 2024.", className="subtitle")])),
    dbc.CardBody([html.Div(dcc.Graph(figure=fig_accidentes_por_mes(df)), className="plot-container")])
], className="card-plot")

card_fallecidos_alcaldia = dbc.Card([
    dbc.CardHeader(html.Div([html.H4("Fallecidos por alcaldía"), html.Div("Totales por demarcación.", className="subtitle")])),
    dbc.CardBody([html.Div(dcc.Graph(figure=fig_fallecidos_por_alcaldia(df)), className="plot-container")])
], className="card-plot")

card_les_vs_fall = dbc.Card([
    dbc.CardHeader(html.Div([html.H4("Lesionados vs fallecidos (total)"), html.Div("Relación acumulada en el año.", className="subtitle")])),
    dbc.CardBody([html.Div(dcc.Graph(figure=fig_bubble_lesionados_vs_fallecidos_total(df)), className="plot-container")])
], className="card-plot")

card_tipo_evento = dbc.Card([
    dbc.CardHeader(html.Div([html.H4("Distribución por tipo de evento"), html.Div("Volumen de reportes por categoría, paleta consistente con el mapa.", className="subtitle")])),
    dbc.CardBody([html.Div(dcc.Graph(figure=fig_eventos_por_tipo(df)), className="plot-container")])
], className="card-plot")

# --- Layout ---
app.layout = dbc.Container([
    header, kpi_cards, html.Hr(),
    dbc.Row([dbc.Col(card_treemap, md=6), dbc.Col(card_mapa, md=6)], className="mb-4"),
    dbc.Row([dbc.Col(card_prioridad, md=12)], className="mb-4"),
    dbc.Row([dbc.Col(card_hora, md=6), dbc.Col(card_heatmap, md=6)], className="mb-4"),
    dbc.Row([dbc.Col(card_fallecidos_mes, md=12)], className="mb-4"),
    dbc.Row([dbc.Col(card_mes, md=6), dbc.Col(card_fallecidos_alcaldia, md=6)], className="mb-4"),
    dbc.Row([dbc.Col(card_tipo_evento, md=12)], className="mb-4"),
    dbc.Row([dbc.Col(card_les_vs_fall, md=12)], className="mb-4"),
], fluid=True)

# --- Callbacks ---
@app.callback(
    Output("mapa-figure", "figure"),
    Input("filtro-tipo-mapa", "value")
)
def actualizar_mapa(tipo_sel):
    df_filtrado = df if tipo_sel == "Todos" else df[df["tipo_evento"] == tipo_sel]
    return fig_mapa_incidentes(df_filtrado)

@app.callback(
    Output("treemap-figure", "figure"),
    Input("slider-min-accidentes", "value")
)
def actualizar_treemap(min_acc):
    return fig_treemap_accidentes_por_alcaldia(df, min_acc=min_acc)


@app.callback(
    Output("slider-valor-visible", "children"),
    Input("slider-min-accidentes", "value")
)
def mostrar_valor_slider(min_acc):
    return f"Mostrando alcaldías con al menos {int(min_acc):,} accidentes."
    
# --- Main ---
if __name__ == "__main__":
    app.run(debug=True, port=8050)

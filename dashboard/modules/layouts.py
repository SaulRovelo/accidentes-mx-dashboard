# dashboard/modules/layouts.py

from dash import html, dcc
import dash_bootstrap_components as dbc

# Importación de funciones de gráficas desde charts.py
from .charts import (
    fig_accidentes_por_mes,
    fig_mapa_incidentes,
    fig_accidentes_por_hora,
    fig_fallecidos_por_alcaldia,
    fig_treemap_accidentes_por_alcaldia,
    fig_heatmap_hora_dia,
    fig_prioridad_atencion,
    fig_fallecidos_donut,
    fig_bubble_lesionados_vs_fallecidos_total,
    fig_eventos_por_tipo,
)

# Filtros visuales (slider y radio buttons)
from .filters.mapa_filters import get_radio_tipo_evento
from .filters.treemap_filters import slider_min_accidentes

# --- CARD: Mapa de incidentes ---
def card_mapa(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([
            html.H4("Mapa de incidentes"),
            html.Div("Localización geográfica de los siniestros.", className="subtitle"),
            get_radio_tipo_evento(df)
        ]), style={"backgroundColor": "#f8f9fa"}),
        dbc.CardBody([
            dcc.Graph(
                id="mapa-figure",
                figure=fig_mapa_incidentes(df),
                className="plot-container",
                config={"responsive": True},
                style={"width": "90%", "maxWidth": "700px", "height": "500px", "margin": "0 auto"}
            ),
        ])
    ], className="card-plot", style={"height": "700px"})

# --- CARD: Treemap de accidentes por alcaldía ---
# --- CARD: Treemap de accidentes por alcaldía ---
def card_treemap(df, min_acc, max_acc):
    return dbc.Card([
        dbc.CardHeader(html.Div([
            html.H4("Accidentes por alcaldía"),
            html.Div("Alcaldías con mayor número de reportes de accidentes.", className="subtitle"),
            slider_min_accidentes(min_acc, max_acc),
            html.Div(id="slider-valor-visible", className="text-center text-muted small py-1")
        ]), style={"backgroundColor": "#f8f9fa"}),
        dbc.CardBody([
            dcc.Graph(
                id="treemap-figure",
                figure=fig_treemap_accidentes_por_alcaldia(df, min_acc),
                className="plot-container",
                config={"responsive": False},             # 👈 evita re-cálculo de tamaño
                style={
                    "width": "90%",                       # 👈 igual que el mapa
                    "maxWidth": "700px",
                    "height": "520px",
                    "margin": "0 auto"
                }
            )
        ])
    ], className="card-plot", style={"height": "700px"})


# --- CARD: Distribución de prioridad de atención ---
# --- layouts.py (solo el Graph de card_prioridad para asegurar centrado) ---
def card_prioridad(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([
            html.H4("Distribución de prioridad de atención"),
            html.Div("Proporción de incidentes clasificados en prioridad Alta, Media y Baja.", className="subtitle")
        ]), style={"backgroundColor": "#f8f9fa"}),
        dbc.CardBody([
            dcc.Graph(
                id="prioridad-figure",
                figure=fig_prioridad_atencion(df),
                config={"responsive": True},
                style={
                    "width": "90%",
                    "maxWidth": "680px",   # da más respiro al label de 'Alta' fuera
                    "height": "460px",
                    "margin": "0 auto"     # centra el canvas del gráfico
                },
                className="plot-container"
            )
        ])
    ], className="mb-4")


# --- CARD: Accidentes por hora ---
def card_hora(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([
            html.H4("Accidentes por hora"),
            html.Div("Picos en horarios laborales y fines de semana.", className="subtitle")
        ]), style={"backgroundColor": "#f8f9fa"}),
        dbc.CardBody([
            dcc.Graph(
                figure=fig_accidentes_por_hora(df),
                className="plot-container",
                config={"displayModeBar": False, "responsive": True},
                style={"height": "430px"}
            )
        ])
    ], className="card-plot")



# --- CARD: Heatmap hora vs día ---
# layouts.py
def card_heatmap(df):
    marks_12h = {h: f"{12 if h % 12 == 0 else h % 12} {'AM' if h < 12 else 'PM'}"
                 for h in range(0, 24, 2)}
    return dbc.Card([
        dbc.CardHeader(html.Div([
            html.H4("Accidentes por hora y día"),
            html.Div("Mapa de calor por franja horaria y día de la semana.", className="subtitle"),
            dbc.Row([
                dbc.Col(dbc.RadioItems(
                    id="radio-dia-scope",
                    options=[
                        {"label": "Todos", "value": "todos"},
                        {"label": "Lunes–Viernes", "value": "laborales"},
                        {"label": "Fin de semana", "value": "fin"},
                    ],
                    value="todos", inline=True, className="radio-negro mt-2"
                ), width=12),
            ], className="g-2"),
            html.Div("Rango de horas", className="text-muted small mt-2"),
            dcc.RangeSlider(
                id="rng-horas", min=0, max=23, step=1, value=[0, 23],
                marks=marks_12h, tooltip={"always_visible": False},
                className="slider-negro mt-1"
            ),
        ]), style={"backgroundColor": "#f8f9fa"}),
        dbc.CardBody([
            dcc.Graph(
                id="heatmap-figure",
                figure=fig_heatmap_hora_dia(df),
                className="plot-container",
                config={"displayModeBar": False, "responsive": True},
                style={"height": "440px"}  # ~20px extra vs height del fig para evitar cortes
            )
        ])
    ], className="card-plot")



# --- CARD: Donut de fallecidos por mes ---
def card_fallecidos_mes(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([
            html.H4("Fallecidos por mes"),
            html.Div("Distribución mensual de víctimas fatales.", className="subtitle")
        ]), style={"backgroundColor": "#f8f9fa"}),
        dbc.CardBody([
            dcc.Graph(figure=fig_fallecidos_donut(df), className="plot-container")
        ])
    ], className="card-plot")

# --- CARD: Accidentes por mes ---
def card_mes(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([
            html.H4("Accidentes por mes"),
            html.Div("Tendencia mensual de reportes en 2024.", className="subtitle")
        ]), style={"backgroundColor": "#f8f9fa"}),
        dbc.CardBody([
            dcc.Graph(figure=fig_accidentes_por_mes(df), className="plot-container")
        ])
    ], className="card-plot")

# --- CARD: Fallecidos por alcaldía ---
def card_fallecidos_alcaldia(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([
            html.H4("Fallecidos por alcaldía"),
            html.Div("Totales por demarcación.", className="subtitle")
        ]), style={"backgroundColor": "#f8f9fa"}),
        dbc.CardBody([
            dcc.Graph(figure=fig_fallecidos_por_alcaldia(df), className="plot-container")
        ])
    ], className="card-plot")

# --- CARD: Lesionados vs fallecidos (donut) ---
def card_les_vs_fall(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([
            html.H4("Lesionados vs fallecidos (total)"),
            html.Div("Relación acumulada en el año.", className="subtitle")
        ]), style={"backgroundColor": "#f8f9fa"}),
        dbc.CardBody([
            dcc.Graph(figure=fig_bubble_lesionados_vs_fallecidos_total(df), className="plot-container")
        ])
    ], className="card-plot")

# --- CARD: Tipo de evento ---
def card_tipo_evento(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([
            html.H4("Distribución por tipo de evento"),
            html.Div("Volumen de reportes por categoría, paleta consistente con el mapa.", className="subtitle")
        ]), style={"backgroundColor": "#f8f9fa"}),
        dbc.CardBody([
            dcc.Graph(figure=fig_eventos_por_tipo(df), className="plot-container")
        ])
    ], className="card-plot")

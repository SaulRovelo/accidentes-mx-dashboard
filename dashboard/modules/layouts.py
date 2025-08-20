# dashboard/modules/layouts.py

from dash import html, dcc
import dash_bootstrap_components as dbc

from .charts import (
    fig_accidentes_por_mes, fig_mapa_incidentes, fig_accidentes_por_hora,
    fig_fallecidos_por_alcaldia, fig_treemap_accidentes_por_alcaldia,
    fig_heatmap_hora_dia, fig_prioridad_atencion, fig_fallecidos_donut,
    fig_bubble_lesionados_vs_fallecidos_total, fig_eventos_por_tipo,
)

from .filters.mapa_filters import get_radio_tipo_evento
from .filters.treemap_filters import slider_min_accidentes

def card_mapa(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([
            html.H4("Mapa de incidentes"),
            html.Div("Localización geográfica de los siniestros.", className="subtitle"),
            get_radio_tipo_evento(df)
        ])),
        dbc.CardBody([
            dcc.Graph(id="mapa-figure", figure=fig_mapa_incidentes(df), className="plot-container"),
            html.P("Los corredores viales principales muestran alta densidad de puntos.", className="insight")
        ])
    ], className="card-plot")

def card_treemap(df, min_acc, max_acc):
    return dbc.Card([
        dbc.CardHeader(html.Div([
            html.H4("Accidentes por alcaldía"),
            html.Div("Comparativo del volumen por demarcación.", className="subtitle"),
            slider_min_accidentes(min_acc, max_acc),
            html.Div(id="slider-valor-visible", className="text-center text-muted small py-1")
        ])),
        dbc.CardBody([
            dcc.Graph(id="treemap-figure", figure=fig_treemap_accidentes_por_alcaldia(df), className="plot-container")
        ])
    ], className="card-plot")

def card_prioridad(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([html.H4("Distribución de prioridad de atención"), html.Div("Proporción de reportes por nivel de prioridad.", className="subtitle")])),
        dbc.CardBody([dcc.Graph(figure=fig_prioridad_atencion(df), className="plot-container")])
    ], className="card-plot")

def card_hora(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([html.H4("Accidentes por hora"), html.Div("Picos en horarios laborales y fines de semana.", className="subtitle")])),
        dbc.CardBody([dcc.Graph(figure=fig_accidentes_por_hora(df), className="plot-container")])
    ], className="card-plot")

def card_heatmap(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([html.H4("Accidentes por hora y día"), html.Div("Mapa de calor por franja horaria y día de la semana.", className="subtitle")])),
        dbc.CardBody([dcc.Graph(figure=fig_heatmap_hora_dia(df), className="plot-container")])
    ], className="card-plot")

def card_fallecidos_mes(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([html.H4("Fallecidos por mes"), html.Div("Distribución mensual de víctimas fatales.", className="subtitle")])),
        dbc.CardBody([dcc.Graph(figure=fig_fallecidos_donut(df), className="plot-container")])
    ], className="card-plot")

def card_mes(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([html.H4("Accidentes por mes"), html.Div("Tendencia mensual de reportes en 2024.", className="subtitle")])),
        dbc.CardBody([dcc.Graph(figure=fig_accidentes_por_mes(df), className="plot-container")])
    ], className="card-plot")

def card_fallecidos_alcaldia(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([html.H4("Fallecidos por alcaldía"), html.Div("Totales por demarcación.", className="subtitle")])),
        dbc.CardBody([dcc.Graph(figure=fig_fallecidos_por_alcaldia(df), className="plot-container")])
    ], className="card-plot")

def card_les_vs_fall(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([html.H4("Lesionados vs fallecidos (total)"), html.Div("Relación acumulada en el año.", className="subtitle")])),
        dbc.CardBody([dcc.Graph(figure=fig_bubble_lesionados_vs_fallecidos_total(df), className="plot-container")])
    ], className="card-plot")

def card_tipo_evento(df):
    return dbc.Card([
        dbc.CardHeader(html.Div([html.H4("Distribución por tipo de evento"), html.Div("Volumen de reportes por categoría, paleta consistente con el mapa.", className="subtitle")])),
        dbc.CardBody([dcc.Graph(figure=fig_eventos_por_tipo(df), className="plot-container")])
    ], className="card-plot")

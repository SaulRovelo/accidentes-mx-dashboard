# dashboard/app.py

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from modules.data import load_data
from modules.theme import DATOS_FUENTE_URL
from modules.charts import fig_mapa_incidentes, fig_treemap_accidentes_por_alcaldia
from modules.layouts import (
    card_mapa, card_treemap, card_prioridad, card_hora, card_heatmap,
    card_fallecidos_mes, card_mes, card_fallecidos_alcaldia,
    card_les_vs_fall, card_tipo_evento
)

# --- Inicialización ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard de Siniestros Viales CDMX — 2024"

# --- Carga de datos ---
df = load_data("data/accidentes_cdmx_limpio.csv")
total_accidentes = len(df)
total_lesionados = int(df["personas_lesionadas"].fillna(0).sum())
total_fallecidos = int(df["personas_fallecidas"].fillna(0).sum())

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

# --- Layout principal ---
app.layout = dbc.Container([
    header, kpi_cards, html.Hr(),
    dbc.Row([dbc.Col(card_treemap(df, 100, 4000), md=6), dbc.Col(card_mapa(df), md=6)], className="mb-4"),
    dbc.Row([dbc.Col(card_prioridad(df), md=12)], className="mb-4"),
    dbc.Row([dbc.Col(card_hora(df), md=6), dbc.Col(card_heatmap(df), md=6)], className="mb-4"),
    dbc.Row([dbc.Col(card_fallecidos_mes(df), md=12)], className="mb-4"),
    dbc.Row([dbc.Col(card_mes(df), md=6), dbc.Col(card_fallecidos_alcaldia(df), md=6)], className="mb-4"),
    dbc.Row([dbc.Col(card_tipo_evento(df), md=12)], className="mb-4"),
    dbc.Row([dbc.Col(card_les_vs_fall(df), md=12)], className="mb-4"),
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
    df_filtrado = df.groupby("alcaldia").filter(lambda g: len(g) >= min_acc)
    return fig_treemap_accidentes_por_alcaldia(df_filtrado)

@app.callback(
    Output("slider-valor-visible", "children"),
    Input("slider-min-accidentes", "value")
)
def mostrar_valor_slider(min_acc):
    return f"Mostrando alcaldías con al menos {int(min_acc):,} accidentes."

# --- Main ---
if __name__ == "__main__":
    app.run(debug=True, port=8050)

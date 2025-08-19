# dashboard/app_dash.py
# Migración del dashboard de accidentes CDMX de Streamlit a Dash + Bootstrap

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from modules.data import load_data
from modules.charts import (
    fig_accidentes_por_mes,
    fig_mapa_incidentes,
    fig_accidentes_por_hora,
    fig_fallecidos_por_alcaldia,
    fig_treemap_accidentes_por_alcaldia,
    fig_heatmap_hora_dia,
    fig_prioridad_atencion,
    fig_fallecidos_donut,
    fig_bubble_lesionados_vs_fallecidos_total,
)

# 1) Inicializar app con Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "🚦 Dashboard de Accidentes CDMX"

# 2) Cargar datos
df = load_data("data/accidentes_cdmx_limpio.csv")

# 3) KPIs
total_accidentes = len(df)
total_lesionados = int(df["personas_lesionadas"].fillna(0).sum())
total_fallecidos = int(df["personas_fallecidas"].fillna(0).sum())

kpi_cards = dbc.Row([
    dbc.Col(dbc.Card(
        dbc.CardBody([
            html.H5("📍 Total Accidentes", className="card-title"),
            html.H2(f"{total_accidentes:,}", className="card-text")
        ]), className="shadow-sm"), md=4),
    dbc.Col(dbc.Card(
        dbc.CardBody([
            html.H5("🩹 Personas Lesionadas", className="card-title"),
            html.H2(f"{total_lesionados:,}", className="card-text")
        ]), className="shadow-sm"), md=4),
    dbc.Col(dbc.Card(
        dbc.CardBody([
            html.H5("⚰️ Personas Fallecidas", className="card-title"),
            html.H2(f"{total_fallecidos:,}", className="card-text")
        ]), className="shadow-sm"), md=4),
])

# 4) Layout principal
app.layout = dbc.Container([
    html.H1("🚦 Dashboard de Accidentes en CDMX", className="my-4 text-center"),

    # KPIs
    kpi_cards,
    html.Hr(),

    

    # 1️⃣ Treemap + Mapa (2 juntas)
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("🏙️ Treemap por alcaldía"),
            dbc.CardBody(dcc.Graph(figure=fig_treemap_accidentes_por_alcaldia(df)))
        ]), md=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("🗺️ Mapa de incidentes"),
            dbc.CardBody(dcc.Graph(figure=fig_mapa_incidentes(df)))
        ]), md=6),
    ], className="mb-4"),


     # Distribución de prioridad (sola)
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("🎯 Distribución de prioridad de atención"),
            dbc.CardBody(dcc.Graph(figure=fig_prioridad_atencion(df)))
        ]), md=12),
    ], className="mb-4"),

    # 2️⃣ Accidentes por hora + Heatmap (2 juntas)
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("⏰ Accidentes por hora"),
            dbc.CardBody(dcc.Graph(figure=fig_accidentes_por_hora(df)))
        ]), md=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("🔥 Heatmap hora × día"),
            dbc.CardBody(dcc.Graph(figure=fig_heatmap_hora_dia(df)))
        ]), md=6),
    ], className="mb-4"),

    # 3️⃣ Donut de fallecidos (sola)
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("☠️ Fallecidos por mes (donut)"),
            dbc.CardBody(dcc.Graph(figure=fig_fallecidos_donut(df)))
        ]), md=12),
    ], className="mb-4"),

    # 4️⃣ Accidentes por mes + Fallecidos por alcaldía (2 juntas)
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("📊 Accidentes por mes"),
            dbc.CardBody(dcc.Graph(figure=fig_accidentes_por_mes(df)))
        ]), md=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("☠️ Fallecidos por alcaldía"),
            dbc.CardBody(dcc.Graph(figure=fig_fallecidos_por_alcaldia(df)))
        ]), md=6),
    ], className="mb-4"),


dbc.Row([
    dbc.Col(dbc.Card([
        dbc.CardHeader("⚖️ Lesionados vs Fallecidos (donut)"),
        dbc.CardBody(dcc.Graph(figure=fig_bubble_lesionados_vs_fallecidos_total(df)))
    ]), md=12),
], className="mb-4"),



], fluid=True)


# 5) Arranque


if __name__ == "__main__":
    app.run(debug=True, port=8050)


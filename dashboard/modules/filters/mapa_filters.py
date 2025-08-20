# dashboard/modules/filters/mapa_filters.py
from dash import dcc
import dash_bootstrap_components as dbc

def get_radio_tipo_evento(df):
    tipos_evento = sorted(df["tipo_evento"].dropna().unique())
    opciones = [{"label": "Todos", "value": "Todos"}] + [{"label": t, "value": t} for t in tipos_evento]

    return dbc.RadioItems(
        id="filtro-tipo-mapa",
        options=opciones,
        value="Todos",
        inline=True,
        className="mt-2"
    )

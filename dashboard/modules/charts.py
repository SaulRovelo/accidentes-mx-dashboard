# modules/charts.py

import pandas as pd
import plotly.express as px
from .theme import (
    PALETA, TEMPLATE, DIAS_SEMANA, MESES, NUM_A_MESES, MAPBOX_STYLE, FONT_FAMILY
)

# ---------- Helper de layout consistente ----------
def apply_base_layout(fig, title, subtitle=None, height=420, margins=(24,20,64,28)):
    fig.update_layout(
        template=TEMPLATE,  # plotly_white
        title=dict(text=title, x=0.0, xanchor="left"),
        height=height,
        margin=dict(l=margins[0], r=margins[1], t=margins[2], b=margins[3]),
        font=dict(family=FONT_FAMILY, size=14, color="#111827"),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        # 👇 Sin rejilla (no “cuadriculado”), solo líneas de eje discretas
        xaxis=dict(
            showgrid=False,
            showline=True, linecolor="#cbd5e1", linewidth=1,
            ticks="outside", tickcolor="#cbd5e1", ticklen=5
        ),
        yaxis=dict(
            showgrid=False,  # si prefieres horizontales muy sutiles: True con gridcolor="#f1f5f9"
            zeroline=False,
            showline=True, linecolor="#cbd5e1", linewidth=1,
            ticks="outside", tickcolor="#cbd5e1", ticklen=5
        ),
        bargap=0.18
    )
    if subtitle:
        fig.add_annotation(
            text=f"<span style='color:#64748b'>{subtitle}</span>",
            xref="paper", yref="paper", x=0.0, y=1.12, showarrow=False, align="left"
        )
    return fig




# ---------- Accidentes por mes ----------
def fig_accidentes_por_mes(df: pd.DataFrame):
    if df.empty or "mes" not in df.columns:
        return px.bar(title="Sin datos para el rango seleccionado", template=TEMPLATE)

    tmp = df.groupby("mes").size().reset_index(name="accidentes")
    tmp["mes_nombre"] = tmp["mes"].map(NUM_A_MESES)

    fig = px.bar(
        tmp, x="mes_nombre", y="accidentes",
        category_orders={"mes_nombre": MESES},
        labels={"mes_nombre": "Mes", "accidentes": "Accidentes"},
        color_discrete_sequence=[PALETA[0]],
        template=TEMPLATE,
        text="accidentes"
    )
    fig.update_traces(textposition="outside")
    return apply_base_layout(
        fig,
        title="Accidentes por mes",
        subtitle="Tendencia mensual de siniestros viales (CDMX, 2024).",
        height=430, margins=(30,20,64,30)
    )


# ---------- Mapa de incidentes (usa paleta para tipo_evento) ----------
# dashboard/modules/charts.py
from typing import Optional
import pandas as pd

def fig_mapa_incidentes(df: pd.DataFrame):
    import plotly.express as px
    import plotly.graph_objects as go

    # Validaciones básicas
    if df.empty or not {"latitud", "longitud"}.issubset(df.columns):
        return None
    m = df.dropna(subset=["latitud", "longitud"])
    if m.empty:
        return None

    # 🎨 Colores fijos por categoría (leyenda estática)
    COLOR_EVENTOS = {
        "atropellado": "#f4a261",
        "choque": "#04c1ab",
        "derrapado": "#f3cd6e",
        "caida de pasajero": "#C69BE2",
        "volcadura": "#b5838d",
        "caida de ciclista": "#8ecae6",
    }
    orden_tipos = list(COLOR_EVENTOS.keys())
    FIG_H = 480  # Altura fija; el ancho lo determina el contenedor (dcc.Graph style={"width":"100%"})

    # Figura base: siempre color por tipo_evento
    fig = px.scatter_mapbox(
        m,
        lat="latitud",
        lon="longitud",
        hover_name="tipo_evento",
        hover_data=["alcaldia", "fecha_evento", "personas_lesionadas", "personas_fallecidas"],
        color="tipo_evento",
        color_discrete_map=COLOR_EVENTOS,
        category_orders={"tipo_evento": orden_tipos},
        height=FIG_H,
        zoom=9.3,  # 👈 Deja el zoom tal cual
        center=dict(lat=19.350, lon=-99.145),  # 👈 Centro CDMX
    )

    # Trazas fantasma para que la leyenda muestre TODAS las categorías
    presentes = set(m["tipo_evento"].dropna().unique())
    for t in (t for t in orden_tipos if t not in presentes):
        fig.add_trace(go.Scattermapbox(
            lat=[None], lon=[None],
            mode="markers",
            marker=dict(color=COLOR_EVENTOS[t], size=8),
            name=t,
            hoverinfo="skip",
            showlegend=True
        ))

    # Layout: leyenda compacta y esquina superior derecha; sin width (responsivo por contenedor)
    fig.update_layout(
        autosize=True,          # el ancho lo controla la tarjeta
        height=FIG_H,
        uirevision="mapa_cdmx", # congela la vista entre callbacks
        margin=dict(l=0, r=0, t=0, b=0),
        mapbox=dict(
            style="carto-positron",
            zoom=9.3,
            center=dict(lat=19.350, lon=-99.145),
        ),
        showlegend=True,
        legend=dict(
            title=None,                                # leyenda más pequeña
            x=0.985, y=0.99, xanchor="right", yanchor="top",
            bgcolor="rgba(255,255,255,0.90)",
            bordercolor="rgba(0,0,0,0.15)", borderwidth=1,
            font=dict(size=11),                        # 👈 más compacta
            itemsizing="trace",  # 👈 Usa el tamaño de los trazos (más pequeño)
           
        ),
    )

    return fig



# ---------- Distribución por tipo de evento (nueva) ----------
def fig_eventos_por_tipo(df: pd.DataFrame):
    if df.empty or "tipo_evento" not in df.columns:
        return px.bar(title="Sin datos para mostrar", template=TEMPLATE)

    tmp = df["tipo_evento"].value_counts().reset_index()
    tmp.columns = ["tipo_evento", "accidentes"]

    fig = px.bar(
        tmp, x="tipo_evento", y="accidentes",
        color="tipo_evento",               # usa paleta cualitativa completa
        color_discrete_sequence=PALETA,
        labels={"tipo_evento": "Tipo de evento", "accidentes": "Accidentes"},
        template=TEMPLATE,
        text="accidentes"
    )
    fig.update_traces(textposition="outside")
    fig.update_xaxes(tickangle=0, automargin=True)
    return apply_base_layout(
        fig,
        title="Distribución por tipo de evento",
        subtitle="Volumen de reportes por categoría; colores consistentes con el mapa.",
        height=430, margins=(28,20,64,36)
    )


# ---------- Accidentes por hora ----------
def _ticks_12h():
    """0..23  ->  ['12 AM','1 AM',...,'11 PM']"""
    etiquetas = []
    for h in range(24):
        h12 = 12 if h % 12 == 0 else h % 12
        suf = "AM" if h < 12 else "PM"
        etiquetas.append(f"{h12} {suf}")
    return list(range(24)), etiquetas

def fig_accidentes_por_hora(df: pd.DataFrame):
    if df.empty or "hora" not in df.columns:
        return px.bar(title="Sin datos para mostrar", template=TEMPLATE)

    # Conteo por hora 0..23
    tmp = (
        df["hora"].astype(int)
          .value_counts()
          .reindex(range(24), fill_value=0)
          .reset_index()
    )
    tmp.columns = ["hora", "accidentes"]

    # Top 3 horas
    top3 = tmp.nlargest(3, "accidentes").reset_index(drop=True)

    # Gráfico base (color sobrio)
    base_color = "#a1e4f1"
    fig = px.bar(
        tmp, x="hora", y="accidentes",
        labels={"hora": "Hora", "accidentes": "Accidentes"},
        color_discrete_sequence=[base_color],
        template=TEMPLATE,
        text=None  # más limpio; el dato aparece en el hover
    )

    # Recolorear por-barra solo las 3 horas top
    top_colors = ["#0003b6", "#265bd6", "#6fb2fe"]  # Top1, Top2, Top3
    color_by_bar = [base_color] * len(tmp)

    # Mapa Hora -> etiqueta '12 AM'..'11 PM' para ticks y hover
    tickvals, ticktext = _ticks_12h()
    label_by_hour = {h: t for h, t in zip(tickvals, ticktext)}
    # Customdata con la etiqueta AM/PM
    custom_labels = tmp["hora"].map(label_by_hour)

    # Asignar color y anotaciones
    for rank in range(3):
        h = int(top3.loc[rank, "hora"])
        v = int(top3.loc[rank, "accidentes"])
        idx = tmp.index[tmp["hora"] == h][0]
        color_by_bar[idx] = top_colors[rank]
        fig.add_annotation(
            x=h, y=v,
            text=f"{rank+1}",
            showarrow=False, yshift=14,
            font=dict(color="#000000", size=15)
        )
        

    fig.update_traces(
        marker_color=color_by_bar,
        customdata=custom_labels,
        hovertemplate="Hora %{customdata}<br>Accidentes: %{y:,}<extra></extra>"
    )

    # Eje X en 12 h y layout limpio
    fig.update_layout(
        xaxis=dict(tickmode="array", tickvals=tickvals, ticktext=ticktext, dtick=1),
        yaxis=dict(rangemode="tozero", title="Accidentes"),
        bargap=0.18,
        showlegend=False
    )

    # Si usas tu helper de layout global:
    return apply_base_layout(
        fig,
        title=" ",
        #subtitle="Top 3 horas resaltadas (formato 12 h).",
        height=430, margins=(30, 20, 64, 30)
    )

# ---------- Heatmap hora × día ----------
def fig_heatmap_hora_dia(
    df: pd.DataFrame,
    horas: tuple[int, int] = (0, 23),   # (inicio, fin) en 0..23
    dia_scope: str = "todos"            # "todos" | "laborales" | "fin"
):
    import numpy as np
    import plotly.express as px

    if df.empty or not {"hora", "dia_semana_nombre"}.issubset(df.columns):
        return px.imshow([[0]*24]*7, x=list(range(24)), y=DIAS_SEMANA,
                         title="Sin datos para construir el heatmap", template=TEMPLATE)

    # --- Normaliza filtros ---
    h_ini, h_fin = map(int, horas)
    if h_ini > h_fin:
        h_ini, h_fin = h_fin, h_ini
    h_ini = max(0, min(23, h_ini))
    h_fin = max(0, min(23, h_fin))

    scope = {
        "todos": DIAS_SEMANA,
        "laborales": DIAS_SEMANA[:5],  # Lunes–Viernes
        "fin": DIAS_SEMANA[5:]         # Sábado–Domingo
    }
    dias_sel = scope.get(dia_scope, DIAS_SEMANA)

    # --- Tabla 7×(horas) ---
    df2 = df.copy()
    df2["hora"] = df2["hora"].astype("Int64").clip(0, 23)
    df2 = df2[df2["hora"].between(h_ini, h_fin) & df2["dia_semana_nombre"].isin(dias_sel)]
    tabla = (
        df2.pivot_table(index="dia_semana_nombre", columns="hora",
                        values="tipo_evento", aggfunc="count", fill_value=0)
           .reindex(index=dias_sel, columns=list(range(h_ini, h_fin + 1)), fill_value=0)
    )

   
    azul_suave = [
    "#FBFDB0", "#FEC287", "#FB8761", "#E55964",
    "#B5367A", "#8C2981", "#59106E", "#1F0A3A", "#000004"
]
    fig = px.imshow(
        tabla.values,
        x=tabla.columns,      # horas seleccionadas
        y=tabla.index,        # días seleccionados
        #labels=dict(x="Hora del día", y="Día de la semana", color="Accidentes"),
        template=TEMPLATE,
        color_continuous_scale=azul_suave,
        aspect="auto"         # evita formato cuadrado (se adapta al ancho del contenedor)
    )

    # Separación sutil entre celdas
    fig.update_traces(xgap=1.0, ygap=2.0)

    # --- Eje X en 12 h y hover claro ---
    def _fmt12(h): return f"{12 if h % 12 == 0 else h % 12} {'AM' if h < 12 else 'PM'}"
    tickvals = list(tabla.columns)
    ticktext = [_fmt12(h) for h in tickvals]
    fig.update_traces(
        customdata=np.tile(np.array(ticktext), (len(tabla.index), 1)),
        hovertemplate="Día: %{y}<br>Hora: %{customdata}<br>Accidentes: %{z}<extra></extra>"
    )
    fig.update_xaxes(tickmode="array", tickvals=tickvals, ticktext=ticktext, ticks="outside")
    fig.update_yaxes(ticks="outside")

    # --- Colorbar vertical y figura compacta ---
    fig.update_layout(
        height=420,  # más compacto
        margin=dict(l=28, r=70, t=10, b=28),   # margen derecho para colorbar
        coloraxis_colorbar=dict(
            title="Accidentes",
            orientation="v",   # vertical a la derecha
            x=1.02, xanchor="left",
            y=0.5, yanchor="middle",
            len=0.80,          # tamaño proporcional
            thickness=12,      # delgado
            outlinecolor="rgba(0,0,0,0.15)", outlinewidth=1
        ),
        font=dict(family=FONT_FAMILY, size=14, color="#111827"),
        showlegend=False
    )
    return fig


# ---------- Treemap por alcaldía ----------
def fig_treemap_accidentes_por_alcaldia(df: pd.DataFrame, min_acc: int = 0):
    import plotly.express as px

    if df.empty or "alcaldia" not in df.columns:
        return px.treemap(title="Sin datos para construir el treemap", template="plotly_white")

    # Agrupación y filtrado
    tmp = df["alcaldia"].dropna().value_counts().reset_index()
    tmp.columns = ["alcaldia", "accidentes"]

    max_total = tmp["accidentes"].max()
    tmp = tmp[tmp["accidentes"] >= min_acc]

    if tmp.empty:
        fig = px.treemap(title="Sin datos para el umbral seleccionado", template="plotly_white")
        fig.update_layout(title=None)
        return apply_base_layout(fig, title="", subtitle=None, height=520, margins=(20, 0, 20, 20))

    # Escala fija para que el color sea consistente
    fig = px.treemap(
        tmp,
        path=["alcaldia"],
        values="accidentes",
        color="accidentes",
        color_continuous_scale=["#f6db85", "#f7c585", "#f3a784", "#d96457", "#b80000"],
        range_color=[0, max_total],  # <- fija el rango de color
        template="plotly_white"
    )

    fig.update_traces(
        textinfo="label+value",
        marker=dict(cornerradius=5),
        hovertemplate="<b>%{label}</b><br>Accidentes: %{value}<extra></extra>"
    )

    fig.update_layout(
    title=None,
    paper_bgcolor="white",
    plot_bgcolor="white",
    #margin=dict(t=0, l=0, r=0, b=0),
    coloraxis_colorbar=dict(
        title="Accidentes",
        tickmode="array",
        tickvals=[0, 1000, 2000, 3000, 4000],
        ticktext=["0", "1,000", "2,000", "3,000", "4,000"],
        ticks="outside",
        tickcolor="black",
        ticklen=8,
        tickfont=dict(size=12, color="black"),
        showticklabels=True,
        len=0.8,
        thickness=18,
        y=0.5,
        yanchor="middle"
    )


)

    return apply_base_layout(
        fig,
        title="",
        subtitle=None,
        height=505,
        margins=(20, 0, 20, 20)
    )



# ---------- Barras: fallecidos por alcaldía ----------
def fig_fallecidos_por_alcaldia(df: pd.DataFrame):
    if df.empty or not {"alcaldia", "personas_fallecidas"}.issubset(df.columns):
        return px.bar(title="Sin datos para mostrar", template=TEMPLATE)

    tmp = (
        df.dropna(subset=["alcaldia", "personas_fallecidas"])
          .groupby("alcaldia")["personas_fallecidas"].sum()
          .sort_values(ascending=False).reset_index()
    )
    fig = px.bar(
        tmp, x="alcaldia", y="personas_fallecidas",
        labels={"alcaldia": "Alcaldía", "personas_fallecidas": "Fallecidos"},
        color_discrete_sequence=[PALETA[2]],
        template=TEMPLATE,
        text="personas_fallecidas"
    )
    fig.update_traces(textposition="outside")
    return apply_base_layout(
        fig,
        title="Fallecidos por alcaldía",
        subtitle="Total registrado por demarcación durante 2024.",
        height=430, margins=(30,20,64,30)
    )


# ---------- Pie: prioridad de atención (usa paleta cualitativa) ----------
def fig_prioridad_atencion(df: pd.DataFrame):
    if df.empty or "prioridad" not in df.columns:
        return px.pie(title="Sin datos para mostrar", template=TEMPLATE)

    df = df.copy()
    df["prioridad"] = df["prioridad"].str.capitalize()

    tmp = df["prioridad"].value_counts().reset_index()
    tmp.columns = ["prioridad", "casos"]

    colores_prioridad = {
        "Alta": "#e63946",   # rojo
        "Media": "#ffb703",  # ámbar vivo
        "Baja": "#219ebc"    # azul sobrio
    }

    fig = px.pie(
        tmp,
        names="prioridad",
        values="casos",
        hole=0.42,
        template=TEMPLATE,
        color="prioridad",
        color_discrete_map=colores_prioridad
    )

    # 🔑 Todas las etiquetas afuera
    fig.update_traces(
        textinfo="label+percent",
        texttemplate="<b>%{label}</b><br>%{percent} — %{value:,} casos",
        textposition="outside",
        marker=dict(line=dict(color="white", width=2)),
        pull=[0.08 if p == "Alta" else 0 for p in tmp["prioridad"]],
        outsidetextfont=dict(size=15, family="Segoe UI, Arial, sans-serif", color="#2b2b2b"),
        hovertemplate="<b>%{label}</b><br>Casos: %{value:,}<br>Porcentaje: %{percent}<extra></extra>"
    )

    # 🔑 Leyenda desactivada (innecesaria con etiquetas afuera)
    fig.update_layout(showlegend=False)

    return apply_base_layout(
        fig,
        title="Distribución de prioridad de atención",
        #subtitle="Proporción de incidentes clasificados en prioridad Alta, Media y Baja.",
        height=480,
        margins=(24, 24, 64, 24)
    )



# ---------- Donut: fallecidos por mes ----------
def fig_fallecidos_donut(df: pd.DataFrame):
    if df.empty or "mes" not in df.columns or "personas_fallecidas" not in df.columns:
        return px.pie(title="Sin datos para mostrar", template=TEMPLATE)

    tmp = df.groupby("mes")["personas_fallecidas"].sum().reset_index()
    tmp["mes_nombre"] = tmp["mes"].map(NUM_A_MESES)

    fig = px.pie(
        tmp, names="mes_nombre", values="personas_fallecidas",
        hole=0.45, template=TEMPLATE,
        color="mes_nombre",
        color_discrete_sequence=PALETA
    )
    fig.update_traces(textinfo="label+percent")
    return apply_base_layout(
        fig,
        title="Fallecidos por mes",
        subtitle="Distribución mensual de víctimas fatales durante 2024.",
        height=420, margins=(20,20,64,20)
    )


# ---------- Donut: lesionados vs fallecidos (total) ----------
def fig_bubble_lesionados_vs_fallecidos_total(df: pd.DataFrame):
    if df.empty:
        return px.pie(title="Sin datos para mostrar", template=TEMPLATE)

    valores = {
        "Lesionados": int(df["personas_lesionadas"].fillna(0).sum()),
        "Fallecidos": int(df["personas_fallecidas"].fillna(0).sum())
    }
    tmp = pd.DataFrame(list(valores.items()), columns=["categoria", "total"])

    fig = px.pie(
        tmp, names="categoria", values="total",
        hole=0.5, template=TEMPLATE,
        color="categoria",
        color_discrete_sequence=[PALETA[0], PALETA[1]]
    )
    fig.update_traces(textinfo="label+percent", pull=[0, 0.05])
    return apply_base_layout(
        fig,
        title="Lesionados vs fallecidos (total)",
        subtitle="Relación acumulada de personas lesionadas y fallecidas en 2024.",
        height=420, margins=(20,20,64,20)
    )

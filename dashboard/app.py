#aplicacion web 

import streamlit as st 
import pandas as pd
from modules.data import load_data, filter_data
from modules.filters import sidebar_global_filters
from modules.charts import fig_accidentes_por_mes, fig_mapa_incidentes

def main():

    # 1) Carga de datos
    df = load_data("data/accidentes_cdmx_limpio.csv")
    # load_data: Lee el CSV, parsea 'fecha_evento' a datetime y agrega columna 'mes' (1..12)

    # 2) Panel GLOBAL: solo filtro de alcaldías
    gsel = sidebar_global_filters(df)
    # sidebar_global_filters: Renderiza checkboxes en la sidebar para elegir alcaldías

    df_global = df[df["alcaldia"].isin(gsel["alcaldias_sel"])]
    # df_global: subconjunto del DataFrame según selección global de alcaldías

    # si no hay datos tras el filtro global, mostramos aviso y salimos
    if df_global.empty:
        st.title("🚦 Dashboard de Accidentes CDMX")
        st.info("No hay datos con la selección de alcaldías actual. Ajusta el filtro global para continuar.")
        return

    # 3) Encabezado y KPIs
    st.title("🚦 Dashboard de Accidentes CDMX")

    # KPIs usando el df filtrado globalmente por alcaldías
    col1, col2, col3 = st.columns(3)
    col1.metric("📍 Total de Accidentes", len(df_global))
    # len(): cuenta filas → número total de registros (accidentes) en df_global

    col2.metric("🩹 Personas Lesionadas", int(df_global["personas_lesionadas"].fillna(0).sum()))
    # fillna(0).sum(): suma robusta de lesionados (evita NaN)

    col3.metric("⚰️ Personas Fallecidas", int(df_global["personas_fallecidas"].fillna(0).sum()))
    # fillna(0).sum(): suma robusta de fallecidos (evita NaN)

    st.divider()

    # ===================== Tarjeta 1: Barras por mes =====================
    st.subheader("📊 Accidentes por mes")

    # Slider de meses debajo del gráfico (filtro LOCAL para esta tarjeta)
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    # meses: catálogo ordenado para mostrar nombres correctos (Enero→Diciembre)

    m_ini, m_fin = st.select_slider(
        " ",  # etiqueta vacía para no duplicar títulos
        options=meses,
        value=("Enero", "Diciembre"),
        key="meses_chart1"  # key: mantiene el estado del slider en esta tarjeta
    )

    # Mapear nombres a números y aplicar filtro local (rango de meses)
    meses_numeros = {m: i+1 for i, m in enumerate(meses)}  # {"Enero":1, ..., "Diciembre":12}
    m_ini_n, m_fin_n = meses_numeros[m_ini], meses_numeros[m_fin]
    df_c1 = df_global[df_global["mes"].between(m_ini_n, m_fin_n)]
    # df_c1: subconjunto para la gráfica de barras por mes (filtrado local)

    # Mostrar la gráfica de barras (usa función del módulo charts)
    st.plotly_chart(fig_accidentes_por_mes(df_c1), use_container_width=True)

    st.divider()

    # ===================== Tarjeta 2: Mapa con tipo_evento =====================
    st.subheader("🗺️ Mapa de incidentes")

    # Bloque de filtros LOCALes (tipo_evento) para esta tarjeta
    tipos = sorted(df_global["tipo_evento"].dropna().unique())
    seleccionar_todos = st.checkbox("Seleccionar todos", value=True, key="sel_todos_chart2")
    # seleccionar_todos: si está activo, incluimos todos los tipos; si no, permitimos granularidad

    cols = st.columns(4)  # Distribuye checkboxes en 4 columnas para mejor legibilidad
    tipos_sel = []

    for i, tipo in enumerate(tipos):
        # Si "Seleccionar todos" está activo, no mostramos checkboxes individuales
        # (o los ignoramos). Si no, activamos checkboxes por tipo.
        if seleccionar_todos or cols[i % 4].checkbox(tipo, value=False, key=f"check_{tipo}"):
            tipos_sel.append(tipo)

    # Filtrado local por tipo_evento para el mapa
    df_c2 = df_global[df_global["tipo_evento"].isin(tipos_sel)]

    # Crear figura de mapa con scatter_mapbox (módulo charts)
    fig_map = fig_mapa_incidentes(df_c2)
    if fig_map is not None:
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No hay datos de coordenadas para los filtros actuales.")


    from modules.charts import fig_accidentes_por_hora

# ===================== Tarjeta 4: Distribución por hora del día =====================
    st.subheader("⏰ Distribución de accidentes por hora del día")

    # Sin filtro local → usamos el df_global completo
    df_c4 = df_global.copy()

    # Mostrar gráfico
    st.plotly_chart(fig_accidentes_por_hora(df_c4), use_container_width=True)
    st.divider()




if __name__ == "__main__":
    main()
 
# dashboard/app.py
# ------------------------------------------------------------------------------------
# App principal de Streamlit para el Dashboard de Accidentes CDMX
# Estructura general:
#   1) Carga de datos (desde modules.data)
#   2) Filtros (sidebar) y selección del usuario (desde modules.filters)
#   3) Filtrado centralizado del DataFrame (desde modules.data.filter_data)
#   4) Encabezado + KPIs (métricas principales)
#   5) Gráfico principal (accidentes por mes) - modules.charts.fig_accidentes_por_mes
#   6) Mapa de incidentes por coordenadas - modules.charts.fig_mapa_incidentes
# ------------------------------------------------------------------------------------

import streamlit as st
from modules.data import load_data, filter_data
from modules.filters import sidebar_filters
from modules.charts import (
    fig_accidentes_por_mes, 
    fig_mapa_incidentes
)

def main():
    # 1) Carga de datos ---------------------------------------------------------
    # load_data: función utilitaria que lee el CSV "limpio" y aplica los tipos necesarios
    df = load_data("data/accidentes_cdmx_limpio.csv")

    # 2) Filtros (sidebar) ------------------------------------------------------
    # sidebar_filters: construye los controles en la barra lateral y devuelve
    # un diccionario con las selecciones del usuario (alcaldías, rango de meses, tipos de evento, etc.)
    sel = sidebar_filters(df)

    # 3) Filtrado centralizado (incluye tipo_evento) ---------------------------
    # filter_data: aplica de forma consistente todos los criterios de filtrado.
    # Ventaja: mantenemos la lógica en un solo lugar, lo que reduce duplicación y errores.
    df_filtrado = filter_data(
        df,
        sel["alcaldias_sel"],    # lista de alcaldías seleccionadas
        sel["mes_inicio_num"],   # mes de inicio (numérico, 1-12)
        sel["mes_fin_num"],      # mes de fin (numérico, 1-12)
        sel["tipos_evento_sel"], # lista de tipos de evento seleccionados
    )

    # 4) Encabezado y KPIs ------------------------------------------------------
    st.title("🚦 Dashboard de Accidentes CDMX")
    st.subheader("📌 Indicadores principales")

    # st.columns: creamos 3 columnas para mostrar métricas clave
    col1, col2, col3 = st.columns(3)

    # len(df_filtrado): número de registros tras filtros → total de accidentes
    col1.metric("📍 Total de Accidentes", len(df_filtrado))

    # sum() sobre columnas numéricas; int() para asegurar un entero visible
    col2.metric("🩹 Personas Lesionadas", int(df_filtrado["personas_lesionadas"].sum()))
    col3.metric("⚰️ Personas Fallecidas", int(df_filtrado["personas_fallecidas"].sum()))

    # Línea divisoria para separar secciones visualmente
    st.divider()

    # 5) Gráfico principal: accidentes por mes ---------------------------------
    st.subheader("📊 Distribución mensual de accidentes")
    # fig_accidentes_por_mes: devuelve una figura Plotly ya configurada
    st.plotly_chart(fig_accidentes_por_mes(df_filtrado), use_container_width=True)

    # 6) Mapa de incidentes -------------------------------
    st.subheader("🗺️ Mapa de Accidentes por Coordenadas")
    # fig_mapa_incidentes: puede devolver None si no hay lat/lon válidas
    fig_map = fig_mapa_incidentes(df_filtrado)
    if fig_map is not None:
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        # Mensaje informativo cuando los filtros dejan sin datos georreferenciados
        st.info("No hay datos de coordenadas para los filtros actuales.")

# Punto de entrada estándar de Python. Streamlit ejecuta main() al levantar la app.
if __name__ == "__main__":
    main()

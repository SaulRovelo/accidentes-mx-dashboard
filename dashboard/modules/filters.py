# Módulo de filtros para la barra lateral del dashboard

import streamlit as st  # Framework para crear la app web interactiva
import pandas as pd     # Librería para manipulación/análisis de datos

def sidebar_global_filters(df: pd.DataFrame) -> dict:
    """Panel GLOBAL: sólo controla selección de alcaldías."""
    # df: DataFrame con columna 'alcaldia' usada para poblar la lista de opciones
    # return: dict con la clave 'alcaldias_sel' (lista de alcaldías seleccionadas)

    with st.sidebar.expander("🔎 Filtros globales", expanded=True):
        # st.sidebar.expander: Crea un panel plegable en la barra lateral
        # expanded=True: El panel se muestra abierto por defecto

        st.markdown("### 🏙️ Alcaldías")  # Título de sección en el panel
        alcaldias = sorted(df["alcaldia"].dropna().unique().tolist())
        # dropna(): Elimina valores nulos de la columna 'alcaldia'
        # unique(): Obtiene el conjunto de alcaldías sin repetir
        # sorted(...): Ordena alfabéticamente para facilitar la búsqueda visual
        # tolist(): Convierte a lista de Python

        seleccionar_todas = st.checkbox("Seleccionar todas", value=True, key="all_munis")
        # st.checkbox: Casilla para seleccionar/deseleccionar todas las alcaldías
        # value=True: Activada por defecto para incluir todo al inicio
        # key="all_munis": Clave única del widget para mantener estado

        if seleccionar_todas:
            alcaldias_sel = alcaldias
            # Si está marcada la casilla, usamos la lista completa
        else:
            cols = st.columns(2)
            # st.columns(2): Distribuye las opciones en dos columnas (mejor lectura)
            alcaldias_sel = []
            for i, a in enumerate(alcaldias):
                # enumerate: Recorre la lista y nos da índice (i) y valor (a)
                if cols[i % 2].checkbox(a, value=False, key=f"muni_{a}"):
                    # Alternamos entre col 0 y col 1 usando módulo (%)
                    # Creamos un checkbox por alcaldía (value=False: desmarcadas por defecto)
                    alcaldias_sel.append(a)
                    # append: Agrega la alcaldía seleccionada a la lista final

        if not alcaldias_sel:
            st.info("Selecciona al menos una alcaldía para ver datos.")
            # Mensaje informativo si quedó vacía la selección

    return {"alcaldias_sel": alcaldias_sel}
    # Devuelve diccionario con la selección para que app.py lo use en el filtrado

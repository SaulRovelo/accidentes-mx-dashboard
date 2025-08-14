# Módulo para construir la barra lateral (sidebar).
# Proporciona controles para seleccionar alcaldías, rango de meses y tipos de evento.
# Devuelve un diccionario con todos los valores seleccionados por el usuario.

import streamlit as st  # Framework para apps web interactivas
from .theme import MESES, MESES_A_NUM  # Catálogos y mapeos de meses desde theme.py

def sidebar_filters(df):
    # sidebar_filters: Genera y muestra los filtros en el panel lateral (sidebar).
    # df: DataFrame que contiene las columnas 'alcaldia', 'fecha_evento', 'tipo_evento'.

    with st.sidebar.expander("🔎 Filtros interactivos", expanded=True):
        # st.sidebar.expander: Crea un panel desplegable en la barra lateral.
        # expanded=True: El panel se muestra abierto por defecto.

        st.markdown("### 🏙️ Alcaldías")
        # sorted(...): Ordena alfabéticamente las alcaldías únicas no nulas.
        alcaldias = sorted(df["alcaldia"].dropna().unique())

        cols = st.columns(2)  # Crea dos columnas para mostrar checkboxes en dos listas
        alcaldias_sel = []  # Lista para guardar las alcaldías seleccionadas

        seleccionar_todas = st.checkbox("Seleccionar todas", value=True, key="all_alc")
        # Checkbox general para seleccionar todas las alcaldías por defecto.
        if seleccionar_todas:
            alcaldias_sel = alcaldias
        else:
            # Si no se seleccionan todas, mostrar checkboxes individuales
            for i, a in enumerate(alcaldias):
                if cols[i % 2].checkbox(a, key=f"alc_{a}"):
                    alcaldias_sel.append(a)

        st.divider()  # Línea divisoria visual

        st.markdown("### 📆 Selecciona el rango de meses:")
        # Slider para elegir un mes de inicio y fin
        mes_inicio, mes_fin = st.select_slider(
            label=" ",  # Label vacío para no duplicar el texto
            options=MESES,  # Lista de meses (desde theme.py)
            value=(MESES[0], MESES[-1]),  # Valor inicial: Enero a Diciembre
            key="meses_slider"
        )
        # Convierte los nombres de meses a números usando el mapeo MESES_A_NUM
        mes_inicio_num, mes_fin_num = MESES_A_NUM[mes_inicio], MESES_A_NUM[mes_fin]

        st.markdown("### 🚨 Tipo de evento")
        # Lista de tipos de evento únicos y ordenados alfabéticamente
        tipos = sorted(df["tipo_evento"].dropna().unique())
        cols_ev = st.columns(2)  # Muestra los tipos en dos columnas
        tipos_sel = []  # Lista para guardar los tipos de evento seleccionados

        todos_ev = st.checkbox("Seleccionar todos", value=True, key="all_ev")
        # Checkbox general para seleccionar todos los tipos de evento
        if todos_ev:
            tipos_sel = tipos
        else:
            # Si no se seleccionan todos, mostrar checkboxes individuales
            for i, t in enumerate(tipos):
                if cols_ev[i % 2].checkbox(t, key=f"ev_{t}"):
                    tipos_sel.append(t)

    # Devuelve un diccionario con las selecciones hechas por el usuario
    return {
        "alcaldias_sel": alcaldias_sel,       # Lista de alcaldías seleccionadas
        "mes_inicio_num": mes_inicio_num,     # Mes inicial en formato numérico
        "mes_fin_num": mes_fin_num,           # Mes final en formato numérico
        "tipos_evento_sel": tipos_sel,        # Lista de tipos de evento seleccionados
    }

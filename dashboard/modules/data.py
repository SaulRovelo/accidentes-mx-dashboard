# Módulo para carga y filtrado de datos
# Contiene funciones reutilizables para leer el CSV y aplicar filtros según la selección del usuario.
# Mejora la organización y evita repetir lógica en el dashboard.

import pandas as pd
import streamlit as st
from .theme import DIAS_SEMANA

@st.cache_data(ttl=3600, show_spinner=False)
# @st.cache_data: Guarda en caché el resultado de la función para mejorar el rendimiento.
# ttl=3600: Tiempo de vida de la caché en segundos (1 hora).
# show_spinner=False: Oculta el spinner de carga mientras se ejecuta la función.


# load_data: Carga un archivo CSV en un DataFrame, agrega columna 'mes' y convierte 'fecha_evento' a datetime.
def load_data(path: str) -> pd.DataFrame:
    #df = pd.read_csv("data/accidentes_cdmx_limpio.csv", parse_dates=["fecha_evento"])

    # path: Ruta del archivo CSV a cargar.
    df = pd.read_csv(path, parse_dates=["fecha_evento"])
    # pd.read_csv(): Lee el archivo CSV.
    # parse_dates=["fecha_evento"]: Convierte la columna fecha_evento a tipo datetime.
    
    df["mes"] = df["fecha_evento"].dt.month
    # .dt.month: Extrae el número de mes (1=Enero, 12=Diciembre) para análisis temporal.

    df["hora"] = pd.to_datetime(df["hora_evento"].astype(str), format="%H:%M:%S", errors="coerce").dt.hour
    # .dt.hour: Extrae la hora del evento para análisis temporal.
    # .astype(str): Convierte la columna a tipo string para asegurar formato correcto.
    # format="%H:%M:%S": Especifica el formato de la hora (horas:minutos:segundos).
    # errors="coerce": Convierte valores no válidos a NaT (Not a Time).


    df["dia_semana_num"] = df["fecha_evento"].dt.dayofweek  # 0 = lunes
    # .dt.dayofweek: Obtiene el día de la semana como número (0=Lunes, 6=Domingo).
    df["dia_semana_nombre"] = df["dia_semana_num"].map({i: d for i, d in enumerate(DIAS_SEMANA)})
    # .map(): Reemplaza números por nombres de días (0→"Lunes", ..., 6→"Domingo").



    return df
    # Devuelve el DataFrame cargado y con la columna "mes" añadida.

# Esta función recibe directamente las selecciones del panel lateral (sidebar)
# filter_data: Filtra el DataFrame según alcaldías, rango de meses y tipos de evento.  
def filter_data(df: pd.DataFrame,
                alcaldias_sel: list,
                mes_inicio_num: int,
                mes_fin_num: int,
                tipos_evento_sel: list | None = None) -> pd.DataFrame:
    # df: DataFrame original de accidentes.
    # alcaldias_sel: Lista de alcaldías seleccionadas.
    # mes_inicio_num, mes_fin_num: Mes inicial y final como números.
    # tipos_evento_sel: Lista de tipos de evento seleccionados.

    # Fallback: si no se selecciona ninguna alcaldía, usar todas
    if not alcaldias_sel:
        alcaldias_sel = sorted(df["alcaldia"].dropna().unique())
        # sorted(): Ordena alfabéticamente.
        # dropna(): Elimina valores nulos.
        # unique(): Obtiene valores únicos.

    # mask: Condición booleana para filtrar por alcaldías y rango de meses
    mask = df["alcaldia"].isin(alcaldias_sel) & df["mes"].between(mes_inicio_num, mes_fin_num)

    # Si hay tipos de evento seleccionados, se añade al filtro
    if tipos_evento_sel is not None and len(tipos_evento_sel) > 0:
        mask &= df["tipo_evento"].isin(tipos_evento_sel)

    # Devuelve una copia del DataFrame filtrado
    return df.loc[mask].copy()

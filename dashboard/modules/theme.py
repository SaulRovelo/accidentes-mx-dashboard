# Módulo de tema y catálogos para el dashboard (Dash + Plotly)

# -----------------------
# Colores y estilos
# -----------------------
# Paleta cualitativa con mayor variedad (azules, verdes, morados, naranjas, turquesa, rosa, gris azulado)
PALETA = [
    "#f4a261",  # Terracota suave
    "#2a9d8f",  # Verde agua sobrio
    "#f5dda1",  # Amarillo dorado tenue
    "#264653",  # Azul petróleo elegante
    "#a8dadc",  # Azul pastel claro
    "#8ecae6",  # Azul cielo suave
    "#f3cd6e",  # Amarillo vibrante
    "#219ebc",  # Azul acero sutil
    "#b5838d",  # Rosa antiguo
    "#6a994e",  # Verde oliva fresco
]




TEMPLATE = "plotly_white"
MAPBOX_STYLE = "carto-positron"

# Tipografía global a usar en apply_base_layout() dentro de charts.py
FONT_FAMILY = "Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif"

# Enlace a la fuente de datos (ajusta al dataset exacto que usas)
DATOS_FUENTE_URL = "https://datos.cdmx.gob.mx/dataset/hechos-de-transito-registrados-por-la-ssc-2024-serie-de-datos-ampliada-no-comparativa"  # <-- reemplázalo por el link específico del CSV que usaste

# -----------------------
# Catálogos de tiempo
# -----------------------
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
         "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

MESES_A_NUM = {m: i+1 for i, m in enumerate(MESES)}
NUM_A_MESES = {v: k for k, v in MESES_A_NUM.items()}

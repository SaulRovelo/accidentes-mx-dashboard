# Módulo de tema y catálogos para el dashboard (Dash + Plotly)

# -----------------------
# Colores y estilos
# -----------------------
# Paleta cualitativa con mayor variedad (azules, verdes, morados, naranjas, turquesa, rosa, gris azulado)
PALETA = [
    "#2563EB",  # azul
    "#10B981",  # verde
    "#F59E0B",  # ámbar/naranja
    "#8B5CF6",  # morado
    "#06B6D4",  # turquesa
    "#EF4444",  # rojo
    "#F472B6",  # rosa
    "#64748B",  # slate (gris azulado)
    "#22C55E",  # verde claro
    "#3B82F6",  # azul medio
]

TEMPLATE = "plotly_white"
MAPBOX_STYLE = "carto-positron"

# Tipografía global a usar en apply_base_layout() dentro de charts.py
FONT_FAMILY = "Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif"

# Enlace a la fuente de datos (ajusta al dataset exacto que usas)
DATOS_FUENTE_URL = "https://datos.cdmx.gob.mx/"  # <-- reemplázalo por el link específico del CSV que usaste

# -----------------------
# Catálogos de tiempo
# -----------------------
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
         "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

MESES_A_NUM = {m: i+1 for i, m in enumerate(MESES)}
NUM_A_MESES = {v: k for k, v in MESES_A_NUM.items()}

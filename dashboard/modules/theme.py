# Módulo centralizado para definir paleta de colores, estilo Plotly y catálogos (meses/días) 
# con sus mapeos numéricos. 


PALETA = ["#FF6361", "#58508D", "#FFA600", "#003F5C", "#BC5090", "#2F4B7C"]
# PALETA: Lista de colores base para todos los gráficos

TEMPLATE = "plotly_white"
# TEMPLATE: Estilo global de Plotly. 

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
# DIAS_SEMANA: Catálogo ordenado (L→D)

MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
# MESES: Catálogo ordenado (Enero→Diciembre).

MESES_A_NUM = {m: i+1 for i, m in enumerate(MESES)}
# MESES_A_NUM: Diccionario de mapeo mes→número (Enero:1, ..., Diciembre:12).
# enumerate(MESES): genera pares (i, nombre_mes) empezando en 0 → por eso i+1.

NUM_A_MESES = {v: k for k, v in MESES_A_NUM.items()}
# NUM_A_MESES: Diccionario inverso número→mes (1:"Enero", ..., 12:"Diciembre").
# items(): recorre pares (clave, valor) del diccionario original para construir el inverso.

MAPBOX_STYLE = "carto-positron"  # o "open-street-map"
# MAPBOX_STYLE: Estilo de mapa. 


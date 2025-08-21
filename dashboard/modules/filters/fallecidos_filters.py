# ---- mapeos posición (0..100) <-> umbral real (0..100) ----
HARD_MAX = 100

def umbral_from_pos(pos: float) -> int:
    pos = max(0, min(100, float(pos)))
    if pos <= 78:
        return round((pos / 78) * 50)                 # 0..50
    return round(50 + (pos - 78) / 22 * (HARD_MAX-50))# 50..100

def pos_from_umbral(v: int) -> float:
    v = max(0, min(HARD_MAX, int(v)))
    if v <= 50:
        return 78 * (v / 50)                          # 0..78
    return 78 + (v - 50) * 22 / (HARD_MAX - 50)       # 78..100

def _marks_0_50_100() -> dict:
    # Solo 0–50 cada 10 y 100; SIN 75 ni 125
    vals = [0, 10, 20, 30, 40, 50, 100]
    marks = {}
    for v in vals:
        p = int(round(pos_from_umbral(v)))            # clave = posición comprimida
        marks[p] = {"label": f"{v}"}                  # sin transform por defecto

    # Ajusta bordes para que no “se salgan”
    k0 = min(marks.keys()); k1 = max(marks.keys())
    marks[k0]["style"] = {"transform": "translateX(0%)", "textAlign": "left", "whiteSpace": "nowrap"}
    marks[k1]["style"] = {"transform": "translateX(-100%)", "textAlign": "right", "whiteSpace": "nowrap"}
    return marks

def slider_min_fallecidos(_: int, __: int):
    from dash import dcc
    return dcc.Slider(
        id="slider-min-fallecidos",
        min=0, max=100, step=1, value=0,
        marks=_marks_0_50_100(),
        tooltip={"always_visible": False},
        className="slider-negro mt-2"
    )

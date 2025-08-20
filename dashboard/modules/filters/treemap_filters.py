# dashboard/modules/filters/treemap_filters.py
import math
from dash import dcc

def _nice_number(x, round_to=True):
    if x <= 0:
        return 1.0
    exp = math.floor(math.log10(x))
    f = x / (10 ** exp)
    if round_to:
        if f < 1.5: nf = 1
        elif f < 3: nf = 2
        elif f < 7: nf = 5
        else: nf = 10
    else:
        if f <= 1: nf = 1
        elif f <= 2: nf = 2
        elif f <= 5: nf = 5
        else: nf = 10
    return nf * (10 ** exp)

def build_slider_marks(min_v, max_v, target_ticks=6):
    span = max_v - min_v
    if span <= 0:
        return {min_v: f"{min_v:,}"}
    step = int(_nice_number(span / (target_ticks - 1), round_to=True))
    step = max(100, step)
    start = (math.ceil(min_v / step)) * step
    values = [min_v]
    v = start
    while v < max_v:
        values.append(v)
        v += step
    if values[-1] != max_v:
        values.append(max_v)
    seen, ordered = set(), []
    for n in values:
        if n not in seen:
            ordered.append(n); seen.add(n)
    return {n: f"{n:,}" for n in ordered}

def slider_min_accidentes(min_val, max_val):
    return dcc.Slider(
        id="slider-min-accidentes",
        min=min_val,
        max=max_val,
        step=50,
        value=min_val,
        marks=build_slider_marks(min_val, max_val),
        tooltip={"always_visible": False},
        className="mt-3"
    )

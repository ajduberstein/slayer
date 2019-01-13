def round_to_nearest_multiple(x, base=5):
    return float(base * round(float(x)/base))

from .viewport_helpers import get_n_pct  # noqa

from typing import Dict, Any
from valuation.constants import TOTAL_CURR_ASSETS_KEY, TOTAL_CURR_LIAB_KEY

def compute_current_ratio(deco: Dict[str, Any]) -> float:
    return deco.get(TOTAL_CURR_ASSETS_KEY, 0) / deco.get(TOTAL_CURR_LIAB_KEY, 1e-5)

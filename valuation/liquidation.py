import numpy as np
from typing import Dict, Any
from valuation.constants import (
    TOTAL_CURR_ASSETS_KEY,
    TOTAL_CURR_LIAB_KEY,
    SHARES_OUTS_KEY,
    CASH_AND_EQUIV_KEY,
    RECEIVABLES_FACTOR_KEY,
    NET_RECEIVABLES_KEY,
    INVENTORY_FACTOR_KEY,
    INVENTORY_KEY,
    PPE_FACTOR_KEY,
    PPE_KEY,
    TOTAL_LIAB_KEY,
)


def compute_current_ratio(deco: Dict[str, Any]) -> float:
    if not isinstance(deco, dict):
        raise TypeError("`deco` attribute must be a dictionary")
    current_assets = deco.get(TOTAL_CURR_ASSETS_KEY, 0)
    current_liab = deco.get(TOTAL_CURR_LIAB_KEY, 0)
    if current_liab == 0:
        current_liab = 1e-6
    return current_assets / current_liab

def compute_ncav(deco: Dict[str, Any]) -> float:
    if not isinstance(deco, dict):
        raise TypeError("`deco` attribute must be a dictionary")
    return deco.get(TOTAL_CURR_ASSETS_KEY, 0) - deco.get(TOTAL_LIAB_KEY, 0)

def compute_liqv(deco: Dict[str, Any], factors: Dict[str, float]) -> float:
    if not isinstance(deco, dict):
        raise TypeError("`deco` attribute must be a dictionary")
    if not isinstance(factors, dict):
        raise TypeError("`factors` attribute must be a dictionary")
    if not all([key in factors for key in (RECEIVABLES_FACTOR_KEY, INVENTORY_FACTOR_KEY, PPE_FACTOR_KEY)]):
        raise ValueError("`factors` must have all the following keys : 'receivables_factor', 'inventory_factor' and 'ppe_factor'")
    factored_assets = (
        deco.get(CASH_AND_EQUIV_KEY, 0) +
        sum(
            [
                factors[factor_key] * deco.get(asset_key, 0) for factor_key, asset_key in [
                    (RECEIVABLES_FACTOR_KEY, NET_RECEIVABLES_KEY),
                    (INVENTORY_FACTOR_KEY, INVENTORY_KEY),
                    (PPE_FACTOR_KEY, PPE_KEY),
                ]
            ]
        )
    )
    total_liab = deco.get(TOTAL_LIAB_KEY, 0)
    return factored_assets - total_liab

def compute_ncavps():
    pass

def compute_liqvps():
    if deco["weightedAverageShsOutDil"] == 0:
        return -np.Inf
    liqv = compute_liqv(deco, factors)
    return liqv / deco["weightedAverageShsOutDil"]

def compute_prelim_ncav():
    pass

def get_price_from_dict():
    pass

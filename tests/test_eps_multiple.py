import pytest
import numpy as np
from valuation.eps_multiple import compute_fp, compute_pfv, compute_pex_value_handler

TOLERANCE = 1e-3

@pytest.mark.parametrize(
    "eps, growth_value, years, future_pe, fp",
    [
        (None, 0.20, 7, 9, "all attributes must be numeric"),
        (1, 0.20, [], 9, "all attributes must be numeric"),
        (1, 0.20, -1, 9, "`years` attribute must be a positive integer"),
        (1, 0.20, -1, -1, "`years` attribute must be a positive integer"),
        (1, 0.20, 1, -1, "`future_pe` attribute must be positive"),
        (1.5, 0.20, 7, 9, 48.373),
    ]
)
def test_compute_fp_crash(eps, growth_value, years, future_pe, fp):
    try:
        _ = compute_fp(
            eps, growth_value, years, future_pe
        )
    except (TypeError, AttributeError) as err:
        assert fp == str(err)

@pytest.mark.usefixtures("fp_variables")
def test_compute_fp(fp_variables):
    future_value = compute_fp(
        fp_variables.get("eps"),
        fp_variables.get("growth_value"),
        fp_variables.get("years"),
        fp_variables.get("future_pe"),
    )
    assert np.isclose(
        future_value, fp_variables.get("fp"), atol=TOLERANCE
        )

@pytest.mark.parametrize(
    "fp, return_value, years, pfv",
    [
        (None, 0.20, 2, "all attributes must numerical"),
        (10, "", 2, "all attributes must numerical"),
        (10, 0.20, [], "all attributes must numerical"),
        (10, -0.7, 6, "though numerically possible for negative values, the `return_value` attribute must be greater than or equal to zero"),
        (10, 0.2, 0, "`years` attribute must be greater than zero"),
    ]
)
def test_compute_pfv_crash(fp, return_value, years, pfv):
    try:
        _ = compute_pfv(fp, return_value, years)
    except (TypeError, ValueError) as err:
        assert pfv == str(err)

@pytest.mark.usefixtures("pfv_variables")
def test_compute_pfv(pfv_variables):
    fp = pfv_variables.get("fp")
    return_value = pfv_variables.get("return_value")
    years = pfv_variables.get("years")
    pfv = pfv_variables.get("pfv")
    computed_pfv = compute_pfv(fp, return_value, years)
    assert np.isclose(computed_pfv, pfv, atol=TOLERANCE)
    
    return_value = 1000
    pfv = 1.075
    computed_pfv = compute_pfv(fp, return_value, years)
    assert np.isclose(computed_pfv, pfv, atol=TOLERANCE)


"""def compute_pex_value_handler(
    eps: float,
    growth_value: float,
    return_value: float,
    future_pe: float,
    years: int,
) -> float:
    fp = compute_fp(eps, growth_value, years, future_pe)
    pfv = compute_pfv(fp, return_value, years)
    return pfv"""

@pytest.mark.parametrize(
    "eps, growth_value, return_value, future_pe, years, pfv",
    [
        (None, 1, 1, 1, 1, "all attributes must be numerical"),
        (1, 1, [], 1, 1, "all attributes must be numerical"),
        (1, 1, 1, 1, "", "all attributes must be numerical"),
        (9, -1, -1, 1, -1, "thought numerically possible for negative values, `growth_value` and `return_value` must be greater or equal to zero"),
        (9, 0.15, -1, -1, -1, "thought numerically possible for negative values, `growth_value` and `return_value` must be greater or equal to zero"),
        (9, 0.15, 0.15, -1, -1, "thought numerically possible for other values, `future_pe` must be positive"),
        (9, 0.15, 0.15, 1, -1, "`years` attribute must be positive"),
    ]
)
def test_compute_pex_value_handler_crash(eps, growth_value, return_value, future_pe, years, pfv):
    try:
        _ = compute_pex_value_handler(eps, growth_value, return_value, future_pe, years)
    except (TypeError, ValueError) as err:
        assert pfv == str(err)

@pytest.mark.usefixtures("pex_handler_variables")
def test_compute_pex_value_handler(pex_handler_variables):
    eps, growth_value, return_value, future_pe, years, pfv = (
        pex_handler_variables.get("eps"),
        pex_handler_variables.get("growth_value"),
        pex_handler_variables.get("return_value"),
        pex_handler_variables.get("future_pe"),
        pex_handler_variables.get("years"),
        pex_handler_variables.get("pfv"),
    )
    computed_pfv = compute_pex_value_handler(eps, growth_value, return_value, future_pe, years)
    assert np.isclose(computed_pfv, pfv, atol=TOLERANCE)

    growth_value = 1000
    return_value = 1000
    pfv = 34.042
    computed_pfv = compute_pex_value_handler(eps, growth_value, return_value, future_pe, years)
    assert np.isclose(computed_pfv, pfv, atol=TOLERANCE)

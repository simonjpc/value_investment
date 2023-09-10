import pytest
import numpy as np
from valuation.eps_multiple import compute_fp

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
def test_compute_fp_exceptions(eps, growth_value, years, future_pe, fp):
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

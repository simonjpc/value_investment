import pytest
import numpy as np
from valuation.liquidation import (
    compute_current_ratio,
    compute_ncav,
    compute_liqv,
    compute_ncavps,
    compute_liqvps,
    positive_prelim_ncav,
    get_price_from_dict,
)
from valuation.constants import CURRENT_ASSETS_FACTORS

TOLERANCE = 1e-3


@pytest.mark.parametrize(
    "deco, current_ratio",
    [
        (None, "`deco` attribute must be a dictionary"),
        ("", "`deco` attribute must be a dictionary"),
    ]
)
def test_compute_current_ratio_crash(deco, current_ratio):
    with pytest.raises(TypeError) as e:
        _ = compute_current_ratio(deco)
    assert str(e.value) == current_ratio

@pytest.mark.usefixtures("current_ratio_variables")
def test_compute_current_ratio(current_ratio_variables):
    deco, expected_current_ratio,  = (
        current_ratio_variables.get("deco"),
        current_ratio_variables.get("current_ratio"),
    )
    computed_current_ratio = compute_current_ratio(deco)
    assert np.isclose(expected_current_ratio, computed_current_ratio, atol=TOLERANCE)

    deco["totalCurrentLiabilities"] = 0
    expected_current_ratio = 732e10
    computed_current_ratio = compute_current_ratio(deco)
    assert np.isclose(expected_current_ratio, computed_current_ratio, atol=TOLERANCE)


@pytest.mark.parametrize(
    "deco, ncav",
    [
        (None, "`deco` attribute must be a dictionary"),
        ("", "`deco` attribute must be a dictionary"),
    ]
)
def test_compute_ncav_crash(deco, ncav):
    with pytest.raises(TypeError) as e:
        _ = compute_ncav(deco)
    assert str(e.value) == ncav

@pytest.mark.usefixtures("ncav_variables")
def test_compute_ncav(ncav_variables):
    deco, expected_ncav  = (
        ncav_variables.get("deco"),
        ncav_variables.get("ncav"),
    )
    computed_ncav = compute_ncav(deco)
    assert np.isclose(expected_ncav, computed_ncav, atol=TOLERANCE)


@pytest.mark.parametrize(
    "deco, factors, liqv",
    [
        (None, None, "`deco` attribute must be a dictionary"),
        ({}, None, "`factors` attribute must be a dictionary"),
        ({}, {}, "`factors` must have all the following keys : 'receivables_factor', 'inventory_factor' and 'ppe_factor'"),
    ]
)
def test_compute_liqv_crash(deco, factors, liqv):
    with pytest.raises((TypeError, ValueError)) as e:
        _ = compute_liqv(deco, factors)
    assert str(e.value) == liqv

@pytest.mark.usefixtures("liqv_variables")
def test_compute_ncav(liqv_variables):
    deco, expected_liqv  = (
        liqv_variables.get("deco"),

        liqv_variables.get("liqv"),
    )
    computed_liqv = compute_liqv(deco, CURRENT_ASSETS_FACTORS)
    assert np.isclose(expected_liqv, computed_liqv, atol=TOLERANCE)

    for key in (
        "cashAndCashEquivalents", "netReceivables", "inventory", "propertyPlantEquipmentNet"
    ):
        _ = deco.pop(key)
        
    expected_liqv = -4190000
    computed_liqv = compute_liqv(deco, CURRENT_ASSETS_FACTORS)
    assert np.isclose(expected_liqv, computed_liqv, atol=TOLERANCE)


@pytest.mark.parametrize(
    "deco, ncavps",
    [
        (None, "`deco` attribute must be a dictionary"),
        ("", "`deco` attribute must be a dictionary"),
    ]
)
def test_compute_ncavps_crash(deco, ncavps):
    with pytest.raises(TypeError) as e:
        _ = compute_ncavps(deco)
    assert str(e.value) == ncavps

@pytest.mark.usefixtures("ncav_variables")
def test_compute_ncavps(ncav_variables):
    deco, expected_ncavps  = (
        ncav_variables.get("deco"),
        ncav_variables.get("ncavps"),
    )
    computed_ncavps = compute_ncavps(deco)
    assert np.isclose(expected_ncavps, computed_ncavps, atol=TOLERANCE)


@pytest.mark.parametrize(
    "deco, liqvps",
    [
        (None, "`deco` attribute must be a dictionary"),
        ("", "`deco` attribute must be a dictionary"),
    ]
)
def test_compute_liqvps_crash(deco, liqvps):
    with pytest.raises(TypeError) as e:
        _ = compute_liqvps(deco, CURRENT_ASSETS_FACTORS)
    assert str(e.value) == liqvps

@pytest.mark.usefixtures("liqv_variables")
def test_compute_liqvps(liqv_variables):
    deco, expected_liqvps  = (
        liqv_variables.get("deco"),
        liqv_variables.get("liqvps"),
    )
    computed_liqvps = compute_liqvps(deco, CURRENT_ASSETS_FACTORS)
    assert np.isclose(expected_liqvps, computed_liqvps, atol=TOLERANCE)


@pytest.mark.parametrize(
    "deco, positive_ncav",
    [
        (None, "`deco` attribute must be a dictionary"),
        ("", "`deco` attribute must be a dictionary"),
    ]
)
def test_positive_prelim_ncav_crash(deco, positive_ncav):
    with pytest.raises(TypeError) as e:
        _ = positive_prelim_ncav(deco)
    assert str(e.value) == positive_ncav

@pytest.mark.usefixtures("ncav_variables")
def test_positive_prelim_ncav(ncav_variables):
    deco, expected_positive_ncav  = (
        ncav_variables.get("deco"),
        True,
    )
    computed_positive_ncav = positive_prelim_ncav(deco)
    assert np.isclose(expected_positive_ncav, computed_positive_ncav, atol=TOLERANCE)


@pytest.mark.parametrize(
    "deco, price",
    [
        (None, "`deco` attribute must be a dictionary"),
        ("", "`deco` attribute must be a dictionary"),
    ]
)
def test_get_price_from_dict_crash(deco, price):
    with pytest.raises(TypeError) as e:
        _ = get_price_from_dict(deco)
    assert str(e.value) == price

@pytest.mark.usefixtures("price_from_dict_variables")
def test_get_price_from_dict(price_from_dict_variables):
    expected_price  = price_from_dict_variables.get("price"),
    computed_price = get_price_from_dict(price_from_dict_variables)
    assert np.isclose(expected_price, computed_price, atol=TOLERANCE)

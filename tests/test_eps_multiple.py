import pytest
import numpy as np
import pandas as pd
from valuation.eps_multiple import (
    compute_fp,
    compute_pfv,
    compute_pex_value_handler,
    compute_pex_value,
    compute_tangible_book_value,
    compute_tangible_book_value_ps,
    compute_discounted_tangible_book_value,
    compute_discounted_tangible_book_value_ps,
    compute_pe_ratio,
    compute_de_ratio,
    get_date_range,
    get_reporting_window,
    get_price_history,
    compute_price_at_reporting_date,
    growth_function,
    compute_growth,
)
from valuation.constants import (
    TOTAL_ASSETS_KEY,
    SHARES_OUTS_KEY,
    EXPECTED_OBLIGATIONS,
    TOTAL_LIAB_KEY,
    STOCKHOLDERS_EQUITY_KEY,
    DATE_KEY,
)

TOLERANCE = 1e-3


@pytest.mark.parametrize(
    "eps, growth_value, years, future_pe, fp",
    [
        (None, 0.20, 7, 9, "all attributes must be numeric"),
        (1, 0.20, [], 9, "all attributes must be numeric"),
        (1, 0.20, -1, 9, "`years` attribute must be a positive integer"),
        (1, 0.20, -1, -1, "`years` attribute must be a positive integer"),
        (1, 0.20, 1, -1, "`future_pe` attribute must be positive"),
    ],
)
def test_compute_fp_crash(eps, growth_value, years, future_pe, fp):
    with pytest.raises((TypeError, AttributeError)) as e:
        _ = compute_fp(eps, growth_value, years, future_pe)
    assert str(e.value) == fp


@pytest.mark.usefixtures("fp_variables")
def test_compute_fp(fp_variables):
    future_value = compute_fp(
        fp_variables.get("eps"),
        fp_variables.get("growth_value"),
        fp_variables.get("years"),
        fp_variables.get("future_pe"),
    )
    assert np.isclose(future_value, fp_variables.get("fp"), atol=TOLERANCE)


@pytest.mark.parametrize(
    "fp, return_value, years, pfv",
    [
        (None, 0.20, 2, "all attributes must numerical"),
        (10, "", 2, "all attributes must numerical"),
        (10, 0.20, [], "all attributes must numerical"),
        (
            10,
            -0.7,
            6,
            "though numerically possible for negative values, the `return_value` attribute must be greater than or equal to zero",
        ),
        (10, 0.2, 0, "`years` attribute must be greater than zero"),
    ],
)
def test_compute_pfv_crash(fp, return_value, years, pfv):
    with pytest.raises((TypeError, ValueError)) as e:
        _ = compute_pfv(fp, return_value, years)
    assert str(e.value) == pfv


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


@pytest.mark.parametrize(
    "eps, growth_value, return_value, future_pe, years, pfv",
    [
        (None, 1, 1, 1, 1, "all attributes must be numerical"),
        (1, 1, [], 1, 1, "all attributes must be numerical"),
        (1, 1, 1, 1, "", "all attributes must be numerical"),
        (
            9,
            -1,
            -1,
            1,
            -1,
            "thought numerically possible for negative values, `growth_value` and `return_value` must be greater or equal to zero",
        ),
        (
            9,
            0.15,
            -1,
            -1,
            -1,
            "thought numerically possible for negative values, `growth_value` and `return_value` must be greater or equal to zero",
        ),
        (
            9,
            0.15,
            0.15,
            -1,
            -1,
            "thought numerically possible for other values, `future_pe` must be positive",
        ),
        (9, 0.15, 0.15, 1, -1, "`years` attribute must be positive"),
    ],
)
def test_compute_pex_value_handler_crash(
    eps, growth_value, return_value, future_pe, years, pfv
):
    with pytest.raises((TypeError, ValueError)) as e:
        _ = compute_pex_value_handler(eps, growth_value, return_value, future_pe, years)
    assert str(e.value) == pfv


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
    computed_pfv = compute_pex_value_handler(
        eps, growth_value, return_value, future_pe, years
    )
    assert np.isclose(computed_pfv, pfv, atol=TOLERANCE)

    growth_value = 1000
    return_value = 1000
    pfv = 34.042
    computed_pfv = compute_pex_value_handler(
        eps, growth_value, return_value, future_pe, years
    )
    assert np.isclose(computed_pfv, pfv, atol=TOLERANCE)


@pytest.mark.parametrize(
    "deco, growth_value, return_value, future_pe, years, pfv",
    [
        (None, [], "", -1, -1, "`deco` attribute must be a dictionary"),
        ({}, [], "", -1, -1, "`eps` key is expected in `deco`"),
        (
            {"eps": -1},
            [],
            "",
            -1,
            -1,
            "attributes `growth_value`, `return_value`, `future_pe` and `years` must all be numeric",
        ),
        (
            {"eps": -1},
            0.15,
            "",
            -1,
            -1,
            "attributes `growth_value`, `return_value`, `future_pe` and `years` must all be numeric",
        ),
        (
            {"eps": -1},
            0.15,
            0.20,
            -1,
            -1,
            "thought numerically possible for other values, `future_pe` must be positive",
        ),
        ({"eps": -1}, 0.15, 0.20, 1, -1, "`years` attribute must be positive"),
    ],
)
def test_compute_pex_value_crash(
    deco, growth_value, return_value, future_pe, years, pfv
):
    with pytest.raises((TypeError, ValueError)) as e:
        _ = compute_pex_value(deco, growth_value, return_value, future_pe, years)
    assert str(e.value) == pfv


@pytest.mark.usefixtures("pex_variables")
def test_compute_pex_value(pex_variables):
    deco, growth_value, return_value, future_pe, years, pfv = (
        pex_variables.get("deco"),
        pex_variables.get("growth_value"),
        pex_variables.get("return_value"),
        pex_variables.get("future_pe"),
        pex_variables.get("years"),
        pex_variables.get("pfv"),
    )
    computed_pfv = compute_pex_value(deco, growth_value, return_value, future_pe, years)
    assert np.isclose(computed_pfv, pfv, atol=TOLERANCE)

    growth_value = 1000
    return_value = 1000
    pfv = -34.042

    computed_pfv = compute_pex_value(deco, growth_value, return_value, future_pe, years)
    assert np.isclose(computed_pfv, pfv, atol=TOLERANCE)


@pytest.mark.parametrize(
    "deco, tangible_bv",
    [
        (None, "`deco` attribute must be a dictionary"),
        ([], "`deco` attribute must be a dictionary"),
    ],
)
def test_compute_tangible_book_value_crash(deco, tangible_bv):
    with pytest.raises(AttributeError) as e:
        _ = compute_tangible_book_value(deco)
    assert str(e.value) == tangible_bv


@pytest.mark.usefixtures("tangible_bv_variables")
def test_compute_tangible_book_value(tangible_bv_variables):
    assert compute_tangible_book_value({}) == 0

    computed_tbv = compute_tangible_book_value(tangible_bv_variables)
    expected_tbv = tangible_bv_variables.get("tangible_bv")
    assert np.isclose(computed_tbv, expected_tbv, atol=TOLERANCE)

    tangible_bv_variables[TOTAL_ASSETS_KEY] = 1
    computed_tbv = compute_tangible_book_value(tangible_bv_variables)
    expected_tbv = -4217999
    assert np.isclose(computed_tbv, expected_tbv, atol=TOLERANCE)


@pytest.mark.parametrize(
    "deco, tangible_bvps",
    [
        (None, "`deco` attribute must be a dictionary"),
        ([], "`deco` attribute must be a dictionary"),
    ],
)
def test_compute_tangible_book_value_ps_crash(deco, tangible_bvps):
    with pytest.raises(AttributeError) as e:
        _ = compute_tangible_book_value_ps(deco)
    assert str(e.value) == tangible_bvps


@pytest.mark.usefixtures("compute_tangible_bvps")
def test_compute_tangible_book_value_ps(compute_tangible_bvps):
    expected_tangible_bvps = compute_tangible_bvps.get("tangible_bvps")
    computed_tangible_bvps = compute_tangible_book_value_ps(compute_tangible_bvps)
    assert np.isclose(expected_tangible_bvps, computed_tangible_bvps, atol=TOLERANCE)

    shares_outs = compute_tangible_bvps.get(SHARES_OUTS_KEY)
    compute_tangible_bvps[SHARES_OUTS_KEY] = 0
    expected_tangible_bvps = compute_tangible_bvps.get("tangible_bv") / 1e-6
    computed_tangible_bvps = compute_tangible_book_value_ps(compute_tangible_bvps)
    assert np.isclose(expected_tangible_bvps, computed_tangible_bvps)
    compute_tangible_bvps[SHARES_OUTS_KEY] = shares_outs

    compute_tangible_bvps[TOTAL_ASSETS_KEY] = 1
    expected_tangible_bvps = -1.339
    computed_tangible_bvps = compute_tangible_book_value_ps(compute_tangible_bvps)
    assert np.isclose(expected_tangible_bvps, computed_tangible_bvps, atol=TOLERANCE)


@pytest.mark.parametrize(
    "deco, dct_tangible_bv",
    [
        (None, "`deco` attribute must be a dictionary"),
        ([], "`deco` attribute must be a dictionary"),
    ],
)
def test_compute_discounted_tangible_book_value_crash(deco, dct_tangible_bv):
    with pytest.raises(AttributeError) as e:
        _ = compute_discounted_tangible_book_value(deco)
    assert str(e.value) == dct_tangible_bv


@pytest.mark.usefixtures("dct_tangible_bv_variables", "tangible_bv_variables")
def test_compute_discounted_tangible_book_value(
    dct_tangible_bv_variables, tangible_bv_variables
):
    expected_dct_tangible_bv = dct_tangible_bv_variables.get("dct_tangible_bv")
    computed_dct_tangible_bv = compute_discounted_tangible_book_value(
        dct_tangible_bv_variables
    )
    assert np.isclose(
        expected_dct_tangible_bv, computed_dct_tangible_bv, atol=TOLERANCE
    )

    tangible_bv = tangible_bv_variables.get("tangible_bv")
    assert tangible_bv >= computed_dct_tangible_bv

    dct_tangible_bv_variables[TOTAL_ASSETS_KEY] = 1
    expected_dct_tangible_bv = -4476999
    computed_dct_tangible_bv = compute_discounted_tangible_book_value(
        dct_tangible_bv_variables
    )
    assert np.isclose(
        expected_dct_tangible_bv, computed_dct_tangible_bv, atol=TOLERANCE
    )


@pytest.mark.parametrize(
    "deco, dct_tangible_bvps",
    [
        (None, "`deco` attribute must be a dictionary"),
        ([], "`deco` attribute must be a dictionary"),
    ],
)
def test_compute_discounted_tangible_book_value_ps_crash(deco, dct_tangible_bvps):
    with pytest.raises(AttributeError) as e:
        _ = compute_discounted_tangible_book_value_ps(deco)
    assert str(e.value) == dct_tangible_bvps


@pytest.mark.usefixtures("compute_dct_tangible_bvps", "compute_tangible_bvps")
def test_compute_discounted_tangible_book_value_ps(
    compute_dct_tangible_bvps, compute_tangible_bvps
):
    computed_dct_tangible_bvps = compute_discounted_tangible_book_value_ps(
        compute_dct_tangible_bvps,
    )
    expected_dct_tangible_bvps = compute_dct_tangible_bvps.get("dct_tangible_bvps")
    assert np.isclose(
        computed_dct_tangible_bvps, expected_dct_tangible_bvps, atol=TOLERANCE
    )

    expected_tangible_bvps = compute_tangible_bvps.get("tangible_bvps")
    assert computed_dct_tangible_bvps <= expected_tangible_bvps

    compute_dct_tangible_bvps[TOTAL_ASSETS_KEY] = 1
    expected_dct_tangible_bvps = -1.421
    computed_dct_tangible_bvps = compute_discounted_tangible_book_value_ps(
        compute_dct_tangible_bvps,
    )
    assert np.isclose(
        computed_dct_tangible_bvps, expected_dct_tangible_bvps, atol=TOLERANCE
    )


@pytest.mark.parametrize(
    "deco, pe_ratio",
    [
        (None, "`deco` attribute must be a dictionary"),
    ],
)
def test_compute_pe_ratio_crash(deco, pe_ratio):
    with pytest.raises(AttributeError) as e:
        _ = compute_pe_ratio(deco)
    assert str(e.value) == pe_ratio


@pytest.mark.usefixtures("pe_ratio_variables")
def test_compute_pe_ratio(pe_ratio_variables):
    expected_pe_ratio = pe_ratio_variables.get("pe_ratio")
    computed_pe_ratio = compute_pe_ratio(pe_ratio_variables)
    assert np.isclose(expected_pe_ratio, computed_pe_ratio)

    eps = pe_ratio_variables.get("eps")
    pe_ratio_variables["eps"] = 0
    low_pe_ratio_thr = 100000
    computed_pe_ratio = compute_pe_ratio(pe_ratio_variables)
    assert computed_pe_ratio > low_pe_ratio_thr
    pe_ratio_variables["eps"] = eps


@pytest.mark.parametrize(
    "deco, obligation_type, ratio",
    [
        (None, "total", "`deco` attribute must be a dictionary"),
        ({}, [], "`obligation_type` attribute must be a string"),
        (
            {},
            "total",
            f"`obligation_type` attribute must be one of the following: {EXPECTED_OBLIGATIONS}",
        ),
    ],
)
def test_compute_de_ratio_crash(deco, obligation_type, ratio):
    with pytest.raises(AttributeError) as e:
        _ = compute_de_ratio(deco, obligation_type)
    assert str(e.value) == ratio


@pytest.mark.usefixtures("de_ratio_variables")
def test_compute_de_ratio(de_ratio_variables):
    expected_de_ratio = de_ratio_variables.get(TOTAL_LIAB_KEY) / de_ratio_variables.get(
        STOCKHOLDERS_EQUITY_KEY
    )
    computed_de_ratio = compute_de_ratio(de_ratio_variables, "totalLiabilities")
    assert np.isclose(expected_de_ratio, computed_de_ratio, atol=TOLERANCE)

    de_ratio_variables[STOCKHOLDERS_EQUITY_KEY] = 0
    expected_de_ratio = 3702e9
    computed_de_ratio = compute_de_ratio(de_ratio_variables, "totalLiabilities")
    assert np.isclose(expected_de_ratio, computed_de_ratio, atol=TOLERANCE)


@pytest.mark.parametrize(
    "date, window_start_offset, window_end_offset, window",
    [
        (None, None, None, "`date` attribute must be a pandas timestamp"),
        (
            pd.Timestamp("19-09-2022"),
            None,
            None,
            "both `window_start_offset` & `window_end_offset` must be positive integers",
        ),
        (
            pd.Timestamp("19-09-2022"),
            3,
            None,
            "both `window_start_offset` & `window_end_offset` must be positive integers",
        ),
        (
            pd.Timestamp("19-09-2022"),
            3,
            -1,
            "both `window_start_offset` & `window_end_offset` must be positive integers",
        ),
        (
            pd.Timestamp("19-09-2022"),
            30,
            15,
            "`window_end_offset` must be greater than or equal to `window_start_offset`",
        ),
    ],
)
def test_get_date_range_crash(date, window_start_offset, window_end_offset, window):
    with pytest.raises((AttributeError, ValueError)) as e:
        _ = get_date_range(date, window_start_offset, window_end_offset)
    assert str(e.value) == window


@pytest.mark.usefixtures("date_range_variables")
def test_get_date_range(date_range_variables):
    date, start, end = (
        date_range_variables["date"],
        date_range_variables["window_start_offset"],
        date_range_variables["window_end_offset"],
    )
    expected_range = (
        str(pd.Timestamp("2022-10-19").date()),
        str(pd.Timestamp("2022-11-04").date()),
    )
    computed_range = get_date_range(date, start, end)
    assert expected_range == computed_range


@pytest.mark.parametrize(
    "deco, window_and_date",
    [
        (None, "`deco attribute must be a dictionary`"),
        ([], "`deco attribute must be a dictionary`"),
    ],
)
def test_get_reporting_window_crash(deco, window_and_date):
    with pytest.raises(AttributeError) as e:
        _ = get_reporting_window(deco)
    assert str(e.value) == window_and_date


@pytest.mark.usefixtures("reporting_date_variables")
def test_get_reporting_window(reporting_date_variables):
    expected_window = reporting_date_variables.get("window")
    expected_output = (expected_window[0], expected_window[1], True)
    computed_output = get_reporting_window(reporting_date_variables)
    assert expected_output == computed_output

    reporting_date_variables["fillingDate"] = None
    expected_output = ("2022-09-09", "2022-09-25", False)
    computed_output = get_reporting_window(reporting_date_variables)
    assert expected_output == computed_output

    reporting_date_variables[DATE_KEY] = None
    expected_output = (None, None, False)
    computed_output = get_reporting_window(reporting_date_variables)
    assert expected_output == computed_output


@pytest.mark.parametrize(
    "deco, price_history",
    [
        (None, "`deco` attribute must be a dictionary"),
        ([], "`deco` attribute must be a dictionary"),
    ],
)
def test_get_price_history_crash(deco, price_history):
    with pytest.raises(AttributeError) as e:
        _ = get_price_history(deco)
    assert str(e.value) == price_history


@pytest.mark.usefixtures("price_hist_variables")
def test_get_price_history(price_hist_variables):
    expected_price_hist = price_hist_variables.get("historical")
    computed_price_hist = get_price_history(price_hist_variables)
    assert expected_price_hist == computed_price_hist

    price_hist_variables = {}
    expected_price_hist = []
    computed_price_hist = get_price_history(price_hist_variables)
    assert expected_price_hist == computed_price_hist


@pytest.mark.parametrize(
    "prices, filling_date_flag, key, avg_price_at_report",
    [
        (None, None, None, "`prices` attribute must be a list"),
        ([], None, None, "`filling_date_flag` attribute must be boolean"),
        ([], True, None, "`key` attribute must be a string"),
    ],
)
def test_compute_price_at_reporting_date_crash(
    prices, filling_date_flag, key, avg_price_at_report
):
    with pytest.raises(AttributeError) as e:
        _ = compute_price_at_reporting_date(
            prices=prices, filling_date_flag=filling_date_flag, key=key
        )
    assert str(e.value) == avg_price_at_report


@pytest.mark.usefixtures("reporting_date_price_variables")
def test_compute_price_at_reporting_date(reporting_date_price_variables):
    expected_prices = reporting_date_price_variables.get("low_prices_false")
    computed_prices = compute_price_at_reporting_date(
        prices=reporting_date_price_variables.get("prices_content"),
        filling_date_flag=False,
        key="low",
    )
    assert np.isclose(expected_prices, computed_prices, atol=TOLERANCE)

    expected_prices = reporting_date_price_variables.get("low_prices_true")
    computed_prices = compute_price_at_reporting_date(
        prices=reporting_date_price_variables.get("prices_content"),
        filling_date_flag=True,
        key="low",
    )
    assert np.isclose(expected_prices, computed_prices, atol=TOLERANCE)

    expected_prices = reporting_date_price_variables.get("high_prices_false")
    computed_prices = compute_price_at_reporting_date(
        prices=reporting_date_price_variables.get("prices_content"),
        filling_date_flag=False,
        key="high",
    )
    assert np.isclose(expected_prices, computed_prices, atol=TOLERANCE)

    expected_prices = reporting_date_price_variables.get("high_prices_true")
    computed_prices = compute_price_at_reporting_date(
        prices=reporting_date_price_variables.get("prices_content"),
        filling_date_flag=True,
        key="high",
    )
    assert np.isclose(expected_prices, computed_prices, atol=TOLERANCE)

    expected_prices = float("inf")
    computed_prices = compute_price_at_reporting_date(
        prices=[], filling_date_flag=False, key="low"
    )
    assert expected_prices == computed_prices

    expected_prices = float("inf")
    computed_prices = compute_price_at_reporting_date(
        prices=[], filling_date_flag=True, key="high"
    )
    assert expected_prices == computed_prices


"""def growth_function(current: float, previous: float, nb_years: int) -> float:
    growth_value = round((current / previous) ** (1/nb_years) - 1, 4)
    return growth_value"""


@pytest.mark.parametrize(
    "current, previous, nb_years, growth",
    [
        (None, None, None, "all attributes must be numerical"),
        (1, None, None, "all attributes must be numerical"),
        (1, 1, None, "all attributes must be numerical"),
        (1, 0, 5, "all attributes must be positive"),
    ],
)
def test_growth_function_crash(current, previous, nb_years, growth):
    with pytest.raises((TypeError, ValueError)) as e:
        _ = growth_function(current, previous, nb_years)
    assert str(e.value) == growth


@pytest.mark.usefixtures("growth_function_variables")
def test_growth_function(growth_function_variables):
    attrs = growth_function_variables.get("pos_pos1")
    current, previous, nb_years, expected_growth = (
        attrs.get("current"),
        attrs.get("previous"),
        attrs.get("nb_years"),
        attrs.get("growth"),
    )
    computed_growth = growth_function(current, previous, nb_years)
    assert np.isclose(expected_growth, computed_growth, atol=TOLERANCE)


"""def compute_growth(current: float, previous: float, nb_years: int) -> float:
    if current == 0:
        current = 1e-6
    if previous == 0:
        previous = 1e-6
    if current > 0 and previous < 0:
        gap = current - previous
        current += gap
        previous += gap
    elif current < 0 and previous > 0:
        gap = previous - current
        current += gap
        previous += gap
    elif current < 0 and previous < 0:
        previous, current = current, previous
        previous = abs(previous)
        current = abs(current)
    growth = growth_function(current, previous, nb_years)
    return growth"""


@pytest.mark.parametrize(
    "current, previous, nb_years, growth",
    [
        (None, None, None, "all attributes must be numerical"),
        (1, None, None, "all attributes must be numerical"),
        (1, 1, None, "all attributes must be numerical"),
    ],
)
def test_compute_growth_crash(current, previous, nb_years, growth):
    with pytest.raises(TypeError) as e:
        _ = compute_growth(current, previous, nb_years)
    assert str(e.value) == growth


@pytest.mark.usefixtures("growth_function_variables")
def test_compute_growth(growth_function_variables):
    for combination in (
        "pos_neg1",
        "pos_neg2",
        "neg_pos1",
        "neg_pos2",
        "neg_neg1",
        "neg_neg2",
        "pos_pos1",
        "pos_pos2",
    ):
        attrs = growth_function_variables.get(combination)
        current, previous, nb_years, expected_growth = (
            attrs.get("current"),
            attrs.get("previous"),
            attrs.get("nb_years"),
            attrs.get("growth"),
        )
        computed_growth = compute_growth(current, previous, nb_years)
        assert np.isclose(expected_growth, computed_growth, atol=TOLERANCE)

    expected_growth = 113.869
    computed_growth = compute_growth(current, 0, nb_years)
    assert np.isclose(expected_growth, computed_growth, atol=TOLERANCE)

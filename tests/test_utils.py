import pytest
import pandas as pd
import numpy as np
from valuation.utils import (
    get_key_from_iterator,
    compute_rate_of_change,
    compute_rates_of_change,
    invert_iterator,
    drop_nulls,
    compute_stat_bound,
    compute_avg_value,
    get_date_from_dictionary,
    handling_negative_vals,
)

TOLERANCE = 1e-3


@pytest.mark.parametrize(
    "iterator, key, element",
    [
        (None, None, "`iterator` attribute must be a list of dictionaries"),
        ([], None, "`key` attribute must be a string"),
    ]
)
def test_get_key_from_iterator_crash(iterator, key, element):
    with pytest.raises(TypeError) as e:
        _ = get_key_from_iterator(iterator, key)
    assert str(e.value) == element

@pytest.mark.usefixtures("balance_sheet_data")
def test_get_key_from_iterator(balance_sheet_data):
    expected_output = [19120000, 20810000, 13743000]
    computed_output = get_key_from_iterator(balance_sheet_data, "totalStockholdersEquity")
    assert expected_output == computed_output

    expected_output = [None, None, None]
    computed_output = get_key_from_iterator(balance_sheet_data, "fake_key")
    assert expected_output == computed_output


@pytest.mark.parametrize(
    "prev_value, current_value, change_rate",
    [
        (None, None, "both `prev_value` and `current_value` attributes must be numerical"),
        (10, "", "both `prev_value` and `current_value` attributes must be numerical"),
    ]
)
def test_compute_rate_of_change_crash(prev_value, current_value, change_rate):
    with pytest.raises(TypeError) as e:
        _ = compute_rate_of_change(prev_value, current_value)
    assert str(e.value) == change_rate

@pytest.mark.usefixtures("rate_of_change_variables")
def test_compute_rate_of_change(rate_of_change_variables):
    print(rate_of_change_variables)
    expected_change = rate_of_change_variables.get("rate_of_change")
    prev_value, current_value = (
        rate_of_change_variables.get("prev_value"), rate_of_change_variables.get("current_value")
    )
    computed_change = compute_rate_of_change(prev_value, current_value)
    assert np.isclose(expected_change, computed_change, atol=TOLERANCE)


@pytest.mark.parametrize(
    "iterator, all_growth",
    [
        (None, "`iterator` attribute must be a list of a tuple"),
        ("", "`iterator` attribute must be a list of a tuple"),
        ([None, 1, 2, 3], "both `prev_value` and `current_value` attributes must be numerical")
    ]
)
def test_compute_rates_of_change_crash(iterator, all_growth):
    with pytest.raises(TypeError) as e:
        _ = compute_rates_of_change(iterator)
    assert str(e.value) == all_growth

@pytest.mark.usefixtures("rates_of_change_variables")
def test_compute_rates_of_change(rates_of_change_variables):
    expected_result = rates_of_change_variables.get("rates_of_change")
    computed_result = compute_rates_of_change(rates_of_change_variables.get("iterator"))
    assert len(expected_result) == len(computed_result)
    assert computed_result[0] == None
    assert all(
        [
            np.isclose(
                expected_result[idx],
                computed_result[idx],
                atol=TOLERANCE,
            ) for idx in range(1, len(expected_result))
        ]
    )


@pytest.mark.parametrize(
    "iterator, inverted_iterator",
    [
        (None, "`iterator` attribute must be a list"),
        ("", "`iterator` attribute must be a list"),
    ]
)
def test_invert_iterator_crash(iterator, inverted_iterator):
    with pytest.raises(TypeError) as e:
        _ = invert_iterator(iterator)
    assert str(e.value) == inverted_iterator

@pytest.mark.usefixtures("inversion_variables")
def test_invert_iterator(inversion_variables):
    expected_result = inversion_variables.get("inverted_iterator")
    computed_result = invert_iterator(inversion_variables.get("iterator"))
    assert expected_result == computed_result


@pytest.mark.parametrize(
    "iterator, iterator_wo_nans",
    [
        (None, "`iterator` attribute must be a list"),
    ]
)
def test_drop_nulls_crash(iterator, iterator_wo_nans):
    with pytest.raises(TypeError) as e:
        _ = drop_nulls(iterator)
    assert str(e.value) == iterator_wo_nans


@pytest.mark.usefixtures("drop_nulls_variables")
def test_drop_nulls(drop_nulls_variables):
    expected_result = drop_nulls_variables.get("iterator_wo_null")
    iterator = drop_nulls_variables.get("iterator")
    computed_result = drop_nulls(iterator)
    assert expected_result == computed_result

    computed_result = drop_nulls(iterator[1:])
    assert expected_result == computed_result


@pytest.mark.parametrize(
    "iterator, q_inf, q_sup, distance, bounds",
    [
        (None, None, None, None, "`iterator` attribute must be a list"),
        ([], None, None, None, "all `q_inf`, `q_sup` and `distance` attributes must be a numerical"),
        ([], 1, None, None, "all `q_inf`, `q_sup` and `distance` attributes must be a numerical"),
        ([], 1, 1, None, "all `q_inf`, `q_sup` and `distance` attributes must be a numerical"),
    ]
)
def test_compute_stat_bound_crash(iterator, q_inf, q_sup, distance, bounds):
    with pytest.raises(TypeError) as e:
        _ = compute_stat_bound(iterator, q_inf, q_sup, distance)
    assert str(e.value) == bounds

@pytest.mark.usefixtures("bounds_variables")
def test_compute_stat_bound(bounds_variables):
    expected_result = bounds_variables.get("bounds")
    iterator = bounds_variables.get("iterator")
    computed_result = compute_stat_bound(iterator)
    assert all(
        [
            np.isclose(
                expected_result[idx],
                computed_result[idx],
                atol=TOLERANCE,
            ) for idx in range(len(computed_result))
        ]
    )


@pytest.mark.parametrize(
    "iterator, avg",
    [
        (None, "`iterator` attribute must be a list or a tuple"),
        ("", "`iterator` attribute must be a list or a tuple"),
        ([1, 2, np.nan], "all elements of `iterator` attribute must be numerical"),
        ([1, 2, None], "all elements of `iterator` attribute must be numerical"),
    ]
)
def test_compute_avg_value_crash(iterator, avg):
    with pytest.raises((TypeError, ValueError)) as e:
        _ = compute_avg_value(iterator)
    assert str(e.value) == avg

@pytest.mark.usefixtures("avg_variables")
def test_compute_avg_value(avg_variables):
    expected_result = avg_variables.get("avg")
    iterator = avg_variables.get("iterator")
    computed_result = compute_avg_value(iterator)
    assert np.isclose(expected_result, computed_result)


@pytest.mark.parametrize(
    "dictionary, date_key, datetime",
    [
        (None, None, "`dictionary` attribute must be a dictionary"),
        ("", None, "`dictionary` attribute must be a dictionary"),
        ({}, "date_key", "No 'date_key' key found in the dictionary")
    ]
)
def test_get_date_from_dictionary_crash(dictionary, date_key, datetime):
    with pytest.raises((TypeError, ValueError)) as e:
        _ = get_date_from_dictionary(dictionary, date_key)
    assert str(e.value) == datetime

@pytest.mark.usefixtures("get_date_variables")
def test_get_date_from_dictionary(get_date_variables):
    expected_result = pd.to_datetime("2020-06-30")
    computed_result = get_date_from_dictionary(get_date_variables, "date_key")
    assert expected_result == computed_result


@pytest.mark.parametrize(
    "iterator, pe",
    [
        (None, "`iterator` must be a list or tuple"),
        ([-1, 1, None], "all elements in iterator must be numerical")
    ]
)
def test_handling_negative_vals_crash(iterator, pe):
    with pytest.raises(TypeError) as e:
        _ = handling_negative_vals(iterator)
    assert str(e.value) == pe

@pytest.mark.usefixtures("negative_vals_variables")
def test_handling_negative_vals(negative_vals_variables):
    expected_result = negative_vals_variables.get("iter_wo_negative_vals")
    computed_result = handling_negative_vals(negative_vals_variables.get("iter_w_negative_vals"))
    assert expected_result == computed_result

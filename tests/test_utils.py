import pytest
import numpy as np
from valuation.utils import get_key_from_iterator, compute_rate_of_change, compute_rates_of_change

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



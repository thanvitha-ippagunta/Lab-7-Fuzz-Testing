"""Property-based input validation tests for processor.py."""

import math

import pytest
from hypothesis import given, settings, strategies as st

from processor import calculate_average, normalize_username, parse_int_list


@settings(max_examples=250, deadline=None)
@given(st.text())
def test_parse_int_list_never_leaks_unexpected_exception(value):
    try:
        result = parse_int_list(value)
    except (TypeError, ValueError):
        return
    assert isinstance(result, list)
    assert all(type(item) is int for item in result)


@settings(max_examples=250, deadline=None)
@given(st.text())
def test_normalize_username_is_valid_or_rejected(value):
    try:
        result = normalize_username(value)
    except (TypeError, ValueError):
        return
    assert 1 <= len(result) <= 32
    assert result == result.lower()
    assert all(char.isalnum() or char in "-_" for char in result)


@settings(max_examples=250, deadline=None)
@given(st.lists(st.floats(allow_nan=False, allow_infinity=False, width=32), min_size=1, max_size=100))
def test_average_is_finite_and_within_input_bounds(values):
    result = calculate_average(values)
    assert math.isfinite(result)
    assert min(values) <= result <= max(values)


@settings(max_examples=200, deadline=None)
@given(st.one_of(st.none(), st.integers(), st.floats(), st.lists(st.one_of(st.text(), st.none()))))
def test_average_rejects_invalid_container_or_values(value):
    if isinstance(value, (list, tuple)) and value and all(
        isinstance(item, (int, float)) and not isinstance(item, bool) for item in value
    ):
        return
    with pytest.raises((TypeError, ValueError)):
        calculate_average(value)


def test_parse_integer_list_examples():
    assert parse_int_list(" 1, -2, 003 ") == [1, -2, 3]
    assert parse_int_list("  ") == []


def test_username_normalization_example():
    assert normalize_username("  Transit_User-7  ") == "transit_user-7"


def test_average_example():
    assert calculate_average([10, 20, 30]) == 20


@settings(max_examples=100, deadline=None)
@given(st.one_of(st.none(), st.integers(), st.floats(), st.lists(st.integers())))
def test_parse_int_list_rejects_non_string_inputs(value):
    with pytest.raises(TypeError):
        parse_int_list(value)


@settings(max_examples=100, deadline=None)
@given(st.one_of(st.none(), st.integers(), st.floats(), st.lists(st.integers())))
def test_normalize_username_rejects_non_string_inputs(value):
    with pytest.raises(TypeError):
        normalize_username(value)


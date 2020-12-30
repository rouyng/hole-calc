"""
Tests for the holecalc.py module

The tests here are designed to unit test the math equations used for hole/pin size calculations
"""

from .context import holecalc
from holecalc import holecalc
from decimal import Decimal, getcontext
import pytest
import random
import sys


def test_import():
    """Test whether module to be tested was successfully imported"""
    for i in sys.modules:
        print(i)
    assert "holecalc" in sys.modules


class TestCalculations:
    """Unit test the math functions"""
    def test_example_values_1(self):
        test_result = holecalc.calculate_hole_size("1", "2", "3")['result']
        assert str(test_result.quantize(Decimal("0.001"))) == "6.000"

    def test_example_values_2(self):
        test_result = holecalc.calculate_hole_size("5", "2", "8")['result']
        assert str(test_result.quantize(Decimal("0.001"))) == "24.375"

    def test_examples_values_3(self):
        test_result = holecalc.calculate_hole_size("0.113", "0.278", "0.156")['result']
        assert str(test_result.quantize(Decimal("0.001"))) == "0.440"

    def test_zero_input(self):
        assert holecalc.calculate_hole_size("0", "1", "2") == \
               {'result': None, 'error': 'Pin dimension cannot be zero'}

    def test_invalid_input(self):
        assert holecalc.calculate_hole_size("50", "1", "0.01") == \
               {'result': None, 'error': 'Cannot calculate hole dimension, check pin values'}

    def test_in_small_tolerances(self):
        for t, v in {"XX": "0.000020",
                     "X": "0.00004",
                     "Y": "0.00007",
                     "Z": "0.0001",
                     "ZZ": "0.0002"}.items():
            for _ in range(0, 20):
                test_dia = str(round(random.uniform(.0009, .8250), 4))
                pos_result = holecalc.pin_tolerance_limits(test_dia, t, True, units="in")
                assert pos_result == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))
                pos_result = holecalc.pin_tolerance_limits(test_dia, t, True, units="in")
                assert pos_result == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))

    def test_in_large_tolerances(self):
        for t, v in {"XX": "0.000100",
                     "X": "0.000200",
                     "Y": "0.000300",
                     "Z": "0.000400",
                     "ZZ": "0.000800"}.items():
            for _ in range(0, 20):
                test_dia = str(round(random.uniform(9.0101, 12.2600), 4))
                pos_result = holecalc.pin_tolerance_limits(test_dia, t, True, units="in")
                assert pos_result == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))
                pos_result = holecalc.pin_tolerance_limits(test_dia, t, True, units="in")
                assert pos_result == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))

    def test_mm_small_tolerances(self):
        for t, v in {"XX": "0.0005",
                     "X": "0.0010",
                     "Y": "0.0018",
                     "Z": "0.0025",
                     "ZZ": "0.0050"}.items():
            for _ in range(0, 20):
                test_dia = str(round(random.uniform(1.00, 21.00), 3))
                pos_result = holecalc.pin_tolerance_limits(test_dia, t, True, units="mm")
                assert pos_result == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))
                pos_result = holecalc.pin_tolerance_limits(test_dia, t, True, units="mm")
                assert pos_result == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))

    def test_mm_large_tolerances(self):
        for t, v in {"XX": "0.0025",
                     "X": "0.0051",
                     "Y": "0.0076",
                     "Z": "0.0100",
                     "ZZ": "0.0200"}.items():
            for _ in range(0, 20):
                test_dia = str(round(random.uniform(230.01, 300.00), 3))
                pos_result = holecalc.pin_tolerance_limits(test_dia, t, True, units="mm")
                assert pos_result == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))
                pos_result = holecalc.pin_tolerance_limits(test_dia, t, True, units="mm")
                assert pos_result == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))

    def test_invalid_tolerance_units(self):
        test_dia = str(round(random.uniform(0.0009, 12.26), 4))
        with pytest.raises(ValueError) as execinfo:
            holecalc.pin_tolerance_limits(test_dia, "X", True, units="garbage")
            assert "Invalid units" in str(execinfo)

    def test_invalid_tolerance_class(self):
        test_dia = str(round(random.uniform(0.0009, 12.26), 4))
        with pytest.raises(ValueError) as execinfo:
            holecalc.pin_tolerance_limits(test_dia, "YX", True, units="in")
            assert "Invalid tolerance class" in str(execinfo)

    def test_in_tolerance_bounds(self):
        test_dia = str(round(random.uniform(0.00005, 0.0008), 4))
        assert holecalc.pin_tolerance_limits(test_dia, "X", True, units="in") is None

    def test_mm_tolerance_bounds(self):
        test_dia = str(round(random.uniform(0.00005, 0.9999), 4))
        assert holecalc.pin_tolerance_limits(test_dia, "X", True, units="mm") is None

    def test_tolerance_hole_measurement_in(self):
        results = holecalc.calculate_hole_size_limits(
            ("1.000", "ZZ", True),
            ("2.000", "ZZ", True),
            ("3.000", "ZZ", True), "in")
        assert results[0]['error'] is None
        assert results[0]['error'] is None
        assert str(results[0]['result'].quantize(Decimal("0.0001"))) == "6.0000"
        assert str(results[1]['result'].quantize(Decimal("0.0001"))) == "6.0003"

    def test_tolerance_hole_measurement_mm(self):
        results = holecalc.calculate_hole_size_limits(
            ("1.00", "ZZ", True),
            ("2.00", "ZZ", True),
            ("3.00", "ZZ", True), "mm")
        assert results[0]['error'] is None
        assert results[0]['error'] is None
        assert str(results[0]['result'].quantize(Decimal("0.01"))) == "6.00"
        assert str(results[1]['result'].quantize(Decimal("0.01"))) == "6.00"

    def test_tolerance_hole_measurement_mm_2(self):
        results = holecalc.calculate_hole_size_limits(
            ("64.25", "Y", True),
            ("11.10", "Z", True),
            ("25.35", "ZZ", True), "mm")
        assert results[0]['error'] is None
        assert results[0]['error'] is None
        assert str(results[0]['result'].quantize(Decimal("0.001"))) == "240.219"
        assert str(results[1]['result'].quantize(Decimal("0.001"))) == "240.174"


class TestWrapper():
    """Unit test functions that wrap math functions"""

    def test_pin_size_wrapper_in(self):
        for t, v in {"XX": "0.000020",
                     "X": "0.00004",
                     "Y": "0.00007",
                     "Z": "0.0001",
                     "ZZ": "0.0002"}.items():
            for _ in range(0, 20):
                test_dia = str(round(random.uniform(.0009, .8250), 4))
                pos_result = holecalc.pin_size_wrapper(test_dia, t, True, "in")
                assert pos_result['result'] == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))
                pos_result = holecalc.pin_size_wrapper(test_dia, t, True, "in")
                assert pos_result['result'] == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))

    def test_pin_size_wrapper_mm(self):
        for t, v in {"XX": "0.0005",
                     "X": "0.0010",
                     "Y": "0.0018",
                     "Z": "0.0025",
                     "ZZ": "0.0050"}.items():
            for _ in range(0, 20):
                test_dia = str(round(random.uniform(1.00, 21.00), 3))
                pos_result = holecalc.pin_size_wrapper(test_dia, t, True, "mm")
                assert pos_result['result'] == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))
                pos_result = holecalc.pin_size_wrapper(test_dia, t, True, "mm")
                assert pos_result['result'] == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))

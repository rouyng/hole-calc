"""
Tests for the holecalc.py module

The tests here are designed to unit test the math equations used for hole/pin size calculations
"""


from holecalc import holecalc
from decimal import Decimal
import pytest
import random
import sys


def test_import():
    """Test whether module to be tested was successfully imported"""
    for i in sys.modules:
        print(i)
    assert "holecalc" in sys.modules


class TestHoleSizeCalculation:
    """Unit test the functions that calculate bore diameter from three pin diameters"""
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
        assert str(results[1]['result'].quantize(Decimal("0.001"))) == "240.173"


class TestPinTolerance:
    """Unit test functions that calculate gage pin tolerances"""

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
                test_dia = str(round(random.uniform(9.0101, 12.010), 4))
                pos_result = holecalc.pin_tolerance_limits(test_dia, t, True, units="in")
                assert pos_result == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))
                pos_result = holecalc.pin_tolerance_limits(test_dia, t, True, units="in")
                assert pos_result == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))

    def test_mm_small_tolerances(self):
        for t, v in {"XX": "0.00051",
                     "X": "0.00102",
                     "Y": "0.00178",
                     "Z": "0.00254",
                     "ZZ": "0.00508"}.items():
            for _ in range(0, 20):
                test_dia = str(round(random.uniform(0.254, 2.096), 3))
                pos_result = holecalc.pin_tolerance_limits(test_dia, t, True, units="mm")
                assert pos_result == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))
                pos_result = holecalc.pin_tolerance_limits(test_dia, t, True, units="mm")
                assert pos_result == (Decimal(test_dia), Decimal(test_dia) + Decimal(v))

    def test_mm_large_tolerances(self):
        for t, v in {"XX": "0.00254",
                     "X": "0.00508",
                     "Y": "0.00762",
                     "Z": "0.01016",
                     "ZZ": "0.02032"}.items():
            for _ in range(0, 20):
                test_dia = str(round(random.uniform(228.86, 305.05), 3))
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
        test_dia = str(round(random.uniform(0.00005, 0.0010), 4))
        assert holecalc.pin_tolerance_limits(test_dia, "X", True, units="in") is None

    def test_mm_tolerance_bounds(self):
        test_dia = str(round(random.uniform(0.00005, 0.254), 4))
        assert holecalc.pin_tolerance_limits(test_dia, "X", True, units="mm") is None

    # Test functions that wrap pin_tolerance_limits for gui use
    def test_pin_size_wrapper_in(self):
        for t, v in {"XX": "0.000020",
                     "X": "0.00004",
                     "Y": "0.00007",
                     "Z": "0.0001",
                     "ZZ": "0.0002"}.items():
            for _ in range(0, 20):
                test_dia = str(round(random.uniform(.0009, .8250), 4))
                pos_result = holecalc.pin_size_wrapper(test_dia, t, True, "in")
                desired_result = Decimal(test_dia) + Decimal(v)
                precision = Decimal("0.00001")
                assert pos_result['result'] == (Decimal(test_dia).quantize(precision),
                                                desired_result.quantize(precision))

    def test_pin_size_wrapper_mm(self):
        for t, v in {"XX": "0.00051",
                     "X": "0.00102",
                     "Y": "0.00178",
                     "Z": "0.00254",
                     "ZZ": "0.00508"}.items():
            for _ in range(0, 20):
                test_dia = str(round(random.uniform(1.00, 20.95), 3))
                pos_result = holecalc.pin_size_wrapper(test_dia, t, True, "mm")
                desired_result = Decimal(test_dia) + Decimal(v)
                precision = Decimal("0.00001")
                assert pos_result['result'] == (Decimal(test_dia).quantize(precision),
                                                desired_result.quantize(precision))


class TestReversePin:
    """Unit tests for the functions that calculate the third pin diameter from two pin diameters
    and a bore diameter."""

    def test_reverse_calculation_1(self):
        precision = Decimal("0.0001")
        test_result = holecalc.calculate_remaining_pin(bore_dia="6", pin1="1", pin2="2")
        assert test_result['result'].quantize(precision) == Decimal("3.0000")

    def test_reverse_calculation_2(self):
        precision = Decimal("0.0001")
        test_result = holecalc.calculate_remaining_pin(bore_dia="240.219",
                                                       pin1="64.25",
                                                       pin2="11.1")
        assert test_result['result'].quantize(precision) == Decimal("25.3500")

    def test_reverse_invalid_bore(self):
        test_result = holecalc.calculate_remaining_pin(bore_dia="2", pin1="3", pin2="1")
        assert test_result['result'] is None
        assert test_result['error'] == "Cannot calculate pin dimension, check pin/bore diameters"

    def test_reverse_negative_value(self):
        test_result = holecalc.calculate_remaining_pin(bore_dia="6", pin1="-3", pin2="1")
        assert test_result['result'] is None
        assert test_result['error'] == "Cannot calculate pin dimension, check pin/bore diameters"

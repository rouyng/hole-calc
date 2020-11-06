"""
Tests for the holecalc.py module

The tests here are designed to unit test the math equations used for hole/pin size calculations
"""

from .context import holecalc
from holecalc import holecalc
import sys


def test_import():
    """Test whether module to be tested was successfully imported"""
    for i in sys.modules:
        print(i)
    assert "holecalc" in sys.modules


class TestCalculations:
    """Tests mathematical accuracy of formulas"""
    def test_example_values_1(self):
        assert round(holecalc.calculate_hole_size(1, 2, 3)['result'], 3) == 6

    def test_example_values_2(self):
        assert round(holecalc.calculate_hole_size(5, 2, 8)['result'], 3) == 24.375

    def test_examples_values_3(self):
        assert round(holecalc.calculate_hole_size(0.113, 0.278, 0.156)['result'], 3) == 0.440

    def test_zero_input(self):
        assert holecalc.calculate_hole_size(0, 1, 2) == \
               {'result': None, 'error': 'Pin dimension cannot be zero'}

    def test_invalid_input(self):
        assert holecalc.calculate_hole_size(50, 1, 0.01) == \
               {'result': None, 'error': 'Cannot calculate hole dimension, check pin values'}

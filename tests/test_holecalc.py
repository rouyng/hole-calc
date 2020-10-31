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
    """Tests mathmatical accuracy of formulas"""
    def test_example_values_1(self):
        assert holecalc.calculate_hole_size(1, 2, 3) == 6

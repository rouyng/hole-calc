from math import sqrt
from decimal import Decimal, getcontext

# set precision for decimal math
getcontext().prec = 8


def calculate_hole_size(pin1: float, pin2: float, pin3: float):
    """From three known pin diameters, calculate diameter of hole they fit into

    This is an application of Descartes' Theorem, which states that for every four
    mutually tangent circles, the radii of the circles satisfy a certain quadratic equation
    """
    try:
        curvatures = [1/(d / 2) for d in (pin1, pin2, pin3)]  # determine curvatures for each pin
    except ZeroDivisionError:
        return {'result': None, 'error': 'Pin dimension cannot be zero'}

    hole_rad = 1 / (sum(curvatures) - 2 * sqrt(curvatures[0]*curvatures[1]
                                               + curvatures[1]*curvatures[2]
                                               + curvatures[0]*curvatures[2]))
    result = abs(hole_rad * 2)
    if any([result < d for d in (pin1, pin2, pin3)]):
        return {'result': None, 'error': 'Cannot calculate hole dimension, check pin values'}
    return {'result': result, 'error': None}


def pin_tolerance_limits(nominal: str, tol_class: str, is_plus: bool, units: str = "in"):
    """Return the minimum and maximum diameter of a gauge pin, given the nominal size in units,
    the tolerance class of the gauge, and whether it is a plus or minus pin.

    Tolerance class information from https://www.newmantools.com/meyer/pluggage_ABC.htm
    """
    # tolerance classes for gauge pins have upper and lower bounds, if nominal dimension is outside
    # these bounds, return None
    nominal_dia = Decimal(nominal)
    if units not in ("in", "mm"):
        raise ValueError(f"Invalid units specified: {units}")
    elif tol_class not in ('XX', 'X', 'Y', 'Z', 'ZZ'):
        raise ValueError(f"Invalid tolerance class specified: {tol_class}")
    elif (nominal_dia < Decimal(".0009") or nominal_dia > Decimal("12.2600")) and units == "in":
        return None
    elif (nominal_dia < Decimal("1.00") or nominal_dia > Decimal("300.00")) and units == "mm":
        return None
    tol_table_in = {
        "0.8250": {
            'XX': Decimal("0.00002"),
            'X': Decimal("0.000040"),
            'Y': Decimal("0.000070"),
            'Z': Decimal("0.000100"),
            'ZZ': Decimal("0.000200")
        },
        "1.5100": {
            'XX': Decimal("0.000030"),
            'X': Decimal("0.000060"),
            'Y': Decimal("0.000090"),
            'Z': Decimal("0.000120"),
            'ZZ': Decimal("0.000240")
        },

    }
    tol_table_mm = {
        "21.00": {
            'XX': Decimal("0.0005"),
            'X': Decimal("0.0010"),
            'Y': Decimal("0.0018"),
            'Z': Decimal("0.0025"),
            'ZZ': Decimal("0.0050")}
    }
    if units == "in":
        for r, t in tol_table_in.items():
            if nominal_dia < Decimal(r):
                tolerance = t[tol_class]
                break
    else:
        for r, t in tol_table_mm.items():
            if nominal_dia < Decimal(r):
                tolerance = t[tol_class]
                break
    if is_plus:
        tolerance_bounds = (nominal, nominal + tolerance)
    else:
        tolerance_bounds = (nominal - tolerance, nominal)
    return tolerance_bounds


def calculate_center_positions(pin1: float, pin2: float, pin3: float, hole_dia):
    """
    From three known tangent circle diameters (representing pins in a hole),
    calculate the x,y coordinates of each circle center relative to the center 0,0
    of the circumscribing circle with diameter of hole_dia.

    This function will eventually be used to draw the relative sizes and positions of the three
    pins within the hole being measured. Need to figure out the geometry first before I can
    complete it, though!
    """
    pass


def calculate_remaining_pin(hole_dia: float, pin1: float, pin2: float, ) -> float:
    """From two pin sizes calculate the required third pin diameter to gauge hole diameter"""
    pass

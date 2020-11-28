from decimal import Decimal, getcontext
import logging


# set precision for decimal math
getcontext().prec = 12
# set rounding method for decimal math
getcontext().rounding = "ROUND_HALF_UP"
# set logging level
logging.getLogger().setLevel(logging.INFO)


def calculate_hole_size(pin1: str, pin2: str, pin3: str):
    """From three known pin diameters, calculate diameter of hole they fit into

    This is an application of Descartes' Theorem, which states that for every four
    mutually tangent circles, the radii of the circles satisfy a certain quadratic equation
    :param pin1: String representing decimal size of first pin, ex: "1.000"
    :param pin2: String representing decimal size of first pin, ex: "2.000"
    :param pin3: String representing decimal size of first pin, ex: "3.000"
    :returns: Dictionary containing "result" and "error" entries. result contains a Decimal
    object or none if an error occurs, Error contains descriptive math error text (if applicable)
    """
    try:
        curvatures = [1/(Decimal(d) / 2) for d in (pin1, pin2, pin3)]  # determine curvatures
    except ZeroDivisionError:
        return {'result': None, 'error': 'Pin dimension cannot be zero'}

    hole_rad = 1 / (sum(curvatures) - 2 * (curvatures[0]*curvatures[1]
                                           + curvatures[1]*curvatures[2]
                                           + curvatures[0]*curvatures[2]).sqrt())
    result = abs(hole_rad * 2)
    if any([result < Decimal(d) for d in (pin1, pin2, pin3)]):
        return {'result': None, 'error': 'Cannot calculate hole dimension, check pin values'}
    return {'result': result, 'error': None}


def pin_tolerance_limits(nominal: str, tol_class: str, is_plus: bool, units: str = "in"):
    """Return the minimum and maximum diameter of a gauge pin, given the nominal size in units,
    the tolerance class of the gauge, and whether it is a plus or minus pin.

    Tolerance class information from https://www.newmantools.com/meyer/pluggage_ABC.htm
    """

    nominal_dia = Decimal(nominal)
    if units not in ("in", "mm"):
        raise ValueError(f"Invalid units specified: {units}")
    elif tol_class not in ('XX', 'X', 'Y', 'Z', 'ZZ'):
        raise ValueError(f"Invalid tolerance class specified: {tol_class}")
    # tolerance classes for gauge pins have upper and lower bounds, if nominal dimension is outside
    # these bounds, return None
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
        "2.5100": {
            'XX': Decimal("0.000040"),
            'X': Decimal("0.000080"),
            'Y': Decimal("0.000120"),
            'Z': Decimal("0.000160"),
            'ZZ': Decimal("0.000320")
        },
        "4.5100": {
            'XX': Decimal("0.000050"),
            'X': Decimal("0.000100"),
            'Y': Decimal("0.000150"),
            'Z': Decimal("0.000200"),
            'ZZ': Decimal("0.000400")
        },
        "6.5100": {
            'XX': Decimal("0.000065"),
            'X': Decimal("0.000130"),
            'Y': Decimal("0.000190"),
            'Z': Decimal("0.000250"),
            'ZZ': Decimal("0.000500")
        },
        "9.0100": {
            'XX': Decimal("0.000080"),
            'X': Decimal("0.000160"),
            'Y': Decimal("0.000240"),
            'Z': Decimal("0.000320"),
            'ZZ': Decimal("0.000640")
        },
        "12.2600": {
            'XX': Decimal("0.000100"),
            'X': Decimal("0.000200"),
            'Y': Decimal("0.000300"),
            'Z': Decimal("0.000400"),
            'ZZ': Decimal("0.000800")
        }
    }
    tol_table_mm = {
        "21.00": {
            'XX': Decimal("0.0005"),
            'X': Decimal("0.0010"),
            'Y': Decimal("0.0018"),
            'Z': Decimal("0.0025"),
            'ZZ': Decimal("0.0050")
        },
        "38.00": {
            'XX': Decimal("0.0008"),
            'X': Decimal("0.0015"),
            'Y': Decimal("0.0023"),
            'Z': Decimal("0.0030"),
            'ZZ': Decimal("0.0060")
        },
        "64.00": {
            'XX': Decimal("0.0010"),
            'X': Decimal("0.0020"),
            'Y': Decimal("0.0030"),
            'Z': Decimal("0.0040"),
            'ZZ': Decimal("0.0080")
        },
        "115.00": {
            'XX': Decimal("0.0013"),
            'X': Decimal("0.0025"),
            'Y': Decimal("0.0038"),
            'Z': Decimal("0.0050"),
            'ZZ': Decimal("0.0100")
        },
        "165.00": {
            'XX': Decimal("0.0017"),
            'X': Decimal("0.0033"),
            'Y': Decimal("0.0048"),
            'Z': Decimal("0.0060"),
            'ZZ': Decimal("0.0130")
        },
        "230.00": {
            'XX': Decimal("0.0020"),
            'X': Decimal("0.0041"),
            'Y': Decimal("0.0061"),
            'Z': Decimal("0.0080"),
            'ZZ': Decimal("0.0160")
        },
        "300.00": {
            'XX': Decimal("0.0025"),
            'X': Decimal("0.0051"),
            'Y': Decimal("0.0076"),
            'Z': Decimal("0.0100"),
            'ZZ': Decimal("0.0200")
        }
    }
    if units == "in":
        for r, t in tol_table_in.items():
            if nominal_dia <= Decimal(r):
                tolerance = t[tol_class]
                break
    else:
        for r, t in tol_table_mm.items():
            if nominal_dia <= Decimal(r):
                tolerance = t[tol_class]
                break
    if is_plus:
        tolerance_bounds = (nominal_dia, nominal_dia + tolerance)
    else:
        tolerance_bounds = (nominal_dia - tolerance, nominal_dia)
    return tolerance_bounds


def calculate_hole_size_limits(pin1: tuple, pin2: tuple, pin3: tuple, units: str):
    """
    Given nominal size and tolerance class of each pin, calculate the upper and lower limits
    of the measured hole.
    :param pin1: Tuple containing nominal size, tolerance class, and boolean for plus
    tolerance of pin1
    :param pin2: Same info for pin2
    :param pin3: Same info for pin2
    :param units: Str containing "in" or "mm", designating the units of measurement
    :return: Decimal minimum and maximum values of the hole measured by pins 1-3
    """
    pin1_limits = pin_tolerance_limits(pin1[0], pin1[1], pin1[2], units)
    pin2_limits = pin_tolerance_limits(pin2[0], pin2[1], pin2[2], units)
    pin3_limits = pin_tolerance_limits(pin3[0], pin3[1], pin3[2], units)
    if None in (pin1_limits, pin2_limits, pin3_limits):
        return {'result': None, 'error': 'Pin is beyond tolerance class limits'}, \
               {'result': None, 'error': 'Pin is beyond tolerance class limits'}
    min_hole = calculate_hole_size(pin1_limits[0], pin2_limits[0], pin3_limits[0])
    max_hole = calculate_hole_size(pin1_limits[1], pin2_limits[1], pin3_limits[1])
    return min_hole, max_hole


def calculate_center_positions(pin1: float, pin2: float, pin3: float, hole_dia):
    """
    From three known tangent circle diameters (representing pins in a hole),
    calculate the x,y coordinates of each circle center relative to the center 0,0
    of the circumscribing circle with diameter of hole_dia.

    This function will eventually be used to draw the relative sizes and positions of the three
    pins within the hole being measured. Need to figure out the geometry first before I can
    complete it, though!
    """
    # placeholder for planned functionality
    pass


def calculate_remaining_pin(hole_dia: float, pin1: float, pin2: float, ) -> float:
    """From two pin sizes calculate the required third pin diameter to gauge hole diameter"""
    # placeholder for planned functionality
    pass

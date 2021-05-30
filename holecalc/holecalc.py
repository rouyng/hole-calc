"""Module containing functions used for math needed in hole calc, including descartes theorem and
 other functions that wrap the descartes theorem calculation for different purposes"""

from decimal import Decimal, getcontext, InvalidOperation
import logging
from math import acos, cos, radians, degrees, sqrt

# set precision for decimal math
getcontext().prec = 12
# set rounding method for decimal math
getcontext().rounding = "ROUND_HALF_UP"
# set logging level
logging.getLogger().setLevel(logging.INFO)


def descartes(k1: Decimal, k2: Decimal, k3: Decimal) -> Decimal:
    """Implementation of Descartes theorem, which states that for every four
    mutually tangent circles, the radii of the circles satisfy a certain quadratic equation.
    The curvature parameters used in this value are calculated as k = ±1/r, where r == circle radius

    For more mathematical details, see https://en.wikipedia.org/wiki/Descartes%27_theorem

    :param k1: Decimal object representing curvature of circle 1
    :param k2: Decimal object representing curvature of circle 2
    :param k3: Decimal object representing curvature of circle 3
    :returns: Decimal object representing diameter of circle 4, which is mutually tangent to circles
    1, 2 and 3.
    """
    radius = 1 / (sum((k1, k2, k3)) - 2 * (k1 * k2 + k2 * k3 + k1 * k3).sqrt())
    logging.debug(f"Descartes radius: {radius}")
    return radius * 2


def calculate_hole_size(pin1: str, pin2: str, pin3: str) -> dict:
    """From three known pin diameters, calculate diameter of hole they fit into using
    Descartes' Theorem. Exceptions raised by math errors are caught and passed to gui functions as
    descriptive text.

    :param pin1: String representing decimal diameter of first pin, ex: "1.000"
    :param pin2: String representing decimal diameter of second pin, ex: "2.000"
    :param pin3: String representing decimal diameter of third pin, ex: "3.000"
    :returns: Dictionary containing "result" and "error" keys. result value is a Decimal
    object representing the diameter of the bore. If an error occurs, error value is
    descriptive math error text.
    """
    try:
        curvatures = [1 / (Decimal(d) / 2) for d in (pin1, pin2, pin3)]  # determine curvatures
        result = descartes(curvatures[0], curvatures[1], curvatures[2])
    except ZeroDivisionError as e:
        # no pin diameter should be zero, if that occurs ZeroDivisionError is raised
        logging.debug(str(e))
        logging.info("Zero division error")
        return {'result': None, 'error': 'Cannot calculate hole dimension, check pin values'}
    except InvalidOperation as e:
        # if something that the decimal library can't understand as a number is passed, this
        # exception is raised
        logging.debug(str(e))
        return {'result': None, 'error': 'Cannot calculate hole dimension, check pin values'}
    if result >= 0:
        logging.debug(f"Descartes theorem returned a positive value for {(pin1, pin2, pin3)}")
        return {'result': None, 'error': 'Cannot calculate hole dimension, check pin values'}
    return {'result': abs(result), 'error': None}


def pin_tolerance_limits(nominal: str, tol_class: str, is_plus: bool, units: str = "in"):
    """Return the minimum and maximum diameter of a gauge pin, given the nominal size in units,
    the tolerance class of the gauge, and whether it is a plus or minus pin.

    Tolerance class information from ASME B89.1.5-1998
    """
    logging.debug(f"Calculating pin tolerance bounds: {nominal} dia, "
                  f"{tol_class} class, positive {is_plus}, units {units}")
    nominal_dia = Decimal(nominal)
    if units not in ("in", "mm"):
        raise ValueError(f"Invalid units specified: {units}")
    elif tol_class not in ('XX', 'X', 'Y', 'Z', 'ZZ'):
        raise ValueError(f"Invalid tolerance class specified: {tol_class}")
    # tolerance classes for gauge pins have upper and lower bounds, if nominal dimension is outside
    # these bounds, return None
    elif (nominal_dia <= Decimal(".0010") or nominal_dia > Decimal("21.010")) and units == "in":
        # TODO: refactor pin_tolerance_limits() so out-of-range generate descriptive exceptions
        return None
    elif (nominal_dia <= Decimal("0.254") or nominal_dia > Decimal("533.65")) and units == "mm":
        return None
    tol_table_in = {
        "0.825": {
            'XX': Decimal("0.000020"),
            'X': Decimal("0.000040"),
            'Y': Decimal("0.000070"),
            'Z': Decimal("0.000100"),
            'ZZ': Decimal("0.000200")
        },
        "1.510": {
            'XX': Decimal("0.000030"),
            'X': Decimal("0.000060"),
            'Y': Decimal("0.000090"),
            'Z': Decimal("0.000120"),
            'ZZ': Decimal("0.000240")
        },
        "2.510": {
            'XX': Decimal("0.000040"),
            'X': Decimal("0.000080"),
            'Y': Decimal("0.000120"),
            'Z': Decimal("0.000160"),
            'ZZ': Decimal("0.000320")
        },
        "4.510": {
            'XX': Decimal("0.000050"),
            'X': Decimal("0.000100"),
            'Y': Decimal("0.000150"),
            'Z': Decimal("0.000200"),
            'ZZ': Decimal("0.000400")
        },
        "6.510": {
            'XX': Decimal("0.000065"),
            'X': Decimal("0.000130"),
            'Y': Decimal("0.000190"),
            'Z': Decimal("0.000250"),
            'ZZ': Decimal("0.000500")
        },
        "9.010": {
            'XX': Decimal("0.000080"),
            'X': Decimal("0.000160"),
            'Y': Decimal("0.000240"),
            'Z': Decimal("0.000320"),
            'ZZ': Decimal("0.000640")
        },
        "12.010": {
            'XX': Decimal("0.000100"),
            'X': Decimal("0.000200"),
            'Y': Decimal("0.000300"),
            'Z': Decimal("0.000400"),
            'ZZ': Decimal("0.000800")
        },
        "15.010": {
            'XX': Decimal("0.000150"),
            'X': Decimal("0.000300"),
            'Y': Decimal("0.000450"),
            'Z': Decimal("0.000600"),
            'ZZ': Decimal("0.001200")
        },
        "18.010": {
            'XX': Decimal("0.000200"),
            'X': Decimal("0.000400"),
            'Y': Decimal("0.000600"),
            'Z': Decimal("0.000800"),
            'ZZ': Decimal("0.001600")
        },
        "21.010": {
            'XX': Decimal("0.000250"),
            'X': Decimal("0.000500"),
            'Y': Decimal("0.000750"),
            'Z': Decimal("0.001000"),
            'ZZ': Decimal("0.002000")
        }
    }
    tol_table_mm = {
        "20.96": {
            'XX': Decimal("0.00051"),
            'X': Decimal("0.00102"),
            'Y': Decimal("0.00178"),
            'Z': Decimal("0.00254"),
            'ZZ': Decimal("0.00508")
        },
        "38.35": {
            'XX': Decimal("0.00076"),
            'X': Decimal("0.00152"),
            'Y': Decimal("0.00229"),
            'Z': Decimal("0.00305"),
            'ZZ': Decimal("0.00610")
        },
        "63.75": {
            'XX': Decimal("0.00102"),
            'X': Decimal("0.00203"),
            'Y': Decimal("0.00305"),
            'Z': Decimal("0.00406"),
            'ZZ': Decimal("0.00813")
        },
        "114.55": {
            'XX': Decimal("0.00127"),
            'X': Decimal("0.00254"),
            'Y': Decimal("0.00381"),
            'Z': Decimal("0.00508"),
            'ZZ': Decimal("0.01016")
        },
        "165.35": {
            'XX': Decimal("0.00165"),
            'X': Decimal("0.00330"),
            'Y': Decimal("0.00483"),
            'Z': Decimal("0.00635"),
            'ZZ': Decimal("0.01270")
        },
        "228.85": {
            'XX': Decimal("0.00203"),
            'X': Decimal("0.00406"),
            'Y': Decimal("0.00610"),
            'Z': Decimal("0.00813"),
            'ZZ': Decimal("0.01626")
        },
        "305.05": {
            'XX': Decimal("0.00254"),
            'X': Decimal("0.00508"),
            'Y': Decimal("0.00762"),
            'Z': Decimal("0.01016"),
            'ZZ': Decimal("0.02032")
        },
        "381.25": {
            'XX': Decimal("0.00381"),
            'X': Decimal("0.00762"),
            'Y': Decimal("0.01143"),
            'Z': Decimal("0.01524"),
            'ZZ': Decimal("0.03048")
        },
        "457.45": {
            'XX': Decimal("0.00508"),
            'X': Decimal("0.01016"),
            'Y': Decimal("0.01524"),
            'Z': Decimal("0.02032"),
            'ZZ': Decimal("0.04064")
        },
        "533.65": {
            'XX': Decimal("0.00635"),
            'X': Decimal("0.01270"),
            'Y': Decimal("0.01905"),
            'Z': Decimal("0.02540"),
            'ZZ': Decimal("0.05080")
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
    logging.debug(f"Calculated pin tolerance bounds: {tolerance_bounds}")
    return tolerance_bounds


def pin_size_wrapper(w_nominal: str, w_tol_class: str, w_is_plus: bool, w_units: str = "in"):
    """wrap pin_tolerance_limits() with error handling for use in web gui"""
    try:
        result = pin_tolerance_limits(w_nominal, w_tol_class, w_is_plus, w_units)
    except ValueError as e:
        logging.warning(f"ValueError when calculating pin tolerance limits: {str(e)}")
        return {'result': None, 'error': str(e)}
    if result is None:
        logging.debug(f"{w_nominal} out of class tolerance class range, "
                      f"could not calculate diameter")
        return {'result': None, 'error': 'Diameter not within tolerance class limits'}
    return {'result': result, 'error': None}


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
    logging.debug("Attempting to calculate hole size limits")
    pin1_limits = pin_tolerance_limits(pin1[0], pin1[1], pin1[2], units)
    pin2_limits = pin_tolerance_limits(pin2[0], pin2[1], pin2[2], units)
    pin3_limits = pin_tolerance_limits(pin3[0], pin3[1], pin3[2], units)
    if None in (pin1_limits, pin2_limits, pin3_limits):
        logging.debug(f"Calculating hole size limits failed due to pins out of class range")
        return {'result': None, 'error': 'Diameter over tolerance class limit, use nominal mode'}, \
               {'result': None, 'error': 'Diameter over tolerance class limit, use nominal mode'}
    min_hole = calculate_hole_size(pin1_limits[0], pin2_limits[0], pin3_limits[0])
    max_hole = calculate_hole_size(pin1_limits[1], pin2_limits[1], pin3_limits[1])
    logging.debug(f"Calculated hole size limits, min: {min_hole} max: {max_hole}")
    return min_hole, max_hole


def calculate_center_positions(pin1: float, pin2: float, pin3: float) -> tuple:
    """
    From three known tangent circle diameters (representing pins in a hole),
    calculate the x,y coordinates of each circle center relative to the center 0,0
    of the circumscribing circle with diameter of hole_dia.

    The code used to calculate the circle positions is based on that used in Ludger Sandig's
    apollon, see https://github.com/lsandig/apollon/blob/master/apollon.py. Thanks to Ludger.
    """

    class Circle(object):
        """
        A circle represented by center point coordinates and radius.
        """

        def __init__(self, mx, my, r):
            """
            @param mx: x center coordinate
            @type mx: int or float
            @param my: y center coordinate
            @type my: int or float
            @param r: radius
            @type r: int or float
            """
            self.r = r  # radius
            self.x = mx  # center x position
            self.y = my  # center y position
            self.k = 1 / r  # circle curvature
            self.m = (mx + my * 1j)  # complex number representing the center point

    # calculate pin radii
    r1 = pin1 / 2
    r2 = pin2 / 2
    r3 = pin3 / 2

    # create Circle instances based on the three pins
    circle1 = Circle(0, 0, r1)
    circle2 = Circle(r1 + r2, 0, r2)
    m3x = (r1 * r1 + r1 * r3 + r1 * r2 - r2 * r3) / (r1 + r2)
    m3y = sqrt((r1 + r3) * (r1 + r3) - m3x * m3x)
    circle3 = Circle(m3x, m3y, r3)
    cur1 = circle1.k
    cur2 = circle2.k
    cur3 = circle3.k
    m1 = circle1.m
    m2 = circle2.m
    m3 = circle3.m
    # calculate radius and position of enclosing circle and create Circle instance
    cur4 = -2 * sqrt(cur1 * cur2 + cur2 * cur3 + cur1 * cur3) + cur1 + cur2 + cur3
    m4 = (-2 * sqrt(cur1 * m1 * cur2 * m2 + cur2 * m2 * cur3 * m3 + cur1 * m1 * cur3 * m3)
          + cur1 * m1 + cur2 * m2 + cur3 * m3) / cur4
    circle4 = Circle(m4.real, m4.imag, abs(1 / cur4))

    # Transform circle coordinates so enclosing_circle center is at the x,y origin and
    # all dimensions/coordinates are on a scale of 0-1 where the maximum value of 1 is
    # scaled to the radius of the outer circle
    outer_radius = circle4.r
    scale_factor = 1 / outer_radius
    x1 = ((circle1.x - circle4.x) * scale_factor).real
    y1 = ((circle1.y - circle4.y) * scale_factor).real
    x2 = ((circle2.x - circle4.x) * scale_factor).real
    y2 = ((circle2.y - circle4.y) * scale_factor).real
    x3 = ((circle3.x - circle4.x) * scale_factor).real
    y3 = ((circle3.y - circle4.y) * scale_factor).real

    return (x1, y1), (x2, y2), (x3, y3)


def calculate_remaining_pin(bore_dia: str, pin1: str, pin2: str, ) -> dict:
    """From two pin sizes calculate the required third pin diameter to gauge hole diameter, using
    Descartes' Theorem. Exceptions raised by math errors are caught and passed to gui functions as
    descriptive text.

    Mathematically, it uses the Descartes theorem as in calculate_hole_size(), with one of the
    "pin" values flipped to a negative sign to represent the enclosing tangent circle (bore dia)

    :param bore_dia: String representing decimal diameter of bore, ex: "6.000"
    :param pin1: String representing decimal diameter of first pin, ex: "2.000"
    :param pin2: String representing decimal diameter of second pin, ex: "3.000"
    :returns: Dictionary containing "result" and "error" keys. result value is a Decimal
    object representing the diameter of the remaining pin. If an error occurs, error value is
    descriptive math error text.
    """

    try:
        neg_bore_dia = -1 * Decimal(bore_dia)
        curvatures = [1 / (Decimal(d) / 2) for d in
                      (pin1, pin2, neg_bore_dia)]  # determine curvatures
        result = descartes(curvatures[0], curvatures[1], curvatures[2])
    except ZeroDivisionError as e:
        # no pin diameter should be zero, if that occurs ZeroDivisionError is raised
        logging.debug(str(e))
        return {'result': None, 'error': 'Pin or bore dimension cannot be zero'}
    except InvalidOperation as e:
        # if something that the decimal library can't understand as a number is passed, this
        # exception is raised
        logging.debug(str(e))
        return {'result': None, 'error': 'Cannot calculate pin dimension, check pin/bore diameters'}
    if result < 0:
        logging.debug(f"Descartes theorem returned a positive value for {(pin1, pin2, bore_dia)}")
        return {'result': None, 'error': 'Cannot calculate pin dimension, check pin/bore diameters'}
    return {'result': result, 'error': None}

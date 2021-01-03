from decimal import Decimal, getcontext
import logging


# set precision for decimal math
getcontext().prec = 12
# set rounding method for decimal math
getcontext().rounding = "ROUND_HALF_UP"
# set logging level
logging.getLogger().setLevel(logging.INFO)


def calculate_hole_size(pin1: str, pin2: str, pin3: str) -> dict:
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

    Tolerance class information from ASME B89.1.5-1998
    """
    logging.info(f"Calculating pin tolerance bounds: {nominal} dia, "
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
    logging.info(f"Calculated pin tolerance bounds: {tolerance_bounds}")
    return tolerance_bounds


def pin_size_wrapper(w_nominal: str, w_tol_class: str, w_is_plus: bool, w_units: str = "in"):
    """wrap pin_tolerance_limits() with error handling for use in web gui"""
    try:
        result = pin_tolerance_limits(w_nominal, w_tol_class, w_is_plus, w_units)
    except ValueError as e:
        return {'result': None, 'error': str(e)}
    if result is None:
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
    pin1_limits = pin_tolerance_limits(pin1[0], pin1[1], pin1[2], units)
    pin2_limits = pin_tolerance_limits(pin2[0], pin2[1], pin2[2], units)
    pin3_limits = pin_tolerance_limits(pin3[0], pin3[1], pin3[2], units)
    if None in (pin1_limits, pin2_limits, pin3_limits):
        return {'result': None, 'error': 'Diameter over tolerance class limit, use nominal mode'}, \
               {'result': None, 'error': 'Diameter over tolerance class limit, use nominal mode'}
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


def calculate_remaining_pin(hole_dia: str, pin1: str, pin2: str, ) -> dict:
    """From two pin sizes calculate the required third pin diameter to gauge hole diameter.
    This function is used for the reverse calculator in the web gui.

    Mathematically, it uses the Descartes theorem as in calculate_hole_size(), with one of the
    "pin" values flipped to a negative sign to represent the enclosing tangent circle (bore dia)"""
    bore_dia = -1 * Decimal(hole_dia)
    return calculate_hole_size(bore_dia, pin1, pin2)


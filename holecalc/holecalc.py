from math import sqrt


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
    return {'result': abs(hole_rad * 2), 'error': None}


def pin_tolerance_limits(nominal: float, tol_class: str, is_plus: bool):
    """Return the minimum and maximum diameter of a gauge pin, given the nominal size,
    the tolerance class of the gauge, and whether it is a plus or minus pin.

    Tolerance class information from https://www.newmantools.com/meyer/pluggage_ABC.htm
    """
    pass



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

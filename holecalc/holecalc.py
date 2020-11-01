from math import sqrt


def calculate_hole_size(pin1: float, pin2: float, pin3: float):
    """From three known pin diameters, calculate diameter of hole they fit into

    This is an application of Descartes' Theorem, which states that for every four
    mutually tangent circles, the radii of the circles satisfy a certain quadratic equation
    """
    try:
        curvatures = [1/(d / 2) for d in (pin1, pin2, pin3)]  # determine curvatures for each pin
    except ZeroDivisionError:
        return None

    hole_rad = 1 / (sum(curvatures) - 2 * sqrt(curvatures[0]*curvatures[1]
                                               + curvatures[1]*curvatures[2]
                                               + curvatures[0]*curvatures[2]))
    result = abs(hole_rad * 2)
    if any([result < d for d in (pin1, pin2, pin3)]):
        return None
    return abs(hole_rad * 2)


def calculate_center_positions(pin1: float, pin2: float, pin3: float, hole_dia):
    """
    From three known tangent circle diameters (representing pins in a hole),
    calculate the x,y coordinates of each circle center relative to the center 0,0
    of the circumscribing circle with diameter of hole_dia
    """
    pass


def calculate_remaining_pin(hole_dia: float, pin1: float, pin2: float, ) -> float:
    """From two pin sizes calculate the required third pin diameter to gauge hole diameter"""
    pass

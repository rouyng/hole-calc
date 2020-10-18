from math import sqrt


def calculate_hole_size(pin1: float, pin2: float, pin3: float):
    """From three known pin f"""
    def radius(dia):
        return dia / 2

    prod_of_rads = radius(pin1) * radius(pin2) * radius(pin3)
    sum_of_rads = sum([radius(pin1), radius(pin2), radius(pin3)])
    hole_dia = 2 * (prod_of_rads / (2 * sqrt(prod_of_rads * sum_of_rads) -
                                    ((radius(pin1) * radius(pin2)) +
                                     (radius(pin2) * radius(pin3)) +
                                     (radius(pin1) * radius(pin3)))))
    return hole_dia


def calculate_remaining_pin(hole_dia: float, pin1: float, pin2: float, ) -> float:
    """From two pin sizes calculate the required third pin diameter to gauge hole diameter"""
    pass

from math import sqrt


def calculate_hole(pin1, pin2, pin3):
    def radius(dia):
        return dia / 2

    prod_of_rads = radius(pin1) * radius(pin2) * radius(pin3)
    sum_of_rads = sum([radius(pin1), radius(pin2), radius(pin3)])
    hole_dia = 2 * (prod_of_rads / (2 * sqrt(prod_of_rads * sum_of_rads) - (
                (radius(pin1) * radius(pin2)) + (radius(pin2) * radius(pin3)) + (radius(pin1) * radius(pin3)))))
    return hole_dia

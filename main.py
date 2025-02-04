import math
import numpy
from rich import print

import chronology
from draw import Draw

DEGREES = "\u00B0"
THETA = "\u0398"
ORIGIN = (10, 10)


def get_latitude() -> float:
    """Get user-input of latitude to use to calculate angles

    Returns:
        float: The provided latitude, in radians
    """
    l = float(
        input(
            "\nPlease enter the latitude for which you would like to receive calculations (must be decimal format): \n"
        )
    )
    latitude = math.radians(l)  # must convert to radians before calculations
    print(f"\nLatitude: {l}{DEGREES}\n")
    return latitude


if __name__ == "__main__":
    template = Draw(ORIGIN, 15)
    template.create_circle()
    template.draw_equatorial()
    template.draw_meridian()
    list_of_angles = []
    latitude = get_latitude()
    chronometer = chronology.Chronos(latitude)
    for time in chronometer.times:
        round_time = chronometer.get_round_time(time)
        formatted_time = chronometer.format_time(round_time)
        tan_theta = chronometer.calculate_tan_theta(time, chronometer.latitude)
        result = max(-90, min(90, round(tan_theta, 2)))
        entry = str(f"{formatted_time} = {result}{DEGREES}")
        print(entry)
        list_of_angles.append(result)
    template.hour_line(list_of_angles)
    template.label_latitude(numpy.rad2deg(latitude))
    with open("angles.txt", "a") as f:
        for angle in list_of_angles:
            f.write(str(angle))
    eot_correction = chronometer.get_data_table()
    print(eot_correction)
    template.draw()

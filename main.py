from rich import print

import chronology
from draw import Draw

DEGREES = "\u00B0"
THETA = "\u0398"
ORIGIN = (10, 10)


def get_coordinates():
    coords = input(
        "Enter latitude and longitude for desired sundial location (decimal format): \n"
    )
    lat, long = coords.split(" ")
    latitude = float(lat.strip(","))
    longitude = float(long)
    return (latitude, longitude)


def draw(latitude, angle_list):
    template = Draw(ORIGIN, 15)
    template.create_circle()
    template.draw_equatorial()
    template.draw_meridian()
    template.create_circle()
    template.draw_equatorial()
    template.hour_line(angle_list)
    template.label_latitude(round(latitude, 2))
    template.draw()
    return


def calculate(latitude, longitude):
    angle_list = []
    fmt_angle_list = []
    chronos = chronology.Chronos(latitude, longitude)
    sundial_tz = chronos.get_timezone()
    utc_offset = chronos.get_utc_offset(sundial_tz)
    central_meridian = chronos.find_central_meridian(utc_offset)
    # TODO: dial_tilt = chronos.calculate_dial_tilt(central_meridian)
    # TODO: dial_rotation = chronos.calculate_dial_rotation(central_meridian)
    for time in chronos.times:
        round_time = chronos.get_round_time(time)
        formatted_time = chronos.format_time(round_time)
        tan_theta = chronos.calculate_tan_theta(time, chronos.latitude)
        result = max(-90, min(90, round(tan_theta, 2)))
        fmt_result = str(f"{formatted_time} = {result}{DEGREES}")
        angle_list.append(result)
        fmt_angle_list.append(fmt_result)
    data_table = chronos.get_data_table()
    return fmt_angle_list, angle_list, data_table


if __name__ == "__main__":
    latitude, longitude = get_coordinates()
    formatted_angle_list, angle_list, data_table = calculate(latitude, longitude)
    draw(latitude, angle_list)
    eot_correction = data_table
    print(eot_correction)
    print(latitude, longitude)
    for item in formatted_angle_list:
        print(item)

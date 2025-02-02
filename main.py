import datetime
import math
from typing import Tuple
from rich import print

π = math.pi
DEGREES = "\u00B0"
THETA = "\u0398"
TIMES = list(range(-6, 7))


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


def get_hour_angle(time: int) -> float:
    """Determine the Hour Angle (+/- noon)

    Args:
        time (int): Number of hours before or after noon (meridian)

    Returns:
        float: Hour angle in radians
    """
    hour_angle_degrees = time * 15
    hour_angle = math.radians(
        hour_angle_degrees
    )  # must convert to radians before calculations
    return hour_angle


def get_rough_time(time: int) -> int:
    """Get 'rough' time in 24-hour format

    Args:
        time (int): Given time +/- noon, in hours

    Returns:
        int: Hour-only representation of given time
    """
    rough_time = 12 + time
    return rough_time


def format_time(hour: int, minute=0) -> str:
    """Format time for human-readable output

    Args:
        hour (int): Rough time (hour-only portion of time)
        minute (int, optional): Minutes past the hour. Defaults to 0.

    Returns:
        str: String-formatted time [HH:MM]
    """
    time_object = datetime.time(hour, minute)
    formatted_time = time_object.strftime("%H:%M")
    return formatted_time


def get_hour_line(time: int, latitude: float) -> float:
    """Calculate the various angles from the meridian for sundial

    Args:
        time (int): The particular hour (+/- hours from meridian) to calculate the angle for
        latitude (float): The provided latitude to calculate angles for, in radians

    Returns:
        float: tan(Θ) = tan(HA) * sin(lat)
    """
    # tan(θ) = tan(hour_angle) * sin(latitude)
    hour_angle = get_hour_angle(time)
    tan_hour_angle = math.tan(hour_angle)
    sin_latitude = math.sin(latitude)
    tan_theta = tan_hour_angle * sin_latitude
    result = math.degrees(math.atan(tan_theta))
    return result


def get_day_of_year() -> int:
    """Determine the numerical day of the year (DOY)

    Returns:
        int: The day of the year (DOY)
    """
    day_of_year = datetime.date.today().timetuple().tm_yday
    return day_of_year


def equation_of_time(day_of_year: int) -> float:
    """Calculate the Equation of Time to account for the eccentricities of the Earth and return number of minutes to add/subtract from readings for that day

    Args:
        day_of_year (int): Current day of the year (DOY)

    Returns:
        float: Number of minutes to add/subtract from today's readings
    """
    # Δt = 9.873*sin(4π/365.242(n-81))-7.655*sin(2π/365.242(n-1))
    n = day_of_year
    eot1 = 9.873 * math.sin((4 * π) / 365.242 * (n - 81))
    eot2 = 7.655 * math.sin((2 * π) / 365.242 * (n - 1))
    eot = eot1 - eot2
    return eot


def get_eot() -> Tuple[int, float]:
    """Calculate the Equation of Time (EoT) and Day of the Year (DOY) for today and return a tuple containing both

    Returns:
        Tuple[int, float]: Day of the year (DOY), Equation of Time (EoT)
    """
    day_of_year = get_day_of_year()
    eot = equation_of_time(day_of_year)
    return day_of_year, eot


if __name__ == "__main__":
    latitude = get_latitude()
    day_of_year, eot = get_eot()
    for time in TIMES:
        rough_time = get_rough_time(time)
        formatted_time = format_time(rough_time, 0)
        tan_theta = get_hour_line(time, latitude)
        result = max(
            -90, min(90, round(tan_theta, 2))
        )  # ensure the resultant angles are between -90 and 90 degrees
        print(f"{formatted_time} = {result}{DEGREES}")
    print(f"\nToday is day number {day_of_year}.")
    if eot > 0:
        print(
            f"Please subtract {abs(eot):.2f} minutes from your sundial readings today!\n"
        )
    elif eot < 0:
        print(f"Please add {abs(eot):.2f} minutes to your sundial readings today!\n")
    else:
        raise Exception("Honestly I don't even think this is possible...")

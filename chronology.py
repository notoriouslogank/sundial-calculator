import datetime
import math

import numpy
import pytz
import timezonefinder

π = math.pi


class Chronos:

    times = list(range(-6, 7))
    doy = datetime.datetime.today().timetuple().tm_yday

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def get_timezone(self) -> str:
        """Determine sundial timezone.

        Returns:
            str: Sundial's timezone name
        """
        tf = timezonefinder.TimezoneFinder()
        timezone = tf.timezone_at(lng=self.longitude, lat=self.latitude)
        return timezone

    def get_utc_offset(self, timezone: str) -> float:
        """Calculate sundial's offset from UTC

        Args:
            timezone (str): Timezone of sundial

        Returns:
            float: Offset from UTC
        """
        local_tz = pytz.timezone(timezone)
        utc_offset = local_tz.utcoffset(datetime.datetime.now()).total_seconds() / 3600
        return utc_offset

    def find_central_meridian(self, utc_offset: float) -> float:
        """Calculate the central meridian for the sundial's timezone

        Args:
            utc_offset (float): UTC offset for sundial's timezone

        Returns:
            float: Location of central meridian, in degrees
        """
        central_meridian = utc_offset * 15
        return central_meridian

    def calculate_dial_tilt(self, central_meridian: float) -> float:
        """Calculate amount of tilt to zero sundial to central meridian

        Args:
            central_meridian (float): Location of central meridian for sundial's timezone in degrees

        Returns:
            float: Amount to tilt sundial in degrees
        """
        tilt_rad = math.sin(
            numpy.deg2rad(self.longitude) - numpy.deg2rad(central_meridian)
        ) * math.cos(numpy.deg2rad(self.latitude))
        tilt = numpy.rad2deg(tilt_rad)
        return round(float(tilt), 2)

    def calculate_dial_rotation(self, central_meridian: float) -> float:
        """Calculate amount to rotate sundial face to zero out difference from central meridian

        Args:
            central_meridian (float): Location of central meridian for sundial's timezone, in degrees

        Returns:
            float: Amount to rotate sundial, in degrees
        """
        rotation_rad = math.sin(
            numpy.deg2rad(self.longitude) - numpy.deg2rad(central_meridian)
        ) * math.sin(self.latitude)
        rotation = numpy.rad2deg(rotation_rad)
        return round(float(rotation), 2)

    def get_hour_angle(self, time: int) -> float:
        """Convert angle from degrees to radians for easier calculations.

        Args:
            time (int): Number of hours above or below meridian

        Returns:
            float: Angle of hour, in radians
        """
        hour_angle = math.radians(time * 15)
        return hour_angle

    def get_round_time(self, time: int) -> int:
        """Convert the hour +/- into human-readable integer format

        Args:
            time (int): Number of hours above or below meridian

        Returns:
            int: Human-readable 12-hour time as integer
        """
        round_time = 12 + time
        return round_time

    def format_time(self, hour: int) -> str:
        """Format time into 12-hour time string

        Args:
            hour (int): Number of hours above or below meridian

        Returns:
            str: Time as 12-hour formatted string
        """
        raw_time = datetime.time(hour, 0)
        formatted_time = raw_time.strftime("%H:%M")
        return formatted_time

    def calculate_tan_theta(self, time: int, latitude: float) -> float:
        """Use provided latitude and time to calculate angles of hourly demarcations

        Args:
            time (int): Number of hours before or after meridian
            latitude (float): Latitude the sundial will be calibrated for use on

        Returns:
            float: Angle of intersection between hour demarcation and equator
        """
        hour_angle = self.get_hour_angle(time)
        tan_hour_angle = math.tan(hour_angle)
        sin_latitude = math.sin(latitude)
        tan_theta = tan_hour_angle * sin_latitude
        result = math.degrees(math.atan(tan_theta))
        return result

    def equation_of_time(self) -> float:
        """Calculate equation of time to determine how much time should be adjusted for readings based on the day of the year

        Returns:
            float: Equation of Time
        """
        eot1 = 9.873 * math.sin((4 * π) / 365.242 * (self.doy - 81))
        eot2 = 7.655 * math.sin((2 * π) / 365.242 * (self.doy - 1))
        eot = eot1 - eot2
        return eot

    def get_eot_message(self) -> str:
        """Create Equation of Time info message.

        Returns:
            str: Equation of Time info message
        """
        eot = self.equation_of_time()
        fmt_eot = f"{abs(eot):.2f}"
        if eot > 0:
            eot_message = str(f"subtract {fmt_eot} minutes\n")
        elif eot < 0:
            eot_message = str(f"add {fmt_eot} minutes\n")
        return eot_message

    def output_summary(self, dial_tilt: float, dial_rotation: float) -> str:
        """Create summary of calculated values.

        Args:
            dial_tilt (float): Amount to tilt sundial to zero, in degrees
            dial_rotation (float): Amount to rotate sundial to zero, in degrees

        Returns:
            str: Sundial info summary
        """
        separator = f"--------------------\n"
        basic_info = f"Your sundial has been created based the coordinates: {round(self.latitude, 2), round(self.longitude, 2)}!\n"
        day_info = f"Based on that information, we have calculated the following:\nDay of Year: {self.doy}\nEquation of Time Adjustment: {self.get_eot_message()}"
        zeroing_message = f"To ensure greatest accuracy, please perform the following transformations to your sundial:\nTilt Sundial by {dial_tilt}°\nRotate Sundial by {dial_rotation}°\n"
        summary = f"\n{basic_info}{separator}{day_info}{separator}{zeroing_message}{separator}"
        return summary


def calculate(latitude: float, longitude: float) -> tuple:
    """Do necessary calculations and return various results

    Args:
        latitude (float): Sundial latitude
        longitude (float): Sundial longitude

    Returns:
        tuple: Formatted angle list, angle list, summary, dial tilt, dial rotation
    """
    angle_list = []
    fmt_angle_list = []
    chronos = Chronos(latitude, longitude)
    sundial_tz = chronos.get_timezone()
    utc_offset = chronos.get_utc_offset(sundial_tz)
    central_meridian = chronos.find_central_meridian(utc_offset)
    dial_tilt = chronos.calculate_dial_tilt(central_meridian)
    dial_rotation = chronos.calculate_dial_rotation(central_meridian)
    for time in chronos.times:
        round_time = chronos.get_round_time(time)
        formatted_time = chronos.format_time(round_time)
        tan_theta = chronos.calculate_tan_theta(time, chronos.latitude)
        result = max(-90, min(90, round(tan_theta, 2)))
        fmt_result = str(f"{formatted_time} = {result}°")
        angle_list.append(result)
        fmt_angle_list.append(fmt_result)
    summary = chronos.output_summary(dial_tilt, dial_rotation)
    return fmt_angle_list, angle_list, summary, dial_tilt, dial_rotation

import datetime
import math

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
            math.radians(self.longitude) - math.radians(central_meridian)
        ) * math.cos(math.radians(self.latitude))
        tilt = math.degrees(tilt_rad)
        return -round(float(tilt), 2)

    def calculate_dial_rotation(self, central_meridian: float) -> float:
        """Calculate amount to rotate sundial face to zero out difference from central meridian

        Args:
            central_meridian (float): Location of central meridian for sundial's timezone, in degrees

        Returns:
            float: Amount to rotate sundial, in degrees
        """
        diff_of_longs = self.longitude - central_meridian
        delta_diff = math.radians(diff_of_longs)
        rotation = math.sin(delta_diff) * math.sin(math.radians(self.latitude))
        rotation_angle = math.degrees(rotation)
        return -round(float(rotation_angle), 2)

    def get_hour_angle(self, hour: int) -> float:
        sin_of_lat = math.sin(math.radians(self.latitude))
        degree_hours = math.tan(hour * math.radians(15))
        theta = math.atan((sin_of_lat * degree_hours))
        theta_angle = math.degrees(theta)
        return theta_angle

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

    def equation_of_time(self) -> float:
        """Calculate equation of time to determine how much time should be adjusted for readings based on the day of the year

        Returns:
            float: Equation of Time
        """
        eot1 = 9.873 * math.sin((4 * π) / 365.242 * (self.doy - 81))
        eot2 = 7.655 * math.sin((2 * π) / 365.242 * (self.doy - 1))
        eot = eot1 - eot2
        return eot

    def zeroing_message(self, dial_tilt: float, dial_rotation: float) -> str:
        if dial_tilt > 0:
            tilt_message = f"Tilt dial by {dial_tilt}° counter-clockwise.\n"
        elif dial_tilt < 0:
            tilt_message = f"Tilt dial by {dial_tilt}° clockwise.\n"
        if dial_rotation > 0:
            rotation_message = f"Rotate dial by {dial_rotation}° counter-clockwise.\n"
        elif dial_rotation < 0:
            rotation_message = f"Rotate dial by {dial_rotation}° clockwise.\n"
        zeroing_message = tilt_message, rotation_message
        return zeroing_message

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
        tilt_message, rotation_message = self.zeroing_message(dial_tilt, dial_rotation)
        summary = f"{separator}{basic_info}{separator}{tilt_message}{rotation_message}{separator}"
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
        tan_theta = chronos.get_hour_angle(time)
        result = max(-90, min(90, round(tan_theta, 2)))
        fmt_result = str(f"{formatted_time} = {result}°")
        angle_list.append(result)
        fmt_angle_list.append(fmt_result)
    summary = chronos.output_summary(dial_tilt, dial_rotation)
    return fmt_angle_list, angle_list, summary, dial_tilt, dial_rotation

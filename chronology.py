import datetime
import math

π = math.pi


class Chronos:

    times = list(range(-6, 7))
    doy = datetime.date.today().timetuple().tm_yday

    def __init__(self, latitude):
        self.latitude = latitude

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

    def get_data_table(self) -> str:
        """Create information string reflecting the current Day of Year and Equation of Time

        Raises:
            Exception: If the Equation of Time happens to be exactly zero, errors arise

        Returns:
            str: Description of Day of Year and Equation of Time for the current day
        """
        doy = f"\nToday is day number {self.doy}."
        eot = self.equation_of_time()
        if eot > 0:
            subtract_eot = str(
                f"{doy}\nPlease subtract {abs(eot):2f} minutes from your readings today!\n"
            )
            return subtract_eot
        elif eot < 0:
            add_eot = str(
                f"{doy}\nPlease add {abs(eot):2f} minutes to your sundial readings today!\n"
            )
            return add_eot
        else:
            raise Exception("I'm not sure how we got here...")

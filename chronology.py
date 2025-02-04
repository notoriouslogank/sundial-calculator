import datetime
import math

from rich import print

π = math.pi

class Chronos():

    times = list(range(-6, 7))
    doy = datetime.date.today().timetuple().tm_yday

    def __init__(self, latitude):
        self.latitude = latitude

    def get_hour_angle(self, time: int) -> float:
        hour_angle = math.radians(time*15)
        return hour_angle

    def get_round_time(self, time: int) -> int:
        round_time = 12 + time
        return round_time

    def format_time(self, hour) -> str:
        raw_time = datetime.time(hour, 0)
        formatted_time = raw_time.strftime("%H:%M")
        return formatted_time

    def calculate_tan_theta(self, time: int, latitude: float) -> float:
        hour_angle = self.get_hour_angle(time)
        tan_hour_angle = math.tan(hour_angle)
        sin_latitude = math.sin(latitude)
        tan_theta = tan_hour_angle * sin_latitude
        result = math.degrees(math.atan(tan_theta))
        return result

    def equation_of_time(self) -> float:
        eot1 = 9.873 * math.sin((4 * π) / 365.242 * (self.doy - 81))
        eot2 = 7.655 * math.sin((2 * π) / 365.242 * (self.doy - 1))
        eot = eot1 - eot2
        return eot

    def get_data_table(self):
        print(f"\nToday is day number {self.doy}.")
        eot = self.equation_of_time()
        if eot > 0:
            subtract_eot = str(f"Please subtract {abs(eot):2f} minutes from your readings today!\n")
            return subtract_eot
        elif eot < 0:
            add_eot = str(f"Please add {abs(eot):2f} minutes to your sundial readings today!\n")
            return add_eot
        else:
            raise Exception("I'm not sure how we got here...")

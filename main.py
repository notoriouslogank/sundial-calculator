from rich import print

from chronology import calculate
from draw import create_sundial


def get_coordinates() -> tuple:
    """Prompt user for latitude and longitude coordinates

    Returns:
        tuple: latitude, longitude
    """
    coords = input(
        "Enter latitude and longitude for desired sundial location (decimal format): \n"
    )
    lat, long = coords.split(" ")
    latitude = float(lat.strip(","))
    longitude = float(long)
    return (latitude, longitude)


def write_info_file(summary: str, data: list):
    """Write summary and data to info.txt outfile.

    Args:
        summary (str): Summary of data used to construct sundial
        data (list): List of angles for hour markers
    """
    with open("info.txt", "w") as file:
        file.write(f"{summary}")
    for daton in data:
        with open("info.txt", "a") as file:
            file.write(f"{str(daton)}\n")


if __name__ == "__main__":
    latitude, longitude = get_coordinates()
    formatted_angle_list, angle_list, summary, dial_tilt, dial_rotation = calculate(
        latitude, longitude
    )
    create_sundial(latitude, longitude, angle_list, dial_tilt, dial_rotation)
    print(summary)
    write_info_file(summary, formatted_angle_list)

import math

import matplotlib.patches as patches
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
ORIGIN = (10, 10)


class Draw:

    def __init__(self, origin, radius):
        self.origin = origin
        self.radius = radius

    def create_circle(self):
        """Draw cirular dial face"""
        circle = patches.Circle(
            self.origin, self.radius, facecolor="white", edgecolor="black"
        )
        ax.add_patch(circle)
        return

    def draw_equatorial(self):
        """Draw the equatorial line (horizon) on dial face"""
        x_coordinates = [
            self.origin[0] - self.radius,
            self.origin[0] + self.radius,
        ]
        y_coordinates = [self.origin[1], self.origin[1]]
        plt.plot(x_coordinates, y_coordinates, color="black", linestyle="--")
        plt.title("Sundial")
        return

    def draw_meridian(self):
        """Draw meridian line (due North) on dial face"""
        x_coordinates = [
            self.origin[0],
            self.origin[0],
        ]
        y_coordinates = [
            self.origin[1],
            self.origin[1] + self.radius,
        ]
        plt.plot(x_coordinates, y_coordinates, color="red")
        true_north_x = self.origin[0]
        true_north_y = self.origin[1] + self.radius * 0.9
        ax.text(
            true_north_x,
            true_north_y,
            "N",
            ha="center",
            va="center",
            fontsize=20,
            fontweight="bold",
        )
        return

    def label_latitude(self, latitude: float):
        """Draw latitude label on sundial image

        Args:
            latitude (float): Sundial's latitude
        """
        latitude_x = self.origin[0]
        latitude_y = 12 - self.radius * 0.5
        ax.text(
            latitude_x,
            latitude_y,
            f"Latitude: {latitude}°",
            ha="center",
            va="center",
            fontsize=20,
            fontweight="bold",
        )

    def label_longitude(self, longitude: float):
        """Draw longitude label on sundial image

        Args:
            longitude (float): Sundial's longitude
        """
        longitude_x = 10
        longitude_y = 10 - self.radius * 0.5
        ax.text(
            longitude_x,
            longitude_y,
            f"Longitude: {longitude}°",
            ha="center",
            va="center",
            fontsize=20,
            fontweight="bold",
        )

    def label_dial_tilt(self, dial_tilt: float):
        """Draw dial tilt label on sundial image

        Args:
            dial_tilt (float): Amount of tilt to zero sundial
        """
        longitude_x = 10
        longitude_y = 8 - self.radius * 0.5
        ax.text(
            longitude_x,
            longitude_y,
            f"Dial tilt: {dial_tilt}°",
            ha="center",
            va="center",
            fontsize=15,
            fontweight="bold",
        )

    def label_dial_rotation(self, dial_rotation: float):
        """Draw dial rotation label on sundial image

        Args:
            dial_rotation (float): Amount of rotation to zero sundial
        """
        longitude_x = 10
        longitude_y = 6 - self.radius * 0.5
        ax.text(
            longitude_x,
            longitude_y,
            f"Dial Rotation: {dial_rotation}°",
            ha="center",
            va="center",
            fontsize=15,
            fontweight="bold",
        )

    def hour_line(self, angles: list):
        """Draw hourly demarcations on dial face based on calculated angles

        Args:
            angles (list): List of angles calculated for each hourly marker
        """
        angles_rad = []
        for angle in angles:
            angles_rad.append(math.radians(angle))
        for angle in angles_rad:
            x_end = self.origin[0] + self.radius * math.sin(angle)
            y_end = self.origin[1] + self.radius * math.cos(angle)
            ax.plot(
                [self.origin[0], x_end], [self.origin[1], y_end], "b", linewidth=0.5
            )
            label_x = self.origin[0] + (self.radius * 0.75) * math.sin(angle)
            label_y = self.origin[1] + (self.radius * 0.75) * math.cos(angle)

            ax.text(
                label_x,
                label_y,
                f"{math.degrees(angle):.2f}°",
                ha="center",
                va="center",
                fontsize=8,
            )

    def draw(self):
        """Configure settings for output image and write it to .png"""
        ax.set_aspect(
            "equal"
        )  # set aspect ratio prior to setting limits to avoid conflicts
        ax.set_xlim(
            [self.origin[0] - self.radius - 10, self.origin[0] + self.radius + 10]
        )
        ax.set_ylim(
            [self.origin[1] - self.radius - 10, self.origin[1] + self.radius + 10]
        )
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        plt.gca().set_position([0, 0, 1, 1])
        plt.savefig(f"sundial_template.png", bbox_inches=None, transparent=True)


def create_sundial(
    latitude: float,
    longitude: float,
    angle_list: list,
    dial_tilt: float,
    dial_rotation: float,
):
    """Draw sundial template and write image to sundial_template.png

    Args:
        latitude (float): Sundial latitude
        longitude (float): Sundial longitude
        angle_list (list): List of angles for hour marks
        dial_tilt (float): Degrees of tilt to zero sundial
        dial_rotation (float): Degrees of rotation to zero sundial
    """
    sundial = Draw(ORIGIN, 25)
    sundial.create_circle()
    sundial.draw_equatorial()
    sundial.draw_meridian()
    sundial.hour_line(angle_list)
    sundial.label_latitude(round(latitude, 2))
    sundial.label_longitude(round(longitude, 2))
    sundial.label_dial_tilt(dial_tilt)
    sundial.label_dial_rotation(dial_rotation)
    sundial.draw()
    return

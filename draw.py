import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy

fig, ax = plt.subplots(figsize=(10, 10), dpi=300)


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
            -5,
            25,
        ]  # TODO: Make these valuables relative to origin rather than hardcoded
        y_coordinates = [10, 10]  # TODO: See above
        plt.plot(x_coordinates, y_coordinates, color="black", linestyle="--")
        plt.title("Sundial")
        return

    def draw_meridian(self):
        """Draw meridian line (due North) on dial face"""
        x_coordinates = [
            10,
            10,
        ]  # TODO: Make these valuables relative to origin rather than hardcoded
        y_coordinates = [10, 25]  # TODO: See above
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

    def label_latitude(self, latitude):
        latitude_x = self.origin[0]
        latitude_y = self.origin[1] - self.radius * 0.5
        ax.text(
            latitude_x,
            latitude_y,
            f"Latitude: {latitude}°",
            ha="center",
            va="center",
            fontsize=20,
            fontweight="bold",
        )

    def hour_line(self, angles: list):
        """Draw hourly demarcations on dial face based on calculated angles

        Args:
            angles (list): List of angles calculated for each hourly marker
        """
        angles_rad = numpy.radians(angles)
        for angle in angles_rad:
            x_end = self.origin[0] + self.radius * numpy.sin(angle)
            y_end = self.origin[1] + self.radius * numpy.cos(angle)
            ax.plot(
                [self.origin[0], x_end], [self.origin[1], y_end], "b", linewidth=0.5
            )
            label_x = self.origin[0] + (self.radius * 0.75) * numpy.sin(angle)
            label_y = self.origin[1] + (self.radius * 0.75) * numpy.cos(angle)

            ax.text(
                label_x,
                label_y,
                f"{numpy.rad2deg(angle)}°",
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

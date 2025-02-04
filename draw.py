import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy

fig, ax = plt.subplots(figsize=(10, 10), dpi=300)

class Draw():

    def __init__(self, origin, radius):
        self.origin = origin
        self.radius = radius

    def create_circle(self):
        circle = patches.Circle(self.origin, self.radius, facecolor="white", edgecolor="black")
        ax.add_patch(circle)
        return

    def draw_equatorial(self):
        x_coordinates = [-5, 25]
        y_coordinates = [10, 10]
        plt.plot(x_coordinates, y_coordinates, color="black", linestyle="--")
        plt.title("Sundial")
        return

    def draw_meridian(self):
        x_coordinates = [10, 10]
        y_coordinates = [10, 25]
        plt.plot(x_coordinates, y_coordinates, color="red")
        return

    def hour_line(self, angles):
        angles_rad = numpy.radians(angles)
        for angle in angles_rad:
            x_end = self.origin[0] + self.radius * numpy.sin(angle)
            y_end = self.origin[1] + self.radius * numpy.cos(angle)
            ax.plot([self.origin[0], x_end], [self.origin[1], y_end], 'b', linewidth=0.5)

    def draw(self):
        ax.set_aspect('equal') # set aspect ratio prior to setting limits
        ax.set_xlim([self.origin[0] - self.radius - 10, self.origin[0] + self.radius + 10])
        ax.set_ylim([self.origin[1] - self.radius - 10, self.origin[1] + self.radius + 10])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        plt.gca().set_position([0, 0, 1, 1])
        plt.savefig("sundial.png", bbox_inches=None, transparent=True)
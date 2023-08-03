from manimlib import *
import numpy as np


class CoordinateSystemExample(Scene):
    def construct(self):
        axes = Axes(
            # x-axis ranges from -1 to 10, with a default step size of 1
            x_range=(-5, 15),
            # y-axis ranges from -2 to 2 with a step size of 0.5
            y_range=(-5, 15, 1),
            # The axes will be stretched so as to match the specified
            # height and width
            height=6,
            width=10,
            # Axes is made of two NumberLine mobjects.  You can specify
            # their configuration with axis_config
            axis_config={
                "stroke_color": GREY_A,
                "stroke_width": 2,
            },
            # Alternatively, you can specify configuration for just one
            # of them, like this.
            # y_axis_config={
            #     "include_tip": False,
            # }
        )
        axes.add_coordinate_labels(
            font_size=12,
            num_decimal_places=1,
        )
        self.add(axes)


        x = np.arange(0, 10)
        y = x + 2

        points = list(zip(x, y))
        
        for dot in points:
            x, y = dot

            dot = Dot(color=GREEN)
            dot.move_to(axes.c2p(x, y))
            self.add(dot)


        dot_red = Dot(color=RED)
        self.add(dot_red)
        dot_red.move_to(axes.c2p(points[0][0], points[0][1]))

        while True:
            for point in points:
                x, y = point
                self.play(dot_red.animate.move_to(axes.c2p(x, y)))
